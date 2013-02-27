# -*- coding: utf-8 -*-

# Weaponlimiter Plugin for BigBrotherBot(B3)
# Copyright (c) 2012 Harry Gabriel <h.gabriel@nodefab.de>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import b3
import b3.events
import b3.plugin
import b3.cron
from b3.parsers.frostbite2.protocol import CommandFailedError
from pluginconf import PluginConfig
from weapondef import WEAPON_NAMES_BY_ID
from b3.parsers.bf3 import MAP_NAME_BY_ID, GAME_MODES_NAMES, MAP_ID_BY_NAME

__version__ = '0.9.0'
__author__ = 'ozon'


class Weaponlimiterbf3Plugin(b3.plugin.Plugin):
    _adminPlugin = None
    _wpl_is_active = None
    _cronTab = None
    _messages = {}
    _default_messages = {}
    _weapon_list = []
    _mode = None
    _plugin_config = None

    # general settings
    _settings = {}
    _default_settings = {
        'autostartup': False,
        'config_strategy': ('mapname', 'gametype'),
        'anounce_limits_on_first_spawn': True,
        'self_kill_counter': 1,
    }
    # settings for players punishment
    _punisher_settings = {}
    _default_punisher_settings = {
        'kill_player': False,
        'warn_player': True,
    }
    # wpl dont work on:
    _disable_on_gamemode = ['GunMaster0']

    _mapconfig = {}
    _mapconfig_template = {
        'weapons': list(WEAPON_NAMES_BY_ID),
        'gametype': list(GAME_MODES_NAMES),
        'mode': 'blacklist'
    }

    def onLoadConfig(self):
        self._plugin_config = PluginConfig(self)
        # load configuration
        self._plugin_config.load_settings(self._default_settings, 'settings', self._settings)
        self._plugin_config.load_settings(default_settings=self._default_punisher_settings, section='punisher',
                                          to_settings=self._punisher_settings)
        # load map configuration
        self.load_mapconfiguration()
        # remove eventual existing crontab
        if self._cronTab:
            self.console.cron - self._cronTab

        # Load messages
        for key in self.config.options('messages'):
            self._messages[key] = self.config.get('messages', key)

        self._weaponlimiter_enabled_msg = self.config.get('messages', 'weaponlimiter_enabled')
        self.cmd_weaponlimiter_wlist_text = self.config.get('messages', 'warn_message')

    def onStartup(self):
        """ Initialize plugin settings """
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
            # register our command
        self._register_commands()
        # disable WeaponLimiter per default
        self._wpl_is_active = False
        # register Events
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)

    def onEvent(self, event):
        """ Handle CLIENT_KILL and GAME_ROUND_START events """
        if event.type == b3.events.EVT_CLIENT_KILL and self._wpl_is_active:
            try:
                killer = event.client
                weapon = event.data[1]
                if killer.name == event.target.name:
                    self.debug('Suicide detected.')
                    return
                elif self.is_forbidden_weapon(weapon):
                    self.debug('%s in pattern detected' % weapon)
                    self._punish_player(self, event)
                    ##or self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
                    ##no outout msg## killer.warn('1h', _wmsg, None, None, '')
                    #self._adminPlugin.warnClient(killer.id, '', True, False, _wmsg, 1)
                    #if self.kill_killer == 1:
                    #   kill.
            except IndexError:
                pass

        if event.type == b3.events.EVT_GAME_ROUND_START and self._wpl_is_active:
            try:
                self._configure_wpl()
            except IndexError:
                pass

    def is_forbidden_weapon(self, weapon):
        """Check if a weapon in the list of banned weapons."""
        weaponlist = self._mapconfig[self.console.game.mapName].get('weapons')
        mode = self._mapconfig[self.console.game.mapName].get('mode')
        if mode == 'blacklist':
            if weapon in weaponlist:
                return True
        elif mode == 'whitelist':
            if weapon not in weaponlist:
                return True

        return False

        # configure limiter per map
    def _configure_wpl(self):
        """ Load weaponlimiter Configuration per map/gametype """
        _current_map = self.console.game.mapName
        _current_gameType = self.console.game.gameType
        self.debug('Current Map/gameType: %s/%s' % (_current_map, _current_gameType))

        if _current_map in self._mapconfig and _current_gameType in self._mapconfig[_current_map]['gametype']:
            self.debug('Configure WeaponLimiter for %s/%s' % (_current_map, _current_gameType))
            self._weapon_list = self._mapconfig[_current_map].get('weapons')
            self.console.say(self.getMessage('weaponlimiter_enabled'))
            self._report_weaponlist()
            self._update_crontab()
        else:
            self.debug('No configuration found for %s/%s' % (_current_map, _current_gameType))
            self._weapon_list = []
            self._update_crontab()

    # punish player
    def _punish_player(self, event, data=None, client=None):
        """ Punish player """
        weapon = data.data[1]
        killer = data.client
        if self._punisher_settings['kill_player']:
            try:
                self.console.write(('admin.killPlayer', killer.name))
                killer.message('Kill reason: Killed by Admin. %s is forbidden!' % weapon)
            except CommandFailedError, err:
                killer.message('%s is forbidden!' % weapon)

        if self._punisher_settings['warn_player']:
            _wmsg = '%s is forbidden!' % weapon
            self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)

    def _disable_wpl(self):
        """ Disable weaponlimiter activity """
        self._weapon_list = []
        if self._wpl_is_active:
            self.console.say(self._messages['weaponlimiter_disabled'])
            self._wpl_is_active = False
            self._update_crontab()
            if self._cronTab:
                self.console.cron - self._cronTab

    def _report_weaponlist(self):
        if self._mode == 'blacklist':
            self.console.say(self.getMessage('forbidden_message', ', '.join(self._weapon_list)))
        elif self._mode == 'whitelist':
            self.console.say(self.getMessage('allowed_message', ', '.join(self._weapon_list)))

    def _update_crontab(self):
        if self._weapon_list:
            notify_every_min = self.config.getint('settings', 'notice_message_cron')
            self._cronTab = b3.cron.PluginCronTab(self, self._report_weaponlist, minute='*/%s' % notify_every_min)
            if not self._cronTab:
                self.console.cron + self._cronTab
        else:
            if self._cronTab:
                self.console.cron - self._cronTab

    def _maps_from_fonfig(self):
        _maps = dict()
        for mapname in self.config.sections():
            # 'ziba tower' > 'XP2_Skybar'
            if mapname.lower() in MAP_ID_BY_NAME:
                _maps[MAP_ID_BY_NAME.get(mapname.lower())] = ''
            # 'XP2_Skybar'
            elif mapname in MAP_NAME_BY_ID:
                _maps[mapname] = ''

        return _maps

    def load_mapconfiguration(self):

        def setmapconfig(mapid):
            self._mapconfig.update({
                mapid: dict()
            })
            self._plugin_config.load_settings(self._mapconfig_template, mapid, self._mapconfig[mapid])
            self._test_weapons(self._mapconfig[mapid]['weapons'])
            # ToDo: test gamemode

        _maps = self._maps_from_fonfig()
        for mapid in _maps:
            self.debug('Load map configuration for %s', MAP_NAME_BY_ID[mapid])
            setmapconfig(mapid)

    def _test_weapons(self, weapons):
        for weapon in weapons:
            if weapon not in list(WEAPON_NAMES_BY_ID):
                self.error('%s is not a valied wepoan')
                # TODO: kick config

    def cmd_weaponlimiter(self, data, client, cmd=None):
        """ Handle WeaponLimiter """
        if client:
            if not data:
                if self._wpl_is_active:
                    client.message(self._messages['weaponlimiter_enabled'])
                else:
                    client.message(self._messages['weaponlimiter_disabled'])
            else:
                if data not in ('on', 'off', 'pause'):
                    client.message("Invalid parameter. Expecting one of : 'on', 'off', 'pause'")
                elif data == 'on':
                    if self._wpl_is_active:
                        client.message('WeaponLimiter is allready active.')
                    else:
                        self._wpl_is_active = True
                        self._configure_wpl()
                elif data == 'off':
                    self._disable_wpl()

    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None

    def _register_commands(self):
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)


if __name__ == '__main__':
    from b3.fake import fakeConsole, superadmin, joe, simon
    import time

    myplugin = Weaponlimiterbf3Plugin(fakeConsole, 'conf/plugin_weaponlimiterbf3.ini')
    myplugin.onStartup()
    time.sleep(2)
    myplugin.console.game.gameName = 'bf3'
    myplugin.console.game.gameType = 'Domination0'
    myplugin.console.game._mapName = 'XP2_Skybar'
    superadmin.connects(cid=0)
    # make joe connect to the fake game server on slot 1
    joe.connects(cid=1)
    # make joe connect to the fake game server on slot 2
    simon.connects(cid=2)
    # superadmin put joe in group user
    superadmin.says('!putgroup joe user')
    superadmin.says('!putgroup simon user')

    superadmin.connects(cid=0)
    superadmin.says('!weaponlimiter')
    superadmin.says('!wpl on')


