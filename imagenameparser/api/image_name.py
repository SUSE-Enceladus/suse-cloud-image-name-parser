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

"""Provides the ``ImageName`` API class"""

import logging

from imagenameparser.api.image_name_regexp import ImageNameRegexp
from imagenameparser.errors import BadRegexMatchError, InvalidFrameworkError

_logger = logging.getLogger(__name__)


class ImageName:  # pylint: disable=R0904
    """
    Parse an image name.

    ``framework`` should be a valid cloud provider framework name, such
    as ``ec2`` or ``azure``.

    ``name`` should be a valid image name, such as any of the image names
    reported by ``pint``.

    """

    def __init__(self, framework, name):
        self._framework = framework
        self._image_name = name
        self._image_info = None

        self._check_framework()
        self._extract_image_info()

    def _check_framework(self):
        """Check if framework is valid cloud provider framework name

        Raises:
            FrameworkError: If the framework name is missing or Invalid
        """

        if self._framework is None:
            raise InvalidFrameworkError("framework is required", "")
        if self._framework not in (
            'ec2',
            'azure',
            'gce',
            'oci',
            'aliyun'
        ):
            raise InvalidFrameworkError("Invalid framework", self._framework)

    def _extract_image_info(self):
        """Extract the required image details from the image name

        Raises:
            BadRegexMatchError: If the image name does not match the expected
                regex pattern
        """
        if self._image_info is None:
            matched = ImageNameRegexp().match(self._image_name)
            try:
                self._image_info = matched.groupdict()
            except AttributeError:
                raise BadRegexMatchError("Could not match regex for image: "
                                         + self._image_name) from None
            if self._framework in ("azure", "ec2") and \
                    self._image_info['sle_server'] is not None and \
                    self._image_info['azure_hosted'] is None:
                if self._image_info['prodbase'] != "suse-sles":
                    raise BadRegexMatchError(self._framework + " image "
                                             + self._image_name
                                             + " does not start with 'suse'")\
                        from None

            _logger.debug("Image match values for image %s are: %s",
                          self._image_name, self._image_info)

    @property
    def framework(self):
        """Get the framework"""
        return self._framework

    @property
    def is_azure(self):
        """Check if the framework is azure"""
        return self.framework == "azure"

    @property
    def is_ec2(self):
        """Check if framework is ec2"""
        return self.framework == "ec2"

    @property
    def is_gce(self):
        """Check if framework is gce"""
        return self.framework == "gce"

    @property
    def is_oci(self):
        """Check if framework is oci"""
        return self.framework == "oci"

    @property
    def is_aliyun(self):
        """Check if framework is aliyun"""
        return self.framework == "aliyun"

    @property
    def framework_name(self):
        """Get the framework"""
        if self.is_azure or self.is_aliyun:
            framework = self.framework.capitalize()
        else:
            framework = self.framework.upper()
        return framework

    @property
    def dash_framework(self):
        """Get '-framework'"""
        return f"-{self.framework_name}"

    @property
    def framework_dash(self):
        """Get 'framework-'"""
        return f"{self.framework_name}-"

    @property
    def image_name(self):
        """Get the image_name"""
        return self._image_name

    # Image architecture properties

    @property
    def arch(self):
        """Get the architecture if set, otherwise return a default value"""
        if self._image_info["arch"] in ("x86-64", None):
            return "x86_64"
        return self._image_info["arch"]

    @property
    def is_x86_64(self):
        """Check if image is x86_64"""
        return self.arch == "x86_64"

    @property
    def is_aarch64(self):
        """Check if image is aarch64"""
        return self.is_arm64

    @property
    def is_arm64(self):
        """Check if image is arm64"""
        return self.arch == "arm64"

    @property
    def is_amd64(self):
        """Check if image is amd64 (same as x86_64)"""
        return self.is_x86_64

    @property
    def cloud_arch(self):
        """Get the architecture"""
        if self.is_aarch64:
            return "aarch64"
        if self.is_x86_64:
            # arch may be None for some frameworks
            return "x86_64"
        return self.arch

    @property
    def dash_arch(self):
        """Get '-arch'"""
        if self.is_gce:
            return f"-{self.arch.replace('_', '-')}"
        return f"-{self.arch}"

    # General image properties

    @property
    def leap(self):
        """Get the value of the leap regex match"""
        return self._image_info['leap']

    @property
    def is_leap(self):
        """Check if 'leap' is set"""
        return self.leap is not None

    @property
    def opensuse(self):
        """Get the value of the opensuse regex match"""
        return self._image_info['opensuse']

    @property
    def is_opensuse(self):
        """Check if 'opensuse' is set"""
        return self.opensuse is not None

    @property
    def sle_server(self):
        """Get the value of the sle_server regex match"""
        return self._image_info['sle_server']

    @property
    def is_sle_server(self):
        """Check if 'sle_server' is set"""
        return self.sle_server is not None

    @property
    def sle(self):
        """Get the value of the sle regex match"""
        return self._image_info['sle']

    @property
    def is_sle(self):
        """Check if 'sle' is set"""
        return self.sle is not None

    @property
    def sles_serv(self):
        """Get the value of the SUSE-Linux-Enterprise-Server regex match"""
        return self._image_info['sles_serv']

    @property
    def is_sles_serv(self):
        """Check if 'SUSE-Linux_Enterprise-Server' is set"""
        return self.sles_serv is not None

    @property
    def cap(self):
        """Get the value of the cap regex match"""
        return self._image_info['cap']

    @property
    def is_cap(self):
        """Check if 'cap' is set"""
        return self.cap is not None

    @property
    def caasp(self):
        """Get the value of the caasp regex match"""
        return self._image_info['caasp']

    @property
    def is_caasp(self):
        """Check if 'caasp' is set"""
        return self.caasp is not None

    @property
    def sumaserver(self):
        """Get the value of the suma server regex match"""
        return self._image_info['suse_manager_server']

    @property
    def is_sumaserver(self):
        """Check if 'suma server' is set"""
        return self.sumaserver is not None

    @property
    def sumaproxy(self):
        """Get the value of the sums proxy regex match"""
        return self._image_info['suse_manager_proxy']

    @property
    def is_sumaproxy(self):
        """Check if 'suma proxy' is set"""
        return self.sumaproxy is not None

    @property
    def suma(self):
        """Get the value of the suma regex match"""
        return self._image_info['suse_manager']

    @property
    def lasso(self):
        """Get the value of the lasso regex match"""
        return self._image_info['lasso']

    @property
    def is_suma(self):
        """Check if 'suma' is set"""
        return self.suma is not None

    @property
    def suma_type(self):
        """Get the value of the suma_type regex match"""
        return self._image_info['suma_type']

    @property
    def suma_type_desc(self):
        """Get the suma type description"""
        if self.suma_type is None:
            return ""
        return self.suma_type.capitalize()

    @property
    def dash_suma_type(self):
        """Get '-suma_type'"""
        if self.suma_type is None:
            return ""
        return f"-{self.suma_type}"

    @property
    def is_lasso(self):
        """Check if 'lasso' is set"""
        return self.lasso is not None

    @property
    def hpc1(self):
        """Get the value of the hcp1 regex match"""
        return self._image_info['hpc1']

    @property
    def hpc2(self):
        """Get the value of the hpc2 regex match"""
        return self._image_info['hpc2']

    @property
    def is_hpc(self):
        """Check if 'hpc1' or 'hpc2' is set"""
        return (self.hpc1 is not None) or (self.hpc2 is not None)

    @property
    def dash_hpc(self):
        """Get '-hpc' if 'hpc1' or 'hpc2' is set"""
        if not self.is_hpc:
            return ""
        return "-hpc"

    @property
    def dash_HPC(self):
        """Get '-HPC' if 'hpc1' or 'hpc2' is set"""
        return self.dash_hpc.upper()

    @property
    def hpc_dash(self):
        """Get 'hpc-' if 'hpc1' or 'hpc2' is set"""
        if not self.is_hpc:
            return ""
        return "hpc-"

    @property
    def HPC_dash(self):
        """Get 'HPC-' if 'hpc1' or 'hpc2' is set"""
        return self.hpc_dash.upper()

    @property
    def sap1(self):
        """Get the value of the 'sap1' regex match"""
        return self._image_info['sap1']

    @property
    def sap2(self):
        """Get the value of the 'sap2' regex match"""
        return self._image_info['sap2']

    @property
    def is_sap(self):
        """Check if 'sap1' or 'sap2' is set"""
        return (self.sap1 is not None) or (self.sap2 is not None)

    @property
    def dash_sap(self):
        """Get '-sap' if 'sap1' or 'sap2' is set"""
        if not self.is_sap:
            return ""
        return "-sap"

    @property
    def dash_SAP(self):
        """Get '-SAP' if 'sap1' or 'sap2' is set"""
        return self.dash_sap.upper()

    @property
    def sap_desc(self):
        """Get sap description if 'sap1' or 'sap2' is set"""
        if not self.is_sap:
            return ""
        return " for SAP Applications"

    @property
    def sap_label_desc(self):
        """Get sap label description if 'sap1' or 'sap2' is set"""
        if not self.is_sap:
            return ""
        return " for SAP"

    @property
    def server_desc(self):
        """Get server description if 'hcp1' or 'hcp2' is set"""
        if self.is_hpc:
            return "HPC"
        if self.is_micro:
            return "Micro"
        return "Server"

    @property
    def byos(self):
        """Get the value of the 'byos' regex match"""
        return self._image_info['byos']

    @property
    def is_byos(self):
        """Check if 'byos' is set"""
        return self.byos is not None

    @property
    def is_payg(self):
        """Check if 'payg' is set"""
        return self.byos is None

    @property
    def dash_byos(self):
        """Get '-byos' if 'byos' is set"""
        if not self.is_byos:
            return ""
        return f"-{self.byos}"

    @property
    def dash_BYOS(self):
        """Get '-BYOS' if 'byos' is set"""
        return self.dash_byos.upper()

    @property
    def basic(self):
        """Get the value of the 'basic' regex match"""
        return self._image_info['basic']

    @property
    def is_basic(self):
        """Check if 'basic' is set"""
        return self.basic is not None

    @property
    def support_desc(self):
        """Get the support description"""
        if self.is_byos:
            suffix = "BYOS"
        elif self.is_azure:
            if self.is_basic:
                suffix = "Patching"
            else:
                suffix = "24x7 support"
        else:
            suffix = ""

        if len(suffix) > 0:
            return f" - {suffix}"

        return ""

    @property
    def product(self):
        """Get the value of the 'product' regex match"""
        return self._image_info['product']

    @property
    def product_base(self):
        """Get the value of the 'prodbase' regex match"""
        return self._image_info['prodbase']

    @property
    def product_major(self):
        """Get the value of the 'major_version' regex match"""
        return self._image_info['major_version']

    @property
    def product_minor(self):
        """Get the value of the 'minor_version' regex match"""
        min_ver = self._image_info['minor_version']
        return min_ver

    @property
    def product_minor_int(self):
        """Determine the product minor version (SPX or .X)"""
        if self.product_minor is None:
            return 0

        return int(self.product_minor.lower().replace('sp', ''))

    @property
    def product_version(self):
        """Determine the product version"""
        joiner = ''
        version = []
        result = None
        version.append(self.product_major)
        if (self.is_sle_server or self.is_hpc or self.is_lasso
                or self.is_sles_serv or self.is_suma):
            joiner = '-'
        elif (self.is_caasp or self.is_sumaserver or self.is_sumaproxy
                or self.is_leap or self.is_micro):
            joiner = '-'
        elif self.is_opensuse:
            joiner = '-'

        if self.product_minor:
            version.append(self.product_minor)

        if any(version):
            result = joiner.join(version)

        return result

    @property
    def has_product_version(self):
        """ Check if product_version is set"""
        return self.product_version is not None

    @property
    def product_version_string(self):
        """Set the product version string"""
        if not self.has_product_version:
            return ""
        return self.product_version

    @property
    def product_version_dashed(self):
        """Get the product version using a '-' as seperator"""
        return self.product_version_string.replace('.', '-')

    @property
    def product_version_dash_lower(self):
        """Get the lower case product version using a '-' as seperator"""
        return self.product_version_string.replace('.', '-').lower()

    @property
    def product_version_lower(self):
        """Get the lower case product version"""
        return self.product_version_string.lower()

    @property
    def product_version_spaced(self):
        """Get the product version using a ' ' as seperator"""
        return self.product_version_string.replace('-', ' ')

    # Determine how to maintain these mappings best. maybe in a config file?
    _SUMA_DISTRO = {
        # Keys should be the value of self.product_version
        "4.0": "15-SP1",
        "4.1": "15-SP2",
        "4.2": "15-SP3",
        "4.3": "15-SP4",
        "4.4": "15-SP5"
    }
    _MICRO_DISTRO = {
        # Keys should be the value of self.product_version
        "5.0": "15-SP2",
        "5.1": "15-SP3",
        "5.2": "15-SP3",
        "5.3": "15-SP4"
    }

    @property
    def distro_version(self):
        """Determine the distro version for images where the distro
            does not match the product"""
        if self.is_suma:
            version = self._SUMA_DISTRO[self.product_version]
        elif self.is_micro:
            version = self._MICRO_DISTRO[self.product_version]
        elif self.is_lasso:
            version = '15-SP3'
        else:
            version = self.product_version
        return version

    @property
    def has_distro_version(self):
        """Check if the 'distro_version' is set"""
        return self.distro_version is not None

    @property
    def distro_version_string(self):
        """Get the distro version string"""
        if not self.has_distro_version:
            return ""
        return self.distro_version

    @property
    def distro_version_dashed(self):
        """Get 'disto_version-'"""
        return self.distro_version_string.replace('.', '-')

    @property
    def distro_version_lower(self):
        """Get the lowercase of 'disto_version'"""
        return self.distro_version_string.lower()

    @property
    def distro_version_spaced(self):
        """Get 'disto_version' using ' ' as the seperator"""
        return self.distro_version_string.replace('-', ' ')

    @property
    def base_name(self):
        """Get the value of the 'base_name' regex match"""
        return self._image_info['base_name']

    @property
    def generic_name(self):
        """Get the generic name of the image"""
        name_parts = [
            self.base_name,
            "-v{date}"
        ]

        if self.has_suffix:
            if not self.is_azure:
                name_parts.append(self.suffix)

        return ''.join(name_parts)

    @property
    def datestamp(self):
        """Get the value of the 'datestamp' regex match"""
        return self._image_info['datestamp']

    @property
    def unique_name(self):
        "Get the unique name of the image"
        name_parts = [
            self.generic_name.format(date=self.datestamp)
        ]

        if self.has_uuid_prefix:
            if not self.is_azure:
                name_parts.append(self.uuid_prefix)

        return '-'.join(name_parts)

    @property
    def uuid_prefix(self):
        """Get the value of the 'uuid_prefix' regex match"""
        return self._image_info['uuid_prefix']

    @property
    def has_uuid_prefix(self):
        """Check if 'uuid_prefix' is set"""
        return self.uuid_prefix is not None

    @property
    def suffix(self):
        """Get the value of the 'suffix' regex match"""
        return self._image_info['suffix']

    @property
    def has_suffix(self):
        """Check if 'suffix' is set"""
        return self.suffix is not None

    @property
    def gen_id(self):
        """Get the value of the 'gen_id' regex match"""
        return self._image_info['gen_id']

    @property
    def has_gen_id(self):
        """Check if 'gen_id' is set"""
        return self.gen_id is not None

    @property
    def chost(self):
        """Get the value of the 'chost' regex match"""
        return self._image_info['chost']

    @property
    def is_chost(self):
        """ Check if 'chost' is set"""
        return self.chost is not None

    @property
    def dash_chost(self):
        """Get '-chost' if 'chost' is set"""
        if not self.is_chost:
            return ""
        return f"-{self.chost}"

    @property
    def dash_CHOST(self):
        """Get '-CHOST' if 'chost' is set"""
        return self.dash_chost.upper()

    @property
    def micro(self):
        """Get the value of the 'micro' regex match"""
        return self._image_info['micro']

    @property
    def is_micro(self):
        """ Check if 'micro' is set"""
        return self.micro is not None

    @property
    def dash_micro(self):
        """Get '-micro' if 'micro' is set"""
        if not self.is_micro:
            return ""
        return f"-{self.micro}"

    @property
    def dash_Micro(self):
        """Get '-Micro' if 'micro' is set"""
        if not self.is_micro:
            return ""
        return f"-{self.micro.capitalize()}"

    @property
    def ecs(self):
        """Get the value of the 'ecs' regex match"""
        return self._image_info['ecs']

    @property
    def is_ecs(self):
        """ Check if 'ecs' is set"""
        return self.ecs is not None

    @property
    def is_ec2_and_ecs(self):
        """ Check if 'ecs' is set"""
        return self.is_ec2 and self.is_ecs

    @property
    def ecs_desc(self):
        """Get the ecs description is 'ecs' is set"""
        if not self.is_ecs:
            return ""
        return " ECS Optimized"

    @property
    def dash_ecs(self):
        """Get '-ecs' if 'ecs' is set"""
        if not self.is_ecs:
            return ""
        return f"-{self.ecs}"

    @property
    def dash_ECS(self):
        """Get '-ECS' if 'ecs' is set"""
        return self.dash_ecs.upper()

    @property
    def ECS_dash(self):
        """Get 'ECS-' if 'ecs' is set"""
        if not self.is_ecs:
            return ""
        return f"{self.ecs.upper()}-"

    @property
    def virt_type(self):
        """Get the value of the 'virt_type' regex match"""
        return self._image_info['virt_type']

    @property
    def has_virt_type(self):
        """Get the 'virt_type' if it is set"""
        return self.virt_type is not None

    @property
    def is_hvm(self):
        """ Check if the 'virt_type' is set to hvm"""
        return self.has_virt_type and (self.virt_type == "hvm")

    @property
    def is_pv(self):
        """ Check if the 'virt_type' is set to pv"""
        return self.has_virt_type and (self.virt_type == "pv")

    @property
    def dash_virt_type(self):
        """Get '-virt_type' if 'virt_type' is set"""
        if not self.has_virt_type:
            return ""
        return f"-{self.virt_type}"

    @property
    def dash_VIRT_TYPE(self):
        """Get '-VIRT_TYPE' if 'virt_type' is set"""
        return self.dash_virt_type.upper()

    @property
    def sapcal(self):
        """Get the value of the 'sapcal' regex match"""
        return self._image_info['sapcal']

    @property
    def is_sapcal(self):
        """ Check if the 'sapcal' is set"""
        return self.sapcal is not None

    @property
    def dash_sapcal(self):
        """Get '-sapcal' if 'sapcal' is set"""
        if not self.is_sapcal:
            return ""
        return f"-{self.sapcal}"

    @property
    def dash_SAPCAL(self):
        """Get '-SAPCAL' if 'sapcal' is set"""
        return self.dash_sapcal.upper()

    @property
    def azure_hosted(self):
        """Get the value of the 'azure_hosted' regex match"""
        return self._image_info['azure_hosted']

    @property
    def is_azure_hosted(self):
        """ Check if the 'azure_hosted' is set"""
        return self.azure_hosted is not None

    @property
    def dash_azure_hosted(self):
        """Get '-azure_hosted' if 'azure_hosted' is set"""
        if not self.is_azure_hosted:
            return ""
        return f"-{self.azure_hosted}"

    @property
    def dash_AZURE_HOSTED(self):
        """Get '-AZURE_HOSTED' if 'azure_hosted' is set"""
        return self.dash_azure_hosted.upper()

    @property
    def ssd(self):
        """Get the value of the ssd regex match"""
        return self._image_info['ssd']

    @property
    def is_ssd(self):
        """ Check if the 'ssd' is set"""
        return self.ssd is not None

    @property
    def dash_ssd(self):
        """Get '-ssd' if 'ssd' is set"""
        if not self.is_ssd:
            return ""
        return f"-{self.ssd}"

    @property
    def dash_SSD(self):
        """Get '-SSD' if 'ssd' is set"""
        return self.dash_ssd.upper()

    @property
    def dash_ec2_sfx(self):
        """Get '-ec2_sfx"""
        return (f"{self.dash_ecs}{self.dash_virt_type}{self.dash_ssd}" +
                f"{self.dash_arch}")

    @property
    def dash_EC2_SFX(self):
        """Get '-EC2_SFX"""
        return self.dash_ec2_sfx.upper()
