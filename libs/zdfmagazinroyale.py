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
import json
import sys
import urllib
import urllib.parse
import mysql.connector

from libs.database.database_api import DBAPI
from libs.kodion.addon import Addon
from libs.kodion.gui_manager import *
from libs.kodion.utils import Utils as kodionUtils
from libs.utils import utils
from libs.translations import *


class ZDFMagazinRoyale:

    def __init__(self):

        # -- Constants ----------------------------------------------
        self._ADDON_ID = 'plugin.video.zdfmagazinroyale'

        # ADDONTHUMB = utils.translatePath('special://home/addons/' + ADDON_ID + '/resources/assets/icon.png')
        width = getScreenWidth()
        if width >= 2160:
            fanart = f'special://home/addons/{self._ADDON_ID}/resources/assets/2160p/fanart.jpg'
        elif width >= 1080:
            fanart = f'special://home/addons/{self._ADDON_ID}/resources/assets/1080p/fanart.jpg'
        else:
            fanart = f'special://home/addons/{self._ADDON_ID}/resources/assets/720p/fanart.jpg'

        self._FANART = kodionUtils.translatePath(fanart)
        self._POSTERWIDTH = int(width/3)
        self._DEFAULT_IMAGE_URL = ''

        self._guiManager = GuiManager(sys.argv[1], self._ADDON_ID, self._DEFAULT_IMAGE_URL, self._FANART)
        self._guiManager.setContent('movies')

        # -- Settings -----------------------------------------------
        addon = Addon(self._ADDON_ID)
        self._addon_name = addon.getAddonInfo('name')
        self._addon_icon = addon.getAddonInfo('icon')
        self._t = Translations(addon)
        self._quality_id = int(addon.getSetting('quality'))
        self._PAGESIZE = int(addon.getSetting('page_itemCount'))
        self._skip_itemPage = True
        self._db_enabled = True
        self._db_config = None
        if self._db_enabled:
            self._db_config = {
                'host': addon.getSetting('db_host'),
                'port': int(addon.getSetting('db_port')),
                'user': addon.getSetting('db_username'),
                'password': addon.getSetting('db_password'),
                'database': 'KodiWebGrabber_Test'
            }
            self._skip_itemPage = True

    def refreshItem(self, url, pageNumber=None):
        self._guiManager.setToastNotification(self._addon_name, 'NOT IMPLEMENTED, yet! ;)', image=self._addon_icon)

    # def setItemView(self, url, pageNumber=None):
    #
    #     tag = {
    #         'posterWidth': self._POSTERWIDTH,
    #         'quality': self._quality_id
    #     }
    #
    #     API = ARDMediathekAPI(url, tag)
    #     item = API.getItem()
    #     if item is not None:
    #         title = item['title']
    #         broadcastedOn = utils.convertDateTime(item['broadcastedOn'], '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d')
    #
    #         infoLabels = {
    #             'Title': title,
    #             'Plot': item['plot'],
    #             'Date': broadcastedOn,
    #             'Aired': broadcastedOn,
    #             'Duration': item['duration']
    #         }
    #
    #         self._guiManager.addItem(title=title, url=item['url'], poster=item['poster'], _type='video',
    #                                  infoLabels=infoLabels)


    def addItemPage(self, teaser):
        title = teaser['title']
        duration, unit = utils.getDuration(int(teaser['duration']))
        duration = {
            'hours': duration + f' {self._t.getString(HOURS)}',
            'minutes': duration + f' {self._t.getString(MINUTES)}',
            'seconds': duration + f' {self._t.getString(SECONDS)}',
        }[unit]

        broadcastedOn = utils.convertDateTime(teaser['broadcastedOn'], '%Y-%m-%dT%H:%M:%SZ', '%d.%m.%Y, %H:%M:%S')
        availableTo = utils.convertDateTime(teaser['availableTo'], '%Y-%m-%dT%H:%M:%SZ', '%d.%m.%Y, %H:%M:%S')

        plot = f'[B]{title}[/B]\n\n[B]{self._t.getString(DURATION)}[/B]: {duration}\n' \
               f'[B]{self._t.getString(BROADCASTEDON)}[/B]: {broadcastedOn}\n' \
               f'[B]{self._t.getString(AVAILABLETO)}[/B]: {availableTo} '

        broadcastedOn = utils.convertDateTime(teaser['broadcastedOn'], '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d')

        infoLabels = {
            'Title': title,
            'Plot': str(plot),
            'Date': broadcastedOn,
            'Aired': broadcastedOn,
            'Duration': teaser['duration']
        }

        self._guiManager.addDirectory(title=title, poster=teaser['poster'], _type='Video',
                                      infoLabels=infoLabels, args=self.buildArgs('item', teaser['url']))

    def addClip(self, teaser):
        if not self._db_enabled:
            url = teaser['url']
            # self.setItemView(url, None)

        else:
            title = teaser['title']

            broadcastedOn = utils.convertDateTime(teaser['broadcastedOn'], '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d')

            infoLabels = {
                'Title': title,
                'Plot': teaser['plot'],
                'Date': broadcastedOn,
                'Aired': broadcastedOn,
                'Duration': teaser['duration']
            }

            contextMenu = None
            if self._db_enabled:
                contextMenu = [(self._t.getString(REFRESH), f'RunPlugin(plugin://{self._ADDON_ID}/?method=refresh)', )]

            self._guiManager.addItem(title=title, url=teaser['url'], poster=teaser['poster'], _type='video',
                                     infoLabels=infoLabels, contextMenu=contextMenu)

    def setHomeView(self, pageNumber=None):
        if pageNumber is None:
            pageNumber = 0

        tag = {
            'quality': self._quality_id,
            'pageSize': self._PAGESIZE,
            'posterWidth': self._POSTERWIDTH,
            'pageNumber': pageNumber
        }

        if not self._db_enabled:
            # API = ARDMediathekAPI(url, tag)
            pass
        else:
            try:
                API = DBAPI(self._db_config, tag)
            except mysql.connector.Error as e:
                self._guiManager.setToastNotification(self._addon_name, e.msg, image=self._addon_icon)
                return

        teasers = API.getTeaser()
        pagination = API.getPagination()

        if teasers is not None:
            for teaser in teasers:
                if self._db_enabled:
                    self.addClip(teaser)

            if pagination is not None:
                pageNumber = int(pagination['pageNumber'])
                pageSize = int(pagination['pageSize'])
                totalElements = int(pagination['totalElements'])

                if totalElements > ((pageNumber + 1) * pageSize):
                    strPageNumber = str(pageNumber + 2)
                    # tag = {
                    #     'pageNumber': pageNumber + 1,
                    #     'pageSize': self._PAGESIZE,
                    #     'posterWidth': self._POSTERWIDTH
                    # }
                    self._guiManager.addDirectory(title=f'Page {strPageNumber}',
                                                  args=self.buildArgs('home', pageNumber=pageNumber + 1))

    @staticmethod
    def get_query_args(s_args):
        args = urllib.parse.parse_qs(urllib.parse.urlparse(s_args).query)

        for key in args:
            args[key] = args[key][0]
        return args

    @staticmethod
    def buildArgs(method, pageNumber=None):

        item = {
            'method': method,
        }

        if pageNumber is not None:
            item['pageNumber'] = pageNumber

        return item

    def DoSome(self):

        args = self.get_query_args(sys.argv[2])
        if args is None or args.__len__() == 0:
            args = self.buildArgs(method='home')

        method = args.get('method')
        pageNumber = None
        if 'pageNumber' in args:
            pageNumber = args.get('pageNumber')

        {
            'home': self.setHomeView,
            'refresh': self.refreshItem
        }[method](pageNumber)

        # self._guiManager.addSortMethod(GuiManager.SORT_METHOD_NONE)
        # self._guiManager.addSortMethod(GuiManager.SORT_METHOD_DATE)
        self._guiManager.endOfDirectory()
