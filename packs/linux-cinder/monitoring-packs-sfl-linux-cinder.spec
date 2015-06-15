Name:      monitoring-packs-sfl-linux-cinder
Version:   0.3.2
Release:   1
License: GPL v3
Summary: Shinken pack for monitoring OpenStack Cinder
Group: Networking/Other
Source:https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL: https://github.com/savoirfairelinux/monitoring-tools
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Alexandre Viau <alexandre.viau@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildArch : noarch

%description 
Shinken pack for monitoring OpenStack Cinder

%prep
echo %{name}
echo %{buildroot}
%setup -q 

%install

%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}
%{__cp} -r pack/*  %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}
%{__install} -p -m 755 package.json  %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config
/usr/lib/monitoring/packs/sfl/

%changelog
* Mon Jun 15 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com>
* Fri Jan 02 2015 Alexandre Viau <alexandre.viau@savoirfairelinux.com>
- Initial Release
