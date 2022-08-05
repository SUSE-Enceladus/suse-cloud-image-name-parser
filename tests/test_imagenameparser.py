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
#
# Basic testing of imagenameparser api using pytest
#

import pytest
from imagenameparser.api.image_name import ImageName

pytest_plugins = ["pytester"]


#
# Testing Data
#
framework_images = [
    ("azure", "suse-opensuse-leap-15-2-v20200702",
     "suse-opensuse-leap-15-2-v{date}"),
    ("azure",
     "021d1b90c82943ec959408cff8e26c37__suse-sles-12-sp5-hpc-byos-v20201110",
     "suse-sles-12-sp5-hpc-byos-v{date}"),
    ("azure",
     "021d1b90c82943ec959408cff8e26c37__suse-sles-12-sp5-basic-v20200922",
     "suse-sles-12-sp5-basic-v{date}"),
    ("ec2", "suse-sles-15-sp2-byos-v20201111-hvm-ssd-arm64",
     "suse-sles-15-sp2-byos-v{date}-hvm-ssd-arm64"),
    ("ec2", "suse-sle-hpc-15-sp2-byos-v20201106-hvm-ssd-x86_64",
     "suse-sle-hpc-15-sp2-byos-v{date}-hvm-ssd-x86_64"),
    ("ec2", "suse-manager-server-4-1-byos-v20200721-hvm-ssd-x86_64",
     "suse-manager-server-4-1-byos-v{date}-hvm-ssd-x86_64"),
    ("ec2", "suse-sles-15-sp1-chost-byos-v20200922-hvm-ssd-x86_64",
     "suse-sles-15-sp1-chost-byos-v{date}-hvm-ssd-x86_64"),
    ("ec2", "suse-sles-sap-15-sp2-v20200721-hvm-ssd-x86_64",
     "suse-sles-sap-15-sp2-v{date}-hvm-ssd-x86_64"),
    ("ec2", "suse-sles-12-sp5-v20200918-ecs-hvm-ssd-x86_64",
     "suse-sles-12-sp5-v{date}-ecs-hvm-ssd-x86_64"),
    ("gce", "sles-15-sp2-chost-byos-v20201016",
     "sles-15-sp2-chost-byos-v{date}"),
    ("gce", "sles-15-sp1-sapcal-v20201023",
     "sles-15-sp1-sapcal-v{date}"),
    ("gce", "sles-15-sp2-byos-v20191001",
     "sles-15-sp2-byos-v{date}"),
    ("oci", "sles-12-sp5-byos-v20200917",
     "sles-12-sp5-byos-v{date}"),
    ("oci", "sles-15-sp2-sap-byos-v20201110",
     "sles-15-sp2-sap-byos-v{date}"),
    ("aliyun", "sles-15-sp2-chost-byos-v20201110",
     "sles-15-sp2-chost-byos-v{date}"),
    ("ec2", "suse-sle-micro-5-1-byos-v20220215-gen2",
     "suse-sle-micro-5-1-byos-v{date}-gen2"),
    ("ec2", "suse-sle-micro-5-1-byos-v20220719-hvm-ssd-arm64",
     "suse-sle-micro-5-1-byos-v{date}-hvm-ssd-arm64"),
    ("gce", "sles-15-sp4-sap-v20220621-x86-64",
     "sles-15-sp4-sap-v{date}-x86-64"),
    ("gce", "sle-micro-5-1-byos-v20220719-x86-64",
     "sle-micro-5-1-byos-v{date}-x86-64"),
    ("oci", "sles-15-sp3-byos-v20211003",
     "sles-15-sp3-byos-v{date}"),
    ("oci", "sles-15-sp3-sap-byos-v20211003",
     "sles-15-sp3-sap-byos-v{date}")

]

test_parameters = {
    'local': True,
    'verify': True,
}

#
# Test the functionality provided by the API backend code
#


class TestImageparserAPI(object):

    def test_api_import(self):
        import imagenameparser.api  # noqa

    @pytest.mark.parametrize("framework,image_name,generic_name",
                             framework_images)
    def test_api_ImageName(self, framework, image_name, generic_name):

        res = ImageName(framework, image_name)

        assert res.generic_name == generic_name

    def test_image_product(self):
        image_name = "opensuse-leap-15-4-v20220722-arm64"
        framework = "gce"

        res = ImageName(framework, image_name)

        assert res.product == "opensuse-leap"
        assert res.product_major == "15"
        assert res.product_minor == "4"
        assert res.product_minor_int == 4
        assert res.product_version == "15-4"
        assert res.has_product_version is True
        assert res.product_version_string == "15-4"
        assert res.product_version_dashed == "15-4"
        assert res.product_version_dash_lower == "15-4"
        assert res.product_version_spaced == "15 4"
        assert res.is_leap is True
        assert res.leap == "opensuse-leap"
        assert res.is_sle_server is False
        assert res.is_sle is False
        assert res.is_suma is False
        assert res.is_lasso is False
        assert res.is_sap is False
        assert res.distro_version == "15-4"
        assert res.has_distro_version is True
        assert res.distro_version_string == "15-4"
        assert res.distro_version_dashed == "15-4"
        assert res.distro_version_spaced == "15 4"
        assert res.distro_version_lower == "15-4"
        assert res.base_name == "opensuse-leap-15-4"
        assert res.generic_name == "opensuse-leap-15-4-v{date}-arm64"
        assert res.unique_name == "opensuse-leap-15-4-v20220722-arm64"
        assert res.datestamp == "20220722"

    def test_image_byos_arch(self):
        image_name = "suse-sles-sap-15-sp2-byos-v20210212-hvm-ssd-x86_64"
        framework = "ec2"

        res = ImageName(framework, image_name)

        assert res.is_byos is True
        assert res.byos == "byos"
        assert res.is_payg is False
        assert res.dash_byos == "-byos"
        assert res.dash_BYOS == "-BYOS"
        assert res.support_desc == " - BYOS"
        assert res.arch == "x86_64"
        assert res.is_x86_64
        assert res.is_aarch64 is False
        assert res.is_arm64 is False
        assert res.is_amd64
        assert res.cloud_arch == "x86_64"
        assert res.is_hvm
        assert res.is_pv is False
        assert res.ssd == "ssd"
        assert res.is_ssd
        assert res.dash_ssd == "-ssd"
        assert res.dash_SSD == "-SSD"

    def test_image_payg(self):
        image_name = "suse-sles-11-sp4-rightscale-v20150714-pv-ssd-x86_64"
        framework = "ec2"

        res = ImageName(framework, image_name)

        assert res.is_byos is False
        assert res.is_payg
        assert res.is_pv

    def test_image_suma_uuid(self):
        image_name = ("5c9ba39cec434780938dba0f6ea3126d__suse-manager"
                      "-4-0-server-byos-v20210210")
        framework = "azure"

        res = ImageName(framework, image_name)

        assert res.uuid_prefix == "5c9ba39cec434780938dba0f6ea3126d"
        assert res.has_uuid_prefix
        assert res.suma == "suse-manager"
        assert res.suma_type == "server"
        assert res.suma_type_desc == "Server"
        assert res.dash_suma_type == "-server"
