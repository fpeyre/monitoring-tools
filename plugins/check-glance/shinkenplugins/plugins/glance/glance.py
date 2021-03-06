#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Keystone monitoring script for Nagios
#
# Copyright (C) 2014 Savoir-faire Linux Inc.
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Florian Lambert <florian.lambert@enovance.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from shinkenplugins.old import BasePlugin
from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

from keystoneclient.v2_0 import client as keystone_client
from glanceclient import client as glance_client

import datetime


class Plugin(BasePlugin):
    NAME = 'check-keystone'
    VERSION = '0.1'
    DESCRIPTION = 'check keystone'
    AUTHOR = 'Alexandre Viau'
    EMAIL = 'alexandre.viau@savoirfairelinux.com'

    ARGS = [
        # Can't touch this:
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
        # Add your plugin arguments here:
        # ('short', 'long', 'description', 'does it expect a value?')

        # OpenStack Auth
        ('U', 'auth_url', 'Keystone URL', True),
        ('u', 'username', 'username to use for authentication', True),
        ('p', 'password', 'password to use for authentication', True),
        ('t', 'tenant', 'tenant name to use for authentication', True),
        ('e', 'endpoint', 'the glance endpoint', True),
        ('H', 'host', 'the glance host', True),

        # Options
        ('c', 'req_count', "minimum number of images in glance", True),

        ('c', 'req_images',
         "comma separated name of images that must be available", True),
    ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.

        if not args.get('help') and not args.get('version'):
            for arg in [
                'auth_url',
                'username',
                'password',
                'tenant',
                'endpoint',
            ]:
                if arg not in args.keys():
                    return False, 'the argument %s must be present' % arg

            # Turn req_images into a list
            if args.get('req_images'):
                args['req_images'] = args['req_images'].split(',')

            # Turn req_count into an int
            if args.get('req_count'):
                args['req_count'] = int(args['req_count'])

        return True, None

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)
        perfdata = []

        try:
            # Get a keystone token
            keystone = keystone_client.Client(
                username=args['username'],
                tenant_name=args['tenant'],
                password=args['password'],
                auth_url=args['auth_url'],
            )

            # Auth with glance
            start_time = datetime.datetime.now()
            client = glance_client.Client(
                auth_url=args['auth_url'],
                username=args['username'],
                tenant=args['tenant'],
                endpoint=args['endpoint'],
                host=args.get('host'),
                token=keystone.auth_token,
            )
            end_time = datetime.datetime.now()
            perfdata.append(
                PerfData(
                    'auth_time',
                    ((end_time - start_time).total_seconds()/1000),
                    min_='0',
                    unit='ms'
                )
            )
        except Exception as e:
            self.exit(STATES.UNKNOWN, str(e))

        # Get the images
        images = [image for image in client.images.list()]

        # Get the image count
        image_count = len(images)
        perfdata.append(
            PerfData(
                'image_count',
                image_count,
                min_=(args.get('req_count'))
            )
        )

        # Check the count of images
        if args.get('req_count') and image_count < args.get('req_count'):
            self.exit(
                STATES.CRITICAL,
                'Not enough images (%s < %s)' % (image_count, args.get('req_count')),
                *perfdata
            )

        # Check the required images
        missing_images = []
        if args.get('req_images'):
            for image in args.get('req_images'):
                if not next(client.images.list(**{"filters": {"name": image}}), None):
                        missing_images.append(image)
            if len(missing_images) > 0:
                self.exit(
                    STATES.CRITICAL,
                    'Images: %s are missing' % ' '.join(missing_images),
                    *perfdata
                )

        self.exit(
            STATES.OK,
            'OK - %s images found' % image_count,
            *perfdata
        )


def main(argv=None):
    Plugin(argv)


if __name__ == '__main__':
    main()
