WeaponLimiterBF3 plugin for Big Brother Bot
===========================================
This plugin is for the [B3 Bot](http://www.bigbrotherbot.net/).
It allows to ban weapons in Battlefield 3.

### Features
- Allows to ban weapons per map and gametype
- penalized players

Usage
-----

### Installation
1. Copy the file [extplugins/weaponlimiterbf3.py](extplugins/weaponlimiterbf3.py) into your `b3/extplugins` folder and
[extplugins/conf/plugin_weaponlimiterbf3.ini](extplugins/conf/plugin_weaponlimiterbf3.ini) into your `b3/conf` folder

2. Add the following line in your b3.xml file (below the other plugin lines)
```xml
<plugin name="weaponlimiterbf3" config="@conf/plugin_weaponlimiterbf3.ini"/>
```

### Configuration
The configuration is made in [extplugins/conf/plugin_weaponlimiterbf3.ini](extplugins/conf/plugin_weaponlimiterbf3.ini).

A detailed description of all the options will be add soon on 1.0 release.

### Commands in game
* ```!weaponlimits``` show the current blacklisted/whitelisted weapons

* ```!weaponlimiter``` (alias !wpl) show the status
* ```!weaponlimiter <on | off>``` enable/disable the Limiter

If you use whitelist mode, then add 'Death' to the list!

Notes
-----
Note [EA's ROH](https://help.ea.com/article/battlefield-rules-of-conduct) if you want to use the plugin on ranked servers!
Weapons are not restricted by this Plugin. The Players can select and use them. But he must live with the consequences.
I have no closures due to this plugin known. But be warned!

Contributing
------------
* Fork it
* Test it
* Visit [our Battlefield3 Server](http://battlelog.battlefield.com/bf3/servers/show/11bdda3f-bb8b-4abb-92de-55f0b3ada7d7/)

Support
-------
Not realy. Watch to http://forum.bigbrotherbot.net/bf3b3-beta-board/weaponlimiter-plugin/

Thanks
------
* [courgette](https://github.com/courgette) and the B3 project for code samples
