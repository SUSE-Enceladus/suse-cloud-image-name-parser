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

"""
API implementation to parse image names that match the SUSE Public Cloud
image naming convention.
"""

from imagenameparser.api.image_name import ImageName

__all__ = ["ImageName"]
__author__ = """Public Cloud Engineering <public-cloud-dev@susecloud.net>"""
__date__ = "5 August 2022"
__VERSION__ = "1.0.0"
