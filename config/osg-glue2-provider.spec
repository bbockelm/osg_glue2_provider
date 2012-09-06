
# Python packages prefer "_" in the name; RPMs prefer "-".
#
%define python_name osg_glue2_provider

Summary: GLUE2 provider for the OSG
Name: osg-glue2-provider
Version: 0.1
Release: 1
Source0: %{python_name}-%{version}.tar.gz
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Brian Bockelman <bbockelm@cse.unl.edu>
Url: https://github.com/bbockelm/osg_glue2_provider

Requires: gip

%description
A GIP provider; designed to be run centrally for the OSG, and provide
the necessary GLUE2 interoperability with the WLCG.

%prep
%setup -n %{python_name}-%{version}

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%config(noreplace) %{_sysconfdir}/osg/config.d/glue2.cfg
%defattr(-,root,root)

%changelog
* Wed Sep 05 2012 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1-1
- Initial packaging of provider.

