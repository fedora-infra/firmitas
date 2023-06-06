%global pypi_name firmitas

Name:           %{pypi_name}
Version:        0.1.1
Release:        2%{?dist}
Summary:        Simple notification service for X.509-standard TLS certificate statuses

License:        GPLv3+
Url:            https://gitlab.com/t0xic0der/%{pypi_name}
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description
Simple notification service for X.509-standard TLS certificate statuses

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%files -n %{pypi_name} -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{pypi_name}

%changelog

* Tue Jun 06 2023 Onuralp SEZER <thunderbirdtr@fedoraproject.org> - 0.1.1-2
- cosmetic rpm-spec file changes

* Thu Jun 01 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.1-1
- v0.1.1 - Released on June 01st, 2023
- Stepped down dependency version requirements for EPEL9 compatibility
- Rework the RPM specfile to include support for EPEL9 release

* Thu Jun 01 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0-1
- v0.1.0 - Released on June 01st, 2023
- Added notification support for ticketing repositories on Pagure
- Added checking for the validity of X.509-standard TLS certificates
- Introduced configuration mapping for the notification service
- Introduced configuration mapping for the X.509-standard TLS certificates
