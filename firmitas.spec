Name:           firmitas
Version:        0.1.1
Release:        2%{?dist}
Summary:        Simple notification service for X.509-standard TLS certificate statuses

License:        GPLv3+
Url:            https://gitlab.com/t0xic0der/firmitas
Source0:        %{pypi_source firmitas}

BuildArch:      noarch

BuildRequires:  python3-devel

%description
Simple notification service for X.509-standard TLS certificate statuses

%prep
%autosetup -p 1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files firmitas

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/firmitas

%changelog

* Tue Jun 06 2023 Onuralp SEZER <thunderbirdtr@fedoraproject.org> - 0.1.1-2
- Cosmetic RPM specfile changes

* Thu Jun 01 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.1-1
- Stepped down dependency version requirements for EPEL9 compatibility
- Rework the RPM specfile to include support for EPEL9 release

* Thu Jun 01 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0-1
- Added notification support for ticketing repositories on Pagure
- Added checking for the validity of X.509-standard TLS certificates
- Introduced configuration mapping for the notification service
- Introduced configuration mapping for the X.509-standard TLS certificates
