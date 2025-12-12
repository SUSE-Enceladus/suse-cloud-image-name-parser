# suse-cloud-image-name-parser
Parse Public Cloud image names that match the SUSE naming convention

API implementation to parse image names that match the SUSE Public Cloud image naming convention.

## Extending the class with Plugins

The parser's functionality can be extended with plugins. This allows you to add
 new custom properties to the SUSECloudImageName class without modifying the
 core library.

### How to Create a Plugin

1. Create a Python file: Add a new .py file inside the
   suse_cloud_image_name_parser/plugins/ directory. The plugin loader will
   automatically discover it when the SUSECloudImageName is instantiated.

2. Define a Property Function: Write a function that takes one argument: an
 instance of the SUSECloudImageName class. This function will contain the logic
  for your new property.

3. Register the Property: Decorate your function with the `@register_property`
 decorator from the `suse_cloud_image_name_parser/plugins_loader.py` file. The
  name of your function will become the name of the new property added to the
  class.

### Example Plugin

The plugin directory contains an example of a plugin file with a new property.

```python
from suse_cloud_image_name_parser.plugins_loader import register_property


@register_property
def plugins_working(image):
    """Checks if the plugin mechanism is working properly"""
    return True
```

Then you will be able to access that property as follows:

```python
from suse_cloud_image_name_parser import SUSECloudImageName

image = SUSECloudImageName("suse-sles-15-sp3-byos-v20210101-x86_64")
assert image.plugins_working is True
```
