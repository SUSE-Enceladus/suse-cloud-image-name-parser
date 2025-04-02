#
# spec file for package suse-cloud-image-name-parser
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#
%define upstream_name suse-cloud-image-name-parser
%{?sle15_python_module_pythons}


Name:           python-suse-cloud-image-name-parser
Version:        0.0.3
Release:        0
Summary:        Parses SUSE cloud image names
License:        Apache-2.0
Group:          Development/Languages/Python
URL:            https://github.com/SUSE-Enceladus/suse-cloud-image-name-parser
Source:         https://files.pythonhosted.org/packages/source/s/%{upstream_name}/%{upstream_name}-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  fdupes
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module wheel}
BuildArch:      noarch

%python_subpackages

%description

%prep
%setup -q -n %{upstream_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%{python_expand %fdupes %{buildroot}%{$python_sitelib}}

%check

%files %{python_files}
%defattr(-,root,root)
%doc README.md CHANGES.md
%{python_sitelib}/*

%changelog
