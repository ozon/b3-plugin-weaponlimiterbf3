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
    #_poweradminbf3Plugin = None
    
    

    def onLoadConfig(self):
        self._weapon_limiter_is_active = self.config.getboolean('settings', 'autostart')
        self._weaponlimiter_disabled_msg = self.config.get('messages', 'weaponlimiter_disabled')
        self._weaponlimiter_enabled_msg = self.config.get('messages', 'weaponlimiter_enabled')
        self.cmd_weaponlimiter_wlist_text = self.config.get('messages', 'warn_message')


    def onStartup(self):
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
        
        #self._poweradminbf3Plugin = self.console.getPlugin('poweradminbf3')

        self._register_commands()
        self._weapon_limiter_is_active = self.config.getboolean('settings', 'autostart')
        
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)


    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_KILL and  self._weapon_limiter_is_active:
            try:
                killer = event.client
                weapon = event.data[1]
                if weapon in self.forbidden_weapons:
                    #cmd_warn(self, data=None, client=killer, cmd=None)
                    _wmsg = '%s is forbidden!' % weapon
                    _kmsg = 'Use forbidden %s' % weapon
    #               self.console.write(('admin.killPlayer', killer))
#                   killer.message('Kill reason: %s' % _kmsg)
                    
                    self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
                    ##or self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
                    ##no outout msg## killer.warn('1h', _wmsg, None, None, '')
                    #self._adminPlugin.warnClient(killer.id, '', True, False, _wmsg, 1)
                    #if self.kill_killer == 1:
                    #   kill.
            except IndexError:
                pass

        if event.type == b3.events.EVT_GAME_ROUND_START:
            try:
                self._configure_weaponlimiter()
            except IndexError:
                pass
        
    def _configure_weaponlimiter(self):
        _current_map = self.console.game.mapName
        _current_gameType = self.console.game.gameType
        self.debug('Current Map/gameType: %s/%s' % (_current_map, _current_gameType) )
            
        if self.config.has_section(_current_map) and _current_gameType in self._get_cfg_value_list(_current_map, 'gametype'):
            self.debug('Configuration found')
            self.console.say(self._weaponlimiter_enabled_msg)
            self.forbidden_weapons = self._get_cfg_value_list(_current_map, 'weapons')
        else:
            self._disable_weaponlimiter()
            
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
                    self._configure_weaponlimiter()
                    self._weapon_limiter_is_active = True
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
    game = Game(fakeConsole, 'fakegamename')

    from b3.config import XmlConfigParser
    mcfg = XmlConfigParser()
    mcfg.readfp('/home/ozon/bf3_stuff/b3plugingit/b3-plugin-weaponlimiterbf3/extplugins/conf/plugin_weaponlimiterbf3.xml')
#    mcfg.setXml("""\
#        <configuration plugin="weaponlimiterbf3">
# 
#            <settings name="commands">
#                <set name="weaponlimiter">0</set>
#            </settings>
# 
#            <settings name="otherstuff">
#                <set name="helloworld_text">hello world :)</set>
#            </settings>
# 
#        </configuration>
#    """)

    myplugin = Weaponlimiterbf3Plugin(fakeConsole, mcfg)
    myplugin.onStartup()
    time.sleep(2)
    assert game.mapName == 'map3'

    #def testCommand():
    #    superadmin.connects(0)
    #    superadmin.says('!weaponlimiter')

#	testCommand()
    superadmin.connects(cid=0)
    superadmin.says('!weaponlimiter')

