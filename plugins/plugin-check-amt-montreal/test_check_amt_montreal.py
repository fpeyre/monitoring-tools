# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>

import check_amt_montreal
from check_amt_montreal import Plugin

from shinkenplugins import TestPlugin

class Test(TestPlugin):
    def test_version(self):
        args = ['-v']
        self.execute(Plugin, args, 3,
                     'version ' + Plugin.VERSION)

    def test_help(self):
        args = ['-h']
        self.execute(Plugin, args, 3,
                     'Usage:')

    # Add your tests here!
    # They should use
    # self.execute(Plugin,
    #              ['your', 'list', 'of', 'arguments'],
    #              expected_return_value,
    #              'regex to check against the output')

    def test_plugin(self):
        # TODO: manage our token, and get real data
        def get_data(self, _):
            with open('Alert.pb') as f:
                data = f.read()
            return data
        
        # monkey patch
        Plugin.get_feed = get_data
        
        args = ['-U', 'bacon', '-t', 'eggs', '-w', '1', '-c', '3']
        self.execute(Plugin, args, 1, '^WARNING - 2 problems', debug=True)