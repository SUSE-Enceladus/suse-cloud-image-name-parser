# This file serves as an example of how to create a plugin to extend the
# functionality of the SUSECloudImageName class.
#
# How the Plugin Mechanism Works:
#
# 1.  Discovery: Any Python file placed in the `plugins` directory is
#     automatically discovered by the plugin loader when a
#     `SUSECloudImageName` object is instantiated for the first time.
#
# 2.  Registration: The `@register_property` decorator marks a function as a
#     new property. The name of the decorated function becomes the name of
#     the property on the `SUSECloudImageName` class.
#
# 3.  Implementation: The decorated function must accept one argument, which
#     will be an instance of the `SUSECloudImageName` class.
#
# 4.  Usage: Once loaded, the new property can be accessed on any
#     `SUSECloudImageName` instance just like one of the built-in properties.


from suse_cloud_image_name_parser.plugins_loader import register_property


@register_property
def plugins_working(image):
    """Checks if the plugin mechanism is working properly"""
    return True
