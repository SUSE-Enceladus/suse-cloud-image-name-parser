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

"""imagenameparser Error Classes"""


class ImageParserError(Exception):

    """
    Base class for errors thrown by imagenameparser. Any class inheriting from
    it must implement a `message` attribute at the very least.
    """


class APIError(ImageParserError):
    """Derived class for exceptions thrown by imagenameparser
       API.

    Attributes:
        message -- relevant error message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InvalidFrameworkError(APIError):
    """Derived class for invalid framework exceptions."""

    def __init__(self, message, framework):
        """Exception raised for invalid framework errors.

        Parameters:
            message -- stringified error message
            framework -- the invalid framework
        """
        self.message = message
        self.framework = framework
        super().__init__(message)

    def __str__(self):
        return f"{self.message}: {self.framework}"


class BadRegexMatchError(APIError):
    """Derived class for image name regex exceptions."""

    def __init__(self, message):
        """Exception raised for a missing fragment.

        Parameters:
            message -- stringified error message
        """
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"
