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

import time
from datetime import datetime


class utils:

    @staticmethod
    def getDuration(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        if h > 0:
            return f'{h:d}:{m:02d}:{s:02d}', 'hours'
        elif m > 0:
            return f'{m:02d}:{s:02d}', 'minutes'
        else:
            return f'{s:02d}', 'seconds'

    @staticmethod
    def getDateTime(strDateTime, strFormat):
        return datetime(*(time.strptime(strDateTime, strFormat)[0:6]))

    @staticmethod
    def datetimeToString(dt, dstFormat):
        return dt.strftime(dstFormat)

    @staticmethod
    def convertDateTime(strDateTime, srcFormat, dstFormat):

        try:
            dt = utils.getDateTime(strDateTime, srcFormat)
            if dt is not None:
                return dt.strftime(dstFormat)

        except ValueError:
            return None
