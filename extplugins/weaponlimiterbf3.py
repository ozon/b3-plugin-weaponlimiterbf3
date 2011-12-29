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
import b3.cron

__version__ = '0.1'
__author__ = 'ozon'


class Weaponlimiterbf3Plugin(b3.plugin.Plugin):
    _adminPlugin = None
    weapon_limiter_is_active = None
    _cronTab = None

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
        """ Initialize plugin settings """
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
        # register our command
        self.register_commands()
        # disable WeaponLimiter per default
        self.weapon_limiter_is_active = False
        # register Events
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        # load punisher settings
        self._punisher_settings = self.load_punisherConfig()
        # setup own variable to get crontab status
        self.weaponlimiter_cron_is_set = False
        


    def onEvent(self, event):
        """ Handle CLIENT_KILL and GAME_ROUND_START events """
        if event.type == b3.events.EVT_CLIENT_KILL and self.weapon_limiter_is_active:
            try:
                killer = event.client
                weapon = event.data[1]
                if weapon in self.forbidden_weapons:
                    self.debug('%s in pattern detected' % weapon)
                    
                    self.punish_player(self, event)
                    ##or self._adminPlugin.warnClient(killer, _wmsg, None, True, '', 0)
                    ##no outout msg## killer.warn('1h', _wmsg, None, None, '')
                    #self._adminPlugin.warnClient(killer.id, '', True, False, _wmsg, 1)
                    #if self.kill_killer == 1:
                    #   kill.
            except IndexError:
                pass

        if event.type == b3.events.EVT_GAME_ROUND_START and self.weapon_limiter_is_active:
            try:
                self.configure_weaponlimiter()
            except IndexError:
                pass

    
    # configure limiter per map
    def configure_weaponlimiter(self):
        """ Load weaponlimiter Configuration per map/gametype """
        if self.weapon_limiter_is_active:
            _current_map = self.console.game.mapName
            _current_gameType = self.console.game.gameType
            self.debug('Current Map/gameType: %s/%s' % (_current_map, _current_gameType))
            
            if self.config.has_section(_current_map) and _current_gameType in self.get_cfg_value_list(_current_map, 'gametype'):
                self.debug('Configure WeaponLimiter for %s/%s' % (_current_map, _current_gameType))
                self.forbidden_weapons = self.get_cfg_value_list(_current_map, 'weapons')
                self.console.say(self.getMessage('weaponlimiter_enabled', ', '.join(self.forbidden_weapons)))
                self.setup_crontab()
            else:
                self.debug('No configuration found for %s/%s' % (_current_map, _current_gameType))
                self.disable_weaponlimiter()


    # punish player
    def punish_player(self, event, data=None, client=None):
        """ Punish player """
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
            

    def disable_weaponlimiter(self):
        """ Disable weaponlimiter activity """
        self.forbidden_weapons = []
        if self.weapon_limiter_is_active:
            self.console.say(self._weaponlimiter_disabled_msg)
            
        self.weapon_limiter_is_active = False
        #remove crontab
        if self.weaponlimiter_cron_is_set:
            self.console.cron - self._cronTab
            self.weaponlimiter_cron_is_set = False

    def notice_forbidden_weapons(self):
        self.console.say(self.getMessage('notice_message', ', '.join(self.forbidden_weapons)))

    def setup_crontab(self):
        notify_every_min = self.config.getint('settings', 'notice_message_cron')
        self._cronTab = b3.cron.PluginCronTab(self, self.notice_forbidden_weapons, minute='*/%s' % notify_every_min)
        if self.weaponlimiter_cron_is_set:
            self.debug('cronTab is set - skipping')
        else:
            self.console.cron + self._cronTab
            self.weaponlimiter_cron_is_set = True

    def cmd_weaponlimiter(self, data, client, cmd=None):
        """ Handle Plugin commands """
        if client:            
            if not data:
                status_msg = ''
                if self.weapon_limiter_is_active:
                    status_msg = 'WeaponLimiter is active!'
                else:
                    status_msg = 'WeaponLimiter is disabled!'
                client.message(status_msg)
            else:
                if data not in ('on', 'off', 'pause'):
                    client.message("Invalid parameter. Expecting one of : 'on', 'off', 'pause'")
                elif data == 'on':
                    if self.weapon_limiter_is_active:
                        client.message('WeaponLimiter is allready active.')
                    else:
                        self.weapon_limiter_is_active = True
                        self.configure_weaponlimiter()
                elif data == 'off':
                    self.disable_weaponlimiter()
                    



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
 
    def register_commands(self):
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
    superadmin.setvar('weaponlimiterbf3', 'test','blub')
    print(dir(superadmin))
    print(superadmin.var('weaponlimiterbf3','test'))
    superadmin.says('!weaponlimiter')

