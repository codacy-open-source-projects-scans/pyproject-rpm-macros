%global pypi_name entrypoints
Name:           python-%{pypi_name}
Version:        0.3
Release:        0%{?dist}
Summary:        Discover and load entry points from installed packages
License:        MIT
URL:            https://entrypoints.readthedocs.io/
Source0:        %{pypi_source}

BuildArch:      noarch

%description
This package contains one .py module
Building this tests the flit(_core) build backend.
This package also has no explicit BuildRequires for python or the macros,
testing the minimal implementation of %%pyproject_buildrequires
from pyproject-srpm-macros.


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
%{summary}.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
%if 0%{?rhel}
# force the flit-core build backend, as that is available rather than full flit
sed -i 's/"flit/"flit_core/' pyproject.toml
%endif


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# the license is not marked as License-File, hence -L
%pyproject_save_files entrypoints -L


%check
# Internal check: Top level __pycache__ is never owned
grep -E '/__pycache__$' %{pyproject_files} && exit 1 || true
grep -E '/__pycache__/$' %{pyproject_files} && exit 1 || true
grep -F '/__pycache__/' %{pyproject_files}


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%license LICENSE
