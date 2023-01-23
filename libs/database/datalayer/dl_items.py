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

from libs.database.database_core import databaseCore
from libs.utils import utils


class DL_items:

    @staticmethod
    def getItemView(cnx, query):
        items = []
        innerWhereClause = 'project = %s'
        parameter = (query['project'], )

        if query['quality'] == 5:
            innerWhereClause += ' AND best_quality = 1'
        elif query['quality'] == 3:
            innerWhereClause += ' AND quality = %s'
            parameter += ('veryhigh',)
        elif query['quality'] == 2:
            innerWhereClause += ' AND quality = %s'
            parameter += ('high',)
        elif query['quality'] == 1:
            innerWhereClause += ' AND quality = %s'
            parameter += ('med',)
        elif query['quality'] == 0:
            innerWhereClause += ' AND quality = %s'
            parameter += ('low',)

        minItem = (query['page'] - 1) * query['pageSize'] + 1
        maxItem = minItem + query['pageSize'] - 1
        parameter += (minItem, maxItem, )

        sQuery = f'    SELECT * FROM (' \
                 f'        SELECT ROW_NUMBER() OVER (' \
                 f'                              ORDER BY order_date DESC, order_id ASC, broadcastOn_date DESC' \
                 f'              ) AS rowNumber, viewItemLinks.title, viewItemLinks.plot, viewItemLinks.poster_url' \
                 f'              ,viewItemLinks.broadcastOn_date, viewItemLinks.availableTo_date' \
                 f'              ,viewItemLinks.duration, viewItemLinks.quality, viewItemLinks.hoster' \
                 f'              ,viewItemLinks.url' \
                 f'        FROM viewItemLinks' \
                 f'        WHERE {innerWhereClause}' \
                 f'    ) AS t' \
                 f'    WHERE t.rowNumber BETWEEN %s AND %s;'

        cursor = databaseCore.executeReader(cnx, sQuery, parameter)
        if cursor is not None:
            rows = cursor.fetchall()
            for row in rows:
                items.append({
                    'title': row[1],
                    'plot': row[2],
                    'poster': row[3].replace('{width}', str(query['posterWidth'])),
                    'broadcastedOn': utils.convertDateTime(str(row[4]), '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ'),
                    'availableTo': utils.convertDateTime(str(row[5]), '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%SZ'),
                    'duration': row[6],
                    'quality': row[7],
                    'hoster': row[8],
                    'url': row[9]
                })

            cursor.close()
        return items

    @staticmethod
    def getCount(cnx, query):
        whereClause = 'project = %s'
        parameter = (query['project'],)

        if query['quality'] == 5:
            whereClause += ' AND best_quality = 1'
        elif query['quality'] == 3:
            whereClause += ' AND quality = %s'
            parameter += ('veryhigh',)
        elif query['quality'] == 2:
            whereClause += ' AND quality = %s'
            parameter += ('high',)
        elif query['quality'] == 1:
            whereClause += ' AND quality = %s'
            parameter += ('med',)
        elif query['quality'] == 0:
            whereClause += ' AND quality = %s'
            parameter += ('low',)

        sQuery = f'SELECT COUNT(*) FROM viewItemLinks WHERE {whereClause};'

        return databaseCore.executeScalar(cnx, sQuery, parameter)
