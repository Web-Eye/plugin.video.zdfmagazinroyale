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

import mysql.connector
from libs.database.datalayer.dl_items import DL_items


class DBAPI:

    def __init__(self, db_config, tag):
        self._cnx = None
        self._teaserCount = 0
        self._pageNumber = 0
        self._pageSize = 20
        self._posterWidth = 480
        self._quality_id = 3

        if tag is not None:
            if 'pageNumber' in tag:
                self._pageNumber = tag.get('pageNumber')
            if 'pageSize' in tag:
                self._pageSize = tag.get('pageSize')
            if 'posterWidth' in tag:
                self._posterWidth = tag.get('posterWidth')
            if 'quality' in tag:
                self._quality_id = tag.get('quality')

        self._cnx = mysql.connector.Connect(**db_config)

    def __del__(self):
        if self._cnx is not None:
            self._cnx.close()

    def getTeaser(self):
        query = {
            'project': 'ZDFMAGAZINROYALE',
            'quality': self._quality_id,
            'page': int(self._pageNumber) + 1,
            'pageSize': self._pageSize,
            'posterWidth': self._posterWidth
        }

        return DL_items.getItemView(self._cnx, query)

    def getPagination(self):
        query = {
            'project': 'ZDFMAGAZINROYALE',
            'quality': self._quality_id
        }

        item_count = DL_items.getCount(self._cnx, query)

        return {
            'pageNumber': self._pageNumber,
            'pageSize': self._pageSize,
            'totalElements': item_count
        }
