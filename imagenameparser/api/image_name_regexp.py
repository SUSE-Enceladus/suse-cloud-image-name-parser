# Copyright (c) 2022 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Provides the ``ImageNameRegexp`` API class"""

import logging
import re

_logger = logging.getLogger(__name__)


class ImageNameRegexp:
    """Manages the contruction of a Regular Expression that can be used to
    match valid pint image names, and extract the relevant content from
    them as named fields in the returned match object's ``groupdict()``.
    """

    uuid_prefix = r'(?:(?P<uuid_prefix>[0-9a-fA-F]*)__)?'
    basename_pre = r'(?P<base_name>'
    basename_post = r')'
    product_pre = r'(?P<product>'
    product_post = r')'
    prodbase_pre = r'(?P<prodbase>'
    prodbase_post = r')'
    suffix_pre = r'(?P<suffix>'
    suffix_post = r')'
    sle_server = r'(?:(?:suse-)?(?P<sle_server>sles))'
    sles_serv = r'(?:(?:SUSE-)?(?P<sles_serv>SUSE-Linux-Enterprise-Server))'
    sle = r'(?:(?:suse-)?(?P<sle>sle))'
    opensuse_leap = r'(?:(?:suse-)?(?P<leap>open(suse|SUSE)-[l|L]eap))'
    opensuse = r'(?:(?:suse-)?(?P<opensuse>open(suse|SUSE)))'
    cap = r'(?:(?:suse-)?(?P<cap>cap-deploy))'
    caasp = r'(?:(?:suse-)?(?P<caasp>caasp))'
    suse_manager = r'(?P<suse_manager>(suse-manager|manager))'
    suse_manager_server = r'(?P<suse_manager_server>suse-manager-server)'
    suse_manager_proxy = r'(?P<suse_manager_proxy>suse-manager-proxy)'
    lasso = r'(?P<lasso>suse-rancher-setup)'
    product_version = (r'(' +
                       r'(?:-?(?P<major_version>[0-9]+))?' +
                       r'(?:[.-](?P<minor_version>(?:[sS][pP][1-9]|[0-9])))?' +
                       r')')
    sapcal = (r'(?:-(?P<sapcal>sapcal|SAP-CAL|sap-cal|rightscale|'
              'hvm|pv|hvm-bld485|sap-pv|sap-hvm))?')
    azure_hosted = r'(?:-azure-(?P<azure_hosted>li|vli|guest))?'
    manager = r'(?:-manager-(?P<manager>(server-2-1|proxy-2-1)))?'
    sap1 = r'(?:-(?P<sap1>sap))?'
    sap2 = r'(?:-(?P<sap2>(?(sapcal)|sap)))?'
    basic = r'(?:-(?P<basic>(basic|admin|cluster)))?'
    suma_type = (r'(?(suse_manager)' +
                 r'(?:-(?P<suma_type>proxy|server))' +
                 r'|)')
    byos = r'(?:-(?P<byos>byos))?'
    chost = r'(?:-(?P<chost>chost))?'
    micro = r'(?:-(?P<micro>micro))?'
    hpc1 = r'(?:-(?P<hpc1>hpc))?'
    hpc2 = r'(?:-(?P<hpc2>hpc))?'
    version = r'(?:-v(?P<version>[0-9]{3}))?'
    priority = r'(?:-(?P<priority>(priority|Prio)))?'
    standard = r'(?:-(?P<standard>standard))?'
    datestmp = r'(?:-(?P<datestmp>[0-9]{8,9}))?'
    datestamp = r'(?:-v(?P<datestamp>[0-9]{8,9}))?'
    ver = (r'(?:-v(?P<ver>[0-9]+))?' +
           r'(?:[.-](?P<ver1>[0-9]{1,3}))?' +
           r'(?:[.-](?P<ver2>[0-9]{0,3}))?')
    ecs = r'(?:-(?P<ecs>ecs))?'
    gen_id = (r'(?:-(?P<gen_id>(?:(?P=major_version)' +
              r'(?:-(?P=minor_version))?-)?gen[0-9]))?')
    gen2 = r'(?:-(?P<gen2>gen[0-9]))?'
    gen3 = r'(?:[.-](?P<gen3>gen[0-9]))?'
    virt_type = r'(?:-(?P<virt_type>hvm|pv|hvm-mag|pv-mag))?'
    ssd = r'(?:-(?P<ssd>ssd))?'
    arch = r'(?:[.-](?P<arch>x86_64|x86-64|arm64|i386|x86_64_ssd))?'
    archver = (r'(?:-(?P<archver>[0-9]+))?' +
               r'(?:[.-](?P<archver1>[0-9]))?' +
               r'(?:[.-](?P<archver2>[0-9]{1,3}))?')
    build = (r'(?:-(?P<build>build[0-9]))?' +
             r'(?:[.-](?P<build1>[0-9]))?')

    @classmethod
    def matcher(cls):
        """Helper class method that constructs the required regexp
        pattern and returns the compiled result."""

        # Construct a regexp pattern that matches the base product
        # part of an image name, e.g. sles, suse-manager, opensuse,
        # including any optional 'suse-' prefix that may exist for
        # some cloud providers.
        prodbase_pattern = (cls.prodbase_pre +
                            cls.sle_server +
                            r'|' +
                            cls.sles_serv +
                            r'|' +
                            cls.sle +
                            r'|' +
                            cls.opensuse_leap +
                            r'|' +
                            cls.opensuse +
                            r'|' +
                            cls.suse_manager +
                            r'|' +
                            cls.suse_manager_server +
                            r'|' +
                            cls.suse_manager_proxy +
                            r'|' +
                            cls.cap +
                            r'|' +
                            cls.caasp +
                            r'|' +
                            cls.lasso +
                            r'|' +
                            cls.prodbase_post)

        # Construct a regexp pattern that matches the entrire product
        # identification part of the image name, before the product
        # version part, e.g. sles-sap or sles-hpc.
        prod_pattern = (cls.product_pre +
                        prodbase_pattern +
                        cls.hpc1 +
                        cls.sap1 +
                        cls.micro +
                        cls.product_post)

        # Contruct a pattern that matches the entire image basename,
        # i.e. the entire part that comes before the '-v{date}', but
        # excluding the Azure '<UUID>__' prefix, made up of the base
        # product, with any product flavour identifiers, followed by
        # the product version, followed by further possible flavour
        # and payment model identifiers.
        basename_pattern = (cls.basename_pre +
                            prod_pattern +
                            cls.product_version +
                            cls.suma_type +
                            cls.basic +
                            cls.sapcal +
                            cls.sap2 +
                            cls.chost +
                            cls.hpc2 +
                            cls.manager +
                            cls.azure_hosted +
                            cls.priority +
                            cls.standard +
                            cls.byos +
                            cls.basename_post)

        # Construct a pattern that matches the possible suffix
        # elements that can appear after the '-v{date}' in the
        # image name.
        suffix_pattern = (cls.suffix_pre +
                          cls.gen_id +
                          cls.ecs +
                          cls.virt_type +
                          cls.ssd +
                          cls.arch +
                          cls.gen2 +
                          cls.archver +
                          cls.build +
                          cls.suffix_post)
        # print(suffix_pattern)
        # Combine the above patterns with the uuid prefix and
        # datestamp patterns to contruct a pattern that matches
        # the entire image name.
        pattern = (r'^' +
                   cls.uuid_prefix +
                   basename_pattern +
                   cls.gen3 +
                   cls.datestmp +
                   cls.datestamp +
                   cls.ver +
                   cls.version +
                   suffix_pattern +
                   r'$')
        return re.compile(pattern)

    def __init__(self):
        """Call ``self.matcher()`` class helper method to return a
        compiled RE matcher instance that we cache for subsequent
        re-use."""
        self._matcher = self.matcher()

    def match(self, image_name):
        """Return the result of attempting a ``fullmatch()`` against
        the provided ``image_name`` using the compler matcher."""
        return self._matcher.fullmatch(image_name)
