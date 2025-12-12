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
