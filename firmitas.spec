Name:           firmitas
Version:        0.1.0
Release:        1%{?dist}
Summary:        Simple notification service for X.509-standard TLS certificate statuses

License:        GPLv3+
Url:            https://gitlab.com/t0xic0der/%{name}
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3-devel

%description
Simple notification service for X.509-standard TLS certificate statuses

%prep
%autosetup

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files nvautoinstall

%files -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog

* Thu Jun 01 2023 Akashdeep Dhar <t0xic0der@fedoraproject.org> - 0.1.0-1
- v0.1.0 - Released on June 01st, 2023
- Added notification support for ticketing repositories on Pagure
- Added checking for the validity of X.509-standard TLS certificates
- Introduced configuration mapping for the notification service
- Introduced configuration mapping for the X.509-standard TLS certificates
