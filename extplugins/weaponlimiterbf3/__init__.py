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
from b3.plugin import Plugin
from b3.parsers.frostbite2.protocol import CommandFailedError
from pluginconf import PluginConfig
from weapondef import WEAPON_NAMES_BY_ID, BF4_WEAPON_NAMES_BY_ID
from b3.parsers.bf3 import MAP_NAME_BY_ID, GAME_MODES_NAMES, MAP_ID_BY_NAME, GAME_MODES_BY_MAP_ID

from b3.parsers.bf4 import MAP_NAME_BY_ID as BF4_MAP_NAME_BY_ID
from b3.parsers.bf4 import GAME_MODES_NAMES as BF4_GAME_MODES_NAMES
from b3.parsers.bf4 import MAP_ID_BY_NAME as BF4_MAP_ID_BY_NAME
from b3.parsers.bf4 import GAME_MODES_BY_MAP_ID as BF4_GAME_MODES_BY_MAP_ID


__version__ = '0.9.2'
__author__ = 'ozon'


class Weaponlimiterbf3Plugin(Plugin):

    MAP_NAME_BY_ID = None
    GAME_MODES_NAMES = None
    MAP_ID_BY_NAME = None
    GAME_MODES_BY_MAP_ID = None
    WEAPON_NAMES_BY_ID = None
    _adminPlugin = None
    _wpl_is_active = None
    _messages = {}
    _default_messages = {
        'servermessage': 'This game uses weapons limits. Use !weaponlimits to show forbidden weapons.',
        'weaponlimiter_enabled': 'WeaponLimiter for that round activated!',
        'weaponlimiter_disabled': 'Weaponlimiter disabled! All Weapons allowed.',
        'warn_message': 'You used a forbidden weapon! ^7!forbidden_weapons show the list of forbidden weapons',
        'forbidden_message': 'Forbidden Weapons are: %s',
        'allowed_message': 'Allowed Weapons: %s',
        'extra_warning_message': 'You have %(victim)s killed with a %(weapon)s. This weapon is forbidden!',
    }
    _plugin_config = None
    # general settings
    _settings = {}
    _default_settings = {
        'autostartup': False,
        'config_strategy': ('mapname', 'gametype'),
        'anounce_limits_on_first_spawn': True,
        'self_kill_counter': 1,
        'change servermessage': False,
        'display_extra_msg': 'message',
        'yell_duration': 10,
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
    _mapconfig_template = {}
    _old_servermessage = None

    def onLoadConfig(self):
        self._plugin_config = PluginConfig(self)
        # load configuration
        self._plugin_config.load_settings(self._default_settings, 'settings', self._settings)
        self._plugin_config.load_settings(default_settings=self._default_punisher_settings, section='punisher',
                                          to_settings=self._punisher_settings)
        # backup servermessage
        if self._settings['change servermessage']:
            try:
                _old_servermessage = self.console.getCvar('serverMessage')
                self._old_servermessage = _old_servermessage if _old_servermessage is not None else ''
            except CommandFailedError, err:
                self.error('Failed to get vars.serverMessage')

        # Load messages
        for key in self.config.options('messages'):
            self._messages[key] = self.config.get('messages', key, True)

        self._weaponlimiter_enabled_msg = self.config.get('messages', 'weaponlimiter_enabled')
        self.cmd_weaponlimiter_wlist_text = self.config.get('messages', 'warn_message')

    def onStartup(self):
        """ Initialize plugin settings """
        # check if bf3/bf4 game and load constants
        if self.console.game.gameName == 'bf3':
            self.MAP_NAME_BY_ID = MAP_NAME_BY_ID
            self.GAME_MODES_NAMES = GAME_MODES_NAMES
            self.MAP_ID_BY_NAME = MAP_ID_BY_NAME
            self.GAME_MODES_BY_MAP_ID = GAME_MODES_BY_MAP_ID
            self.WEAPON_NAMES_BY_ID = WEAPON_NAMES_BY_ID
        elif self.console.game.gameName == 'bf4':
            self.MAP_NAME_BY_ID = BF4_MAP_NAME_BY_ID
            self.GAME_MODES_NAMES = BF4_GAME_MODES_NAMES
            self.MAP_ID_BY_NAME = BF4_MAP_ID_BY_NAME
            self.GAME_MODES_BY_MAP_ID = BF4_GAME_MODES_BY_MAP_ID
            self.WEAPON_NAMES_BY_ID = BF4_WEAPON_NAMES_BY_ID
        else:
            self.error('This plugin only works with Battlefield 3 (bf3) or Battlefield 4 (bf4).')
            return False
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
        self.registerEvent(b3.events.EVT_GAME_WARMUP)
        self.registerEvent(b3.events.EVT_GAME_ROUND_END)
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)

        self._mapconfig_template = {
            'weapons': list(self.WEAPON_NAMES_BY_ID),
            'gametype': list(self.GAME_MODES_NAMES),
            'mode': 'blacklist'
        }
        # load map configuration
        self._load_mapconfiguration()

    def onEvent(self, event):
        """ Handle CLIENT_KILL and GAME_ROUND_START events """
        if event.type == b3.events.EVT_CLIENT_KILL and self._wpl_is_active and self.console.game.gameType in self._mapconfig[self.console.game.mapName]['gametype']:
            try:
                killer = event.client
                weapon = event.data[1]
                if killer.name == event.target.name:
                    self.debug('Suicide detected.')
                    return
                elif weapon in ('Death', 'DamageArea', 'SoldierCollision'):
                    self.debug('Death by %s detected.' % weapon)
                    return
                elif self._is_forbidden_weapon(weapon):
                    self.debug('%s in pattern detected' % weapon)
                    self._punish_player(self, event)
            except IndexError:
                pass
        # activate wpl if we have a configuration for the current map/gametype
        if event.type == b3.events.EVT_GAME_WARMUP:
            if self.console.game.mapName in self._mapconfig:
                if self.console.game.gameType in self._mapconfig[self.console.game.mapName]['gametype']:
                    self.debug('Found configuration for current map/gametype. Activate Weaponlimiter.')
                    self._wpl_is_active = True
                    self._update_servermessage()
        # disable wpl on round end or mapchange
        if event.type == b3.events.EVT_GAME_ROUND_END or event.type == b3.events.EVT_GAME_MAP_CHANGE:
            if self._wpl_is_active:
                self.debug('Round end or map changed. Disable Weaponlimiter')
                self._wpl_is_active = False
                self._update_servermessage()


    def _is_forbidden_weapon(self, weapon):
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

    # punish player
    def _punish_player(self, event, data=None, client=None):
        """ Punish player """
        weapon = self.WEAPON_NAMES_BY_ID[data.data[1]]['name']
        killer = data.client
        victim = data.target
        if self._punisher_settings['kill_player']:
            try:
                self.console.write(('admin.killPlayer', killer.name))
                killer.message('Kill reason: Killed by Admin. %s is forbidden!' % weapon)
            except CommandFailedError, err:
                killer.message('%s is forbidden!' % weapon)

        if self._punisher_settings['warn_player']:
            _wmsg = '%s is forbidden!' % weapon
            self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)

        if self._settings['display_extra_msg'] == 'message':
            killer.message(self._messages['extra_warning_message'] % ({'victim': victim.name, 'weapon': weapon}))
        elif self._settings['display_extra_msg'] == 'yell':
            _msg = self._messages['extra_warning_message'] % ({'victim': victim.name, 'weapon': weapon})
            self.console.write(self.console.getCommand('bigmessage', message=_msg, cid=killer.cid, big_msg_duration=self._settings['yell_duration']))

    def _disable_wpl(self):
        """ Disable weaponlimiter activity """
        if self._wpl_is_active:
            self.console.say(self._messages['weaponlimiter_disabled'])
            self._wpl_is_active = False
            self._update_servermessage()

    def _report_weaponlist(self, client=None):
        if self._wpl_is_active:
            msg = 'No Limits aktive'
            if self._mapconfig[self.console.game.mapName]['mode'] == 'blacklist':
                msg = self.getMessage('forbidden_message', ', '.join(
                    self._get_human_readable_weaponlist()))
            elif self._mapconfig[self.console.game.mapName]['mode'] == 'whitelist':
                msg = self.getMessage('allowed_message', ', '.join(
                    self._get_human_readable_weaponlist()))

            if client:
                client.message(msg)
            else:
                self.console.say(msg)

    def _maps_from_fonfig(self):
        _maps = dict()
        for mapname in self.config.sections():
            # 'ziba tower' > 'XP2_Skybar'
            if mapname.lower() in self.MAP_ID_BY_NAME:
                _maps[self.MAP_ID_BY_NAME.get(mapname.lower())] = ''
            # 'XP2_Skybar'
            elif mapname in self.MAP_NAME_BY_ID:
                _maps[mapname] = ''

        return _maps

    def _load_mapconfiguration(self):

        def setmapconfig(mapid):
            self._mapconfig.update({
                mapid: dict()
            })
            self._plugin_config.load_settings(self._mapconfig_template, mapid, self._mapconfig[mapid])

        _maps = self._maps_from_fonfig()
        for mapid in _maps:
            self.debug('Load map configuration for %s', self.MAP_NAME_BY_ID[mapid])
            setmapconfig(mapid)
            if not self._mapconfig_is_valid(mapid):
                self.error('Configuration for %s are wrong!', mapid)
                self._mapconfig.pop(mapid)

    def _mapconfig_is_valid(self, mapid):
        # check weapon list
        for weapon in self._mapconfig[mapid].get('weapons'):
            if weapon not in list(self.WEAPON_NAMES_BY_ID):
                self.debug('%s is not a valied weapon')
                return False
            #check gamemodes
        for gamemode in self._mapconfig[mapid].get('gametype'):
            if gamemode not in self.GAME_MODES_BY_MAP_ID[mapid] or gamemode in self._disable_on_gamemode:
                self.debug('%s not support %s' % (mapid, gamemode))
                return False

        return True

    def _get_human_readable_weaponlist(self, weaponlist=None):
        _weaponlist = list()
        if not weaponlist:
            weaponlist = self._mapconfig[self.console.game.mapName]['weapons']

        for weapon in weaponlist:
            _weaponlist.append(self.WEAPON_NAMES_BY_ID[weapon]['name'])

        return _weaponlist

    def cmd_weaponlimiter(self, data, client, cmd=None):
        """\
        <on|off> manage the WeaponLimiter
        """
        if client:
            if not data:
                if self._wpl_is_active:
                    client.message(self._messages['weaponlimiter_enabled'])
                else:
                    client.message(self._messages['weaponlimiter_disabled'])
            else:
                if data not in ('on', 'off'):
                    client.message("Invalid parameter. Expecting one of : 'on', 'off'")
                elif data == 'on':
                    if self._wpl_is_active:
                        client.message('WeaponLimiter is allready active.')
                    else:
                        self._wpl_is_active = True
                        self.console.say(self._messages['weaponlimiter_enabled'])
                        self._report_weaponlist()
                        self._update_servermessage()
                        #self._configure_wpl()
                elif data == 'off':
                    self._disable_wpl()

    def cmd_weaponlimits(self, data, client, cmd=None):
        """ Show weapon Limits """
        if client and self._wpl_is_active:
            self._report_weaponlist(client)

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

    def _update_servermessage(self):
        """Update welcome message"""
        _new_servermessage = self._old_servermessage
        if self._settings['change servermessage'] and self._wpl_is_active:
            _new_servermessage = self.config.get('messages', 'servermessage')

        try:
            self.console.setCvar('serverMessage', _new_servermessage)
            self.debug('Change servermessage to: %s', _new_servermessage)
        except CommandFailedError, err:
            self.error('Failed to change vars.serverMessage - Error: %s', err)
