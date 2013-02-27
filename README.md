WeaponLimiterBF3 plugin for Big Brother Bot
===========================================

What is it?
-----------
This plugin is for the [B3 Bot](http://www.bigbrotherbot.net/).
It allows to ban weapons in Battlefield 3.

Installation
------------
* copy the folder weaponlimiterbf3 into b3/extplugins
* copy conf/plugin_weaponlimiterbf3.ini into b3/extplugins/conf
* add `<plugin name="weaponlimiterbf3" config="@conf/extplugins/plugin_weaponlimiterbf3.ini"/>` in you main b3 config file
* modify plugin_weaponlimiterbf3.ini


Usage
-----
* ```!weaponlimits``` show the current blacklisted/whitelisted weapons

* ```!weaponlimiter``` (alias !wpl) show the status
* ```!weaponlimiter on``` enable the WeaponLimiter
* ```!weaponlimiter off``` disable the Limiter

If you use whitelist mode, then add 'Death' to the list!

Notes
-----
Note [EA's ROH](https://help.ea.com/article/battlefield-rules-of-conduct) if you want to use the plugin on ranked servers!
Weapons are not restricted by this Plugin. The Players can select and use them. But he must live with the consequences.
I have no closures due to this plugin known.
But be warned.

Contributing
------------

* Fork it.
* Test it
* Visit [our Battlefield3 Server](http://battlelog.battlefield.com/bf3/de/servers/show/b5e4367c-4196-4691-bcc6-56ae0b2c0238/) - This Plugin is on Metro Maps active 


Support
-------
Not realy. Watch to http://forum.bigbrotherbot.net/bf3b3-beta-board/weaponlimiter-plugin/

Thanks
------
* HarryGer1991, LunaticBfc  for testing in long nights
* [courgette](https://github.com/courgette) and the b3 project for code samples
