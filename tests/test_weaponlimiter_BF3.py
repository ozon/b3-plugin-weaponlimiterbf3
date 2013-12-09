# -*- encoding: utf-8 -*-

# add extplugins to the Python sys.path
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../extplugins'))

from unittest import TestCase
from mock import patch, call, Mock
from mockito import when, verify
from b3.fake import FakeConsole, FakeClient
from b3.config import XmlConfigParser, CfgConfigParser
from weaponlimiterbf3 import Weaponlimiterbf3Plugin


class PingkickerPluginTest(TestCase):

    def tearDown(self):
        if hasattr(self, "parser"):
            del self.parser.clients
            self.parser.working = False

    def setUp(self):
        # create a B3 FakeConsole
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(r"""<configuration/>""")
        self.console = FakeConsole(self.parser_conf)

        # create our plugin instance
        self.plugin_conf = CfgConfigParser()
        self.p = Weaponlimiterbf3Plugin(self.console, self.plugin_conf)

        # initialise the plugin
        self.plugin_conf.loadFromString(r'''
[commands]
weaponlimiter-wpl: 60
weaponlimits: guest
noobkill: 20

[settings]
change servermessage: yes
self_kill_counter: 1
config_strategy: mapname
display_extra_msg: message
yell_duration: 10

[punisher]
kill_player: no
warn_player: yes

[messages]
servermessage: This game uses weapons limits. Use !weaponlimits to show forbidden weapons.
weaponlimiter_enabled: WeaponLimiter for that round activated!
weaponlimiter_disabled: Weaponlimiter disabled! All Weapons allowed.
warn_message: You used a forbidden weapon! ^7!forbidden_weapons show the list of forbidden weapons
forbidden_message: Forbidden Weapons are: %s
allowed_message: Allowed Weapons: %s
extra_warning_message: You have %(victim)s killed with a %(weapon)s. This weapon is forbidden!

[XP2_Skybar]
banned weapons: SMAW, M320, RPG-7, USAS-12
gametype: Domination0
weapons: Weapons/Gadgets/C4/C4,870MCS,DAO-12,jackhammer,M1014,M26Mass,Siaga20k,SPAS-12,USAS-12
''')

        # fake BF3 game
        self.console.game.gameName = 'bf3'
        self.console.game.gameType = 'Domination0'
        self.console.game._mapName = 'XP2_Skybar'
        # startup plugin
        self.p.onLoadConfig()
        self.p.onStartup()
        # enable
        self.p._wpl_is_active = True
        # prepare a few players
        self.joe = FakeClient(self.console, name="Joe", exactName="Joe", guid="zaerezarezar", groupBits=1)
        self.simon = FakeClient(self.console, name="Simon", exactName="Simon", guid="qsdfdsqfdsqf", groupBits=0)
        self.admin = FakeClient(self.console, name="Level-40-Admin", exactName="Level-40-Admin", guid="875sasda", groupBits=16,)
        self.superadmin = FakeClient(self.console, name="God", exactName="God", guid="f4qfer654r", groupBits=128)

    def test_warning_on_forbidden_kill(self):
        self.joe.connects('joe')
        self.simon.connects('simon')
        #clear message history
        self.joe.message_history = []
        self.simon.message_history = []
        # player simon kills joe with the M1014
        self.simon.kills(self.joe, 'M1014')

        self.assertEqual('You have Joe killed with a M1014. This weapon is forbidden!', self.simon.message_history[0])
        #self.assertEqual(self.p._messages['reminder_ping_warning'], self.simon.message_history[1])

    def test_punish_on_forbidden_kill(self):
        pass

    def test_cmd_weaponlimits(self):
        pass