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

import importlib
import logging
import pkgutil

_logger = logging.getLogger(__name__)
_PLUGINS = {}


def register_property(func):
    """
    Decorator to register a function as a new property for SUSECloudImageName
    class.
    """

    _logger.debug("Registering plugin property: %s", func.__name__)
    if func.__name__ in _PLUGINS:
        _logger.warning(
            "Plugin property %s is already registered. Overwriting.",
            func.__name__
        )
    _PLUGINS[func.__name__] = property(func)
    return func


def load_plugins(target_class):
    """
    Discover and load all plugins included in the plugin directory,
    attaching them to the target_class provided.
    """
    from . import plugins

    for _, name, _ in pkgutil.walk_packages(
        plugins.__path__,
        plugins.__name__ + '.'
    ):
        try:
            importlib.import_module(name)
        except Exception as e:
            _logger.error("Failed to load plugin module %s: %s", name, e)

    for name, prop in _PLUGINS.items():
        if hasattr(target_class, name):
            _logger.warning(
                "Cannot add plugin property '%s': attribute already exists"
                " on %s.",
                name, target_class.__name__
            )
        else:
            _logger.debug(
                "Attaching property '%s' to %s",
                name, target_class.__name__
            )
            setattr(target_class, name, prop)
