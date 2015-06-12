Name:		monitoring-plugins-sfl-check-ceilometer
Version:    	0.3.2
Release:    	1
License: 	GPL v3
Summary: 	Shinken plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering
Group: 		Networking/Other
Source0: 	https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL:            https://github.com/savoirfairelinux/monitoring-tools
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
#Requires: python, python-dlnetsnmp
BuildRequires:  python-setuptools

%description 
Shinken plugin from SFL. A Nagios plug-in to use OpenStack Ceilometer API for metering

%prep
%setup -q -n check_ceilometer

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}%doc

%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/check_ceilometer
%{python_sitelib}/check_ceilometer/*

%changelog
* Fri Jun 12 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com>
- Updated to 0.3.2

* Mon May 05 2014 Alexandre Viau <alexandre.viau@savoirfairelinux.com>
- Initial Release
