# suse-cloud-image-name-parser
Parse Public Cloud image names that match the SUSE naming convention

API implementation to parse image names that match the SUSE Public Cloud image naming convention.

## Quick Start

### Install from Source

```bash
  # Clone the repo
  $ git clone https://github.com/SUSE-Enceladus/suse-cloud-image-name-parser
  $ cd suse-cloud-image-name-parser 

  # create the virtual environment.
  $ virtualenv dev_venv --python=python3

  # activate the virtual environment for interactive bash session
  $ source dev_venv/bin/activate

  # There is 2 ways you can install
    1. Install latest sources in developer mode
       $ pip install -e .[dev]

    2. Install latest version normally
       $ pip install .[dev]
```

## Running Unit Tests

```bash
  # Clone the repo
  $ git clone https://github.com/SUSE-Enceladus/suse-cloud-image-name-parser
  $ cd suse-cloud-image-name-parser

  # create the Python 3 virtual environment.
  $ virtualenv test_venv --python=python3

  # activate the virtual environment for interactive bash session
  $ source test_venv/bin/activate

  # Install dependencies
  $ pip install -e .[dev]

  # Run Unit Tests
  $ tox -e pytest
```

## Install from Cloud:Tools OBS project

```bash
  zypper ar http://download.opensuse.org/repositories/Cloud:/Tools/<distribution>
  zypper refresh
  zypper in python3-susecloudimagenameparser
```

## Install from PyPI

```bash
  pip install python3-susecloudimagenameparser
```

## Usage

The ImageName class can be imported and used as an API in code with the 
package installed using one of the methods above.

Once the package is imported  
```bash
  from imagenameparser.api.image_name import ImageName
  from imagenameparser.errors import BadRegexMatchError
```

Call the API to parse Public Cloud image name that match the SUSE naming convention
```bash
  parsedimg = ImageName(provider, image_name)
  where
    provider - valid cloud provider name such as alibaba, amazon, microsoft, google, oracle,
    ec2 or azure
    image_name - Valid image name that match SUSE naming convention such as image name
    reported by susepubliccloudinfo client 
```   
