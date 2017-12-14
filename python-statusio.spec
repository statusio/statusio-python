%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           statusio-python
Version:        0.5
Release:        %{?dist}
Summary:        Python Interface for Status.io API

Group:          Development/Libraries
License:        Apache License 2.0
URL:            http://github.com/statusio/statusio-python
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       python >= 2.6,
BuildRequires:  python-setuptools


%description
This library provides a pure python interface for the Status.io API.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
chmod a-x README
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.rst
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
- Initial package.