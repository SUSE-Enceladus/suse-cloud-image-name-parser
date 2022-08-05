#
# spec file for package susecloudimagenameparser 
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. 
# The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Name:           python3-susecloudimagenameparser 
Version:        1.0.0 
Release:        0
Summary:        Parse Public Cloud image names  
License:        Apache-2.0 
URL:            https://github.com/SUSE-Enceladus/suse-cloud-image-name-parser
Source:         susecloudimagenameparser-%{version}.tar.gz

BuildRequires:  python-rpm-macros
BuildRequires:  python3-pytest
BuildRequires:  python3-PyYAML
Requires:       python3-PyYAML

%description
Package that Parse Public Cloud image names that match the 
SUSE naming convention

%prep
%setup -q -n susecloudimagenameparser-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files 
%license LICENSE
%doc CONTRIBUTING.md README.md
%{python_sitelib}/*

%changelog
