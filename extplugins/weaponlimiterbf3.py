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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import b3
import b3.events
import b3.plugin
import b3.cron

__version__ = '0.2'
__author__ = 'ozon'

class Weaponlimiterbf3Plugin(b3.plugin.Plugin):
    _adminPlugin = None
    _wpl_is_active = None
    _cronTab = None
    _punisherCfg = {}
    _message = {}
    _weapon_list = []
    _mode = None

    def onLoadConfig(self):
        # remove eventual existing crontab
        if self._cronTab:
            self.console.cron - self._cronTab
        # load punisher settings
        for key in self.config.options('punisher-settings'):
            self._punisherCfg[key] = self.config.getboolean('punisher-settings', key)
        # Load messages
        for key in self.config.options('messages'):
            self._message[key] = self.config.get('messages', key)

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
                if weapon in self._weapon_list and self._mode == 'blacklist':
                    self.debug('%s in pattern detected' % weapon)
                    self._punish_player(self, event)
                elif weapon not in self._weapon_list and self._mode == 'whitelist':
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


    # configure limiter per map
    def _configure_wpl(self):
        """ Load weaponlimiter Configuration per map/gametype """
        _current_map = self.console.game.mapName
        _current_gameType = self.console.game.gameType
        self.debug('Current Map/gameType: %s/%s' % (_current_map, _current_gameType))

        if self.config.has_section(_current_map) and _current_gameType in self.get_cfg_value_list(_current_map, 'gametype'):
            self.debug('Configure WeaponLimiter for %s/%s' % (_current_map, _current_gameType))
            self._weapon_list = self.get_cfg_value_list(_current_map, 'weapons')
            self._mode =  self.config.get(_current_map, 'mode')
            self.console.say(self.getMessage('weaponlimiter_enabled'))
            self.notice_forbidden_weapons()
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
        if self._punisherCfg['kill_player']:
            try:
                self.console.write(('admin.killPlayer', killer.name))
                killer.message('Kill reason: Killed by Admin. %s is forbidden!' % weapon)
            except CommandFailedError, err:
                killer.message('%s is forbidden!' % weapon)

        if self._punisherCfg['warn_player']:
            _wmsg = '%s is forbidden!' % weapon
            self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)


    def _disable_wpl(self):
        """ Disable weaponlimiter activity """
        self._weapon_list = []
        if self._wpl_is_active:
            self.console.say(self._message['weaponlimiter_disabled'])
            self._wpl_is_active = False
            self._update_crontab()
            if self._cronTab:
                self.console.cron - self._cronTab

    def notice_forbidden_weapons(self):
        if self._mode == 'blacklist':
            self.console.say(self.getMessage('forbidden_message', ', '.join(self._weapon_list)))
        elif self._mode == 'whitelist':
            self.console.say(self.getMessage('allowed_message', ', '.join(self._weapon_list)))

    def _update_crontab(self):
        if self._weapon_list:
            notify_every_min = self.config.getint('settings', 'notice_message_cron')
            self._cronTab = b3.cron.PluginCronTab(self, self.notice_forbidden_weapons, minute='*/%s' % notify_every_min)
            if not self._cronTab:
                self.console.cron + self._cronTab
        else:
            if self._cronTab:
                self.console.cron - self._cronTab

    def cmd_weaponlimiter(self, data, client, cmd=None):
        """ Handle WeaponLimiter """
        if client:
            if not data:
                if self._wpl_is_active:
                    client.message(self._message['weaponlimiter_enabled'])
                else:
                    client.message(self._message['weaponlimiter_disabled'])
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


### helper functions ###

    def get_cfg_value_list(self, cfg_section, cfg_setting):
        """
        Load values from plugin configuration section
        @return: list from section values
        @param cfg_section: section in config File
        @param cfg_settings: value in cofigration section
        """
        return [x.strip() for x in self.config.get(cfg_section, cfg_setting).split(',')]

    def getCmd(self, cmd):
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

                func = self.getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

if __name__ == '__main__':

    from b3.fake import fakeConsole, superadmin, joe
    import time

    myplugin = Weaponlimiterbf3Plugin(fakeConsole, '@b3/extplugins/conf/plugin_weaponlimiterbf3.xml')
    myplugin.onStartup()
    time.sleep(2)


    superadmin.connects(cid=0)
    superadmin.says('!weaponlimiter')
    superadmin.says('!wpl on')


