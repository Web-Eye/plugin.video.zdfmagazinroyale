# -*- coding: utf-8 -*-
# Copyright 2022 WebEye
#
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
#

import os
import xbmcaddon


class Addon(xbmcaddon.Addon):

    def __init__(self, _id):
        xbmcaddon.Addon.__init__(self, _id)
        self._debug = os.getenv('kodi_debug') is not None

    def getAddonInfo(self, name):
        if not self._debug:
            return xbmcaddon.Addon.getAddonInfo(self, name)
        else:
            if name == 'name':
                return 'Hart aber Fair'
            elif name == 'icon':
                return None

    def getSetting(self, name):
        if not self._debug:
            return xbmcaddon.Addon.getSetting(self, name)
        else:
            return {
                'quality': '5',
                'suppress_signLanguage': 'true',
                'suppress_duration': '0',
                'page_itemCount': '20',
                'skip_itemPage': 'true',
                'database_enabled': 'true',
                'db_host': 'fsnas01',
                'db_port': '3306',
                'db_username': 'kodi',
                'db_password': 'kodi'
            }[name]
