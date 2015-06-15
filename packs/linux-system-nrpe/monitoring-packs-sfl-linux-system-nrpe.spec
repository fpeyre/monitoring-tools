Name:     monitoring-packs-sfl-linux-system-nrpe
Version:  0.3.2
Release:  1 
License: GPL v3
Summary: Standard linux NRPE active checks using NRPE, like CPU, RAM and disk space.
Group: Networking/Other
Source: https://github.com/savoirfairelinux/monitoring-tools/%{name}_%{version}.orig.tar.gz
URL: https://github.com/savoirfairelinux/monitoring-tools/
Distribution: Savoir-faire Linux
Vendor: Savoir-faire Linux
Packager: Savoir-faire Linux <supervision@savoirfairelinux.com>
BuildRoot:  %{_tmppath}/%{name}-%{version}
BuildRequires:  python-sphinx
BuildArch: noarch
%description
Standard linux NRPE active checks using NRPE, like CPU, RAM and disk space.

%prep
%setup -q

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m 755 %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}
%{__cp} -r pack/* %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}
%{__install} -p -m 755 package.json %{buildroot}/usr/lib/monitoring/packs/sfl/%{name}
sphinx-build -b html -d doc/build/doctrees/source doc %{buildroot}/%{_docdir}/monitoring/packs/sfl/%{name}
sphinx-build -b man -d doc/build/doctrees/source doc %{buildroot}/%{_mandir}/man7/

%clean
rm -rf 

%files
/usr/lib/monitoring/packs/sfl
%doc
%{_docdir}/monitoring/packs/sfl/%{name}
%{_mandir}/man7/*

%changelog
* Mon Jun 15 2015 Flavien Peyre <flavien.peyre@savoirfairelinux.com>
Change to version 0.3.2
* Thu Feb 19 2015 Savoir-faire Linux <supervision@savoirfairelinux.com>
- Initial Release
