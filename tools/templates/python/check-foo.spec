%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}


Name:           monitoring-plugins-sfl-{{ name }}
Version:        {{ date_long }}
Release:        1%{?dist}
Summary:        {{ desc }}

License:        GPLv3
URL:            https://github.com/savoirfairelinux/monitoring-tools
Source0:        https://github.com/savoirfairelinux/monitoring-tools/monitoring-plugins-sfl-{{ name }}_%{version}.orig.tar.gz

Requires:       python-shinkenplugins
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
{{ desc }}
More information is available on Github:
https://github.com/savoirfairelinux/sfl-shinken-plugins

%prep
%setup -q -n monitoring-plugins-sfl-{{ name }}


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --install-lib=%{python_sitelib}
%{__mkdir_p} %{buildroot}/%{_libdir}/monitoring/plugins/sfl
install -p -m0755 {{ exec_name }}  %{buildroot}/%{_libdir}/monitoring/plugins/sfl

%check
cd %{buildroot}/%{python_sitelib}/shinkenplugins/plugins/ && %{__python} -c "import {{ short_name }}"


%files
%defattr(-,root,root,-)
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/shinkenplugins
%{python_sitelib}/shinkenplugins/plugins/{{ short_name }}
%{_libdir}/monitoring/plugins/sfl/{{ exec_name }}

%changelog
* {{ date_rpm }} {{ author_name }} <{{ author_email }}> - {{ date_long }}
- Initial package
