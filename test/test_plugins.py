# Copyright (c) 2025 SUSE LLC
#
# This file is part of suse-cloud-image-name-parser
#
# image-name is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or # (at your option) any later version.
#
# image-name is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with image-name.
# If not, see <http://www.gnu.org/licenses/>.

import unittest

from suse_cloud_image_name_parser.suse_cloud_image_name import (
    SUSECloudImageName
)


class TestPlugins(unittest.TestCase):
    """
    Test that the plugin loading mechanism works as expected.
    """

    def test_plugins_are_loaded(self):
        """
        Verify that plugins are loaded and their properties are available
        on SUSECloudImageName instances.
        """
        # A valid image name to instantiate the class
        image_name = "suse-sles-15-sp3-byos-v20210101-x86_64"
        image = SUSECloudImageName(image_name)

        # Check for the 'plugins_working' property from example_plugin.py
        self.assertTrue(hasattr(image, 'plugins_working'))
        self.assertTrue(image.plugins_working)
