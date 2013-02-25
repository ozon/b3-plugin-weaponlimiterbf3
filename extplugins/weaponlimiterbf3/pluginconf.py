# -*- coding: utf-8 -*-

# PluginConfig Helper for BigBrotherBot(B3)
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


from ConfigParser import NoOptionError


class PluginConfig(object):
    _plugin = None

    def __init__(self, plugin):
        self._plugin = plugin

    def load_settings(self, default_settings, section, to_settings=None):
        """Load settings from plugin config into settings.

        :param to_settings: If given, load settings into given obj. If not, set _section as name
        :param default_settings: dict with default settings
        :param section: section from user plugin config file
        """

        def _get_option(optiontype, k, v):
            _get_config_obj = getattr(self._plugin.config, 'get' + optiontype)
            try:
                _setting = _get_config_obj(section, k)
                self._plugin.debug('Set %s to %s(%s) from %s' % (k, optiontype, v, self._plugin.config.fileName))
            except NoOptionError, err:
                _setting = default_settings[k]
                self._plugin.warning('%s ist not set in section %s. Set %s to %s(%s) from DEFAULS' % (
                    err.option, err.section, k, optiontype, v))

            return _setting

        def _get_list(k, v):
            _setting = [x.strip() for x in self._plugin.config.get(section, k).split(',')]

            # check list vs defaults
            if len(default_settings) <= 0:
                for i in _setting:
                    if i not in default_settings:
                        self._plugin.error('%s in %s is not a valied' % (i, section))

            return _setting

        if self._plugin.config.has_section(section):
            #if to_settings:
            settings = to_settings
            #else:
            #    settings = getattr(self, '_' + section)

            for k, v in default_settings.items():
                if isinstance(v, bool):
                    settings[k] = _get_option('boolean', k, v)
                elif isinstance(v, int):
                    settings[k] = _get_option('int', k, v)
                elif isinstance(v, str):
                    settings[k] = _get_option('', k, v)
                elif isinstance(v, tuple):
                    pass
                elif isinstance(v, list):
                    settings[k] = _get_list(k, v)
        else:
            self._plugin.error('Section %s dosnt exists!' % section)
            # ToDO: use default settings
