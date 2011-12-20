# -*- coding: utf-8 -*-
#
# Weaponlimiter (BF3) Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011 <ozon>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Changelog:
#

# taken  https://github.com/courgette/b3-plugin-teamspeak/blob/master/extplugins/teamspeak.py as sample

import b3
import b3.events
import b3.plugin

__version__ = '0.1'
__author__ = 'ozon'


class Weaponlimiterbf3Plugin(b3.plugin.Plugin):
    _adminPlugin = None
    _weapon_limiter_is_active = None

    # load punisher setting in a dict
    # TODO: should test option and more generic
    def load_punisherConfig(self):
        punisher_settings = {}
        for key in self.config.options('punisher-settings'):
            punisher_settings[key] = self.config.getboolean('punisher-settings', key)
        
        return punisher_settings
        
    # load settings from config file (i think the b3 API should provide safer methods)
    # wrong options break the code
    def onLoadConfig(self):
        self._weaponlimiter_disabled_msg = self.config.get('messages', 'weaponlimiter_disabled')
        self._weaponlimiter_enabled_msg = self.config.get('messages', 'weaponlimiter_enabled')
        self.cmd_weaponlimiter_wlist_text = self.config.get('messages', 'warn_message')
        #loading punisher settings
        self._punisher_settings = self.load_punisherConfig()
        


    def onStartup(self):
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
        # register our command
        self._register_commands()
        # disable WeaponLimiter per default
        self._weapon_limiter_is_active = False
        # register Events
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        # load punisher settings
        self._punisher_settings = self.load_punisherConfig()
        


    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_KILL and self._weapon_limiter_is_active:
            try:
                killer = event.client
                weapon = event.data[1]
                if weapon in self.forbidden_weapons:
                    self.debug('%s in pattern detected' % weapon)
                    
                    self._punish_player(self, event)
                    ##or self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
                    ##no outout msg## killer.warn('1h', _wmsg, None, None, '')
                    #self._adminPlugin.warnClient(killer.id, '', True, False, _wmsg, 1)
                    #if self.kill_killer == 1:
                    #   kill.
            except IndexError:
                pass

        if event.type == b3.events.EVT_GAME_ROUND_START and self._weapon_limiter_is_active:
            try:
                self._configure_weaponlimiter()
            except IndexError:
                pass

    
    # configure limiter per map
    def _configure_weaponlimiter(self):
        if self._weapon_limiter_is_active:
            _current_map = self.console.game.mapName
            _current_gameType = self.console.game.gameType
            self.debug('Current Map/gameType: %s/%s' % (_current_map, _current_gameType))
            
            if self.config.has_section(_current_map) and _current_gameType in self._get_cfg_value_list(_current_map, 'gametype'):
                self.debug('Configure WeaponLimiter for %s/%s' % (_current_map, _current_gameType))
                self.console.say(self._weaponlimiter_enabled_msg)
                self.forbidden_weapons = self._get_cfg_value_list(_current_map, 'weapons')
            else:
                self.debug('No configuration found for %s/%s' % (_current_map, _current_gameType))
                self._disable_weaponlimiter()


    # punish player
    def _punish_player(self, event, data=None, client=None):
        weapon = data.data[1]
        killer = data.client
        if self._punisher_settings['kill_player']:
            _kmsg = 'Use forbidden %s' % weapon
            self.console.write(('admin.killPlayer', killer.name))
            # TODO: check if player live for kill
            killer.message('Kill reason: %s' % _kmsg)
        
        if self._punisher_settings['warn_player']:
            _wmsg = '%s is forbidden!' % weapon
            self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
        
        if self._punisher_settings['kick_player']:
            pass
            

    def _disable_weaponlimiter(self):
        self.forbidden_weapons = []
        if self._weapon_limiter_is_active:
            self.console.say(self._weaponlimiter_disabled_msg)
            
        self._weapon_limiter_is_active = False
            

    def cmd_weaponlimiter(self, data, client, cmd=None):
        if client:            
            if not data:
                status_msg = ''
                if self._weapon_limiter_is_active:
                    status_msg = 'WeaponLimiter is active!'
                else:
                    status_msg = 'WeaponLimiter is disabled!'
                client.message(status_msg)
            else:
                if data not in ('on', 'off', 'pause'):
                    client.message("Invalid parameter. Expecting one of : 'on', 'off', 'pause'")
                elif data == 'on':
                    self._weapon_limiter_is_active = True
                    self._configure_weaponlimiter()
                elif data == 'off':
                    self._disable_weaponlimiter()



### helper functions ###

    def _get_cfg_value_list(self, cfg_section, cfg_setting):
        return [x.strip() for x in self.config.get(cfg_section, cfg_setting).split(',')]

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

    from b3.fake import fakeConsole, superadmin, joe
    import time

    myplugin = Weaponlimiterbf3Plugin(fakeConsole, '@b3/extplugins/conf/plugin_weaponlimiterbf3.xml')
    myplugin.onStartup()
    time.sleep(2)


    superadmin.connects(cid=0)
    superadmin.setvar('weaponlimiterbf3', 'test','blub')
    print(dir(superadmin))
    print(superadmin.var('weaponlimiterbf3','test'))
    superadmin.says('!weaponlimiter')

