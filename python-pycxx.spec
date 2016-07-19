%if (0%{?rhel} >= 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif
%global modname pycxx

# Specify '--without=python3' to NOT build the python 3 RPM
%if 0%{?rhel} && 0%{?rhel} <= 6
# el6 has no python3 packages
%global with_python3 0
%else
%global with_python3 %{?_without_python3:0} %{?!_without_python3:1}
%endif

%global svn_rev 280
%global download_date 20130805
%global vcs_rel %{download_date}svn%{svn_rev}

Name:           python-%{modname}
Version:        6.2.8
Release:        2%{?dist}
Summary:        Write Python extensions in C++

Group:          Development/Libraries
License:        BSD
URL:            http://CXX.sourceforge.net/

BuildArch:      noarch

# SVN version contains updates for Python3
Source0:        http://downloads.sourceforge.net/cxx/%{modname}-%{version}.tar.gz
#Source0:        http://sourceforge.net/code-snapshots/svn/c/cx/cxx/code/cxx-code-%{svn_rev}-trunk.zip
# Patch0:  remove unnecessary 'Src/' directory from include path in sources
Patch0:         %{name}-%{version}-change-include-paths.patch
# Patch1:  fix several problems with install, esp. omitted files, python 
# v2/v3 awareness
Patch1:         %{name}-%{version}-setup.py.patch

BuildRequires:  python2-devel
%if %{with_python3}
BuildRequires:  python3-devel
%endif


%description
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.


%package devel
Summary:        PyCXX header and source files
Group:          Development/Libraries
Requires:       python2

%description devel
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.

The %{name}-devel package provides the header and source files
for Python 2.  There is no non-devel package needed.


%package -n python3-%{modname}-devel
Summary:        PyCXX header and source files
Group:          Development/Libraries
Requires:       python3

%description -n python3-%{modname}-devel
PyCXX is a set of classes to help create extensions of Python in the
C++ language. The first part encapsulates the Python C API taking care
of exceptions and ref counting. The second part supports the building
of Python extension modules in C++.

The python3-%{modname}-devel package provides the header and source files
for Python 3.  There is no non-devel package needed.


%prep
# SVN version .zip file unpacks differently
#setup -q -n cxx-code-%{svn_rev}-trunk/CXX
%setup -q -n %{modname}-%{version}
%patch0 -p1 -b .change-include-paths
%patch1 -p1 -b .setup


%build
python setup.py build


%install
INSTALL='setup.py install
        --root=%{buildroot}
        --prefix=%{_prefix}
        --install-headers=%{_includedir}/CXX
        --install-data=%{_usrsrc}'

%{__python} $INSTALL

%if %{with_python3}
%{__python3} $INSTALL
%endif

# Write pkg-config PyCXX.pc file
mkdir -p %{buildroot}%{_datadir}/pkgconfig
cat > %{buildroot}%{_datadir}/pkgconfig/PyCXX.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
includedir=%{_includedir}
srcdir=%{_usrsrc}/CXX

Name: PyCXX
Description: Write Python extensions in C++
Version: %{version}
Cflags: -I\${includedir}
EOF


%files devel
%doc README.html COPYRIGHT Doc/Python2/ 
%dir %{_includedir}/CXX
%{_includedir}/CXX/*.hxx
%{_includedir}/CXX/*.h
%{_includedir}/CXX/Python2
%{python_sitelib}/CXX*
%dir %{_usrsrc}/CXX
%{_usrsrc}/CXX/*.cxx
%{_usrsrc}/CXX/*.c
%{_usrsrc}/CXX/Python2
%{_datadir}/pkgconfig/PyCXX.pc


%if %{with_python3}
%files -n python3-%{modname}-devel
%doc README.html COPYRIGHT Doc/Python3/ 
%dir %{_includedir}/CXX
%{_includedir}/CXX/*.hxx
%{_includedir}/CXX/*.h
%{_includedir}/CXX/Python3
%{python3_sitelib}/CXX*
%dir %{_usrsrc}/CXX
%{_usrsrc}/CXX/*.cxx
%{_usrsrc}/CXX/*.c
%{_usrsrc}/CXX/Python3
%{_datadir}/pkgconfig/PyCXX.pc
%endif


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion PyCXX)" = "%{version}"


%changelog
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 16 2016 Richard Shaw <hobbes1069@gmail.com> - 6.2.8-1
- Update to latest upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-12.20130805svn280
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-11.20130805svn280
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-10.20130805svn280
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-9.20130805svn280
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 6.2.4-8.20130805svn280
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Aug  5 2013 John Morris <john@zultron.com> - 6.2.4-7.280svn20130805
- Update to SVN r280 for python3 compatibility
- Update python-pycxx-6.2.4-setup.py.patch to apply correctly
- Fix %%setup for SVN zipball
- Add diff extensions to %%patch macros
- Enable python3 pkg by default except for EPEL; see BZ 991342

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 John Morris <john@zultron.com> - 6.2.4-4
- Minor macro fixes for compiling on el6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012  <john@zultron.com> - 6.2.4-2
- Fix Source0 URL

* Thu Jun 28 2012  <john@zultron.com> - 6.2.4-1
- Install headers into /usr/include/CXX instead of default
  /usr/include/python2.7/CXX (setup.py command line option)
- Install sources into /usr/src/CXX rather than /usr/share/python2.7/CXX
- setup.py patch:
  - Update PyCXX version number
  - Convert tabs to spaces (from original patch)
  - Add omitted headers and sources to install
    - Extend install_headers to handle subdirs
  - Install only Python v2 or v3 code as appropriate
- Add --with=python3 option to build python3-pycxx-devel RPM

* Wed Jun 27 2012  <john@zultron.com> - 6.2.4-0
- Add a pkg-config PyCXX.pc file
- Update to 6.2.4
- Build only a -devel package; no regular package needed
- Beautify specfile, fix macros

* Thu Mar 29 2012  <jman@greaser.zultron.com> - 6.2.3-2
- rebuild with koji

* Wed Feb 22 2012 John Morris <john@zultron.com> - 6.2.3-1
- update to compile on el5 as well as fc16 (missing python_sitelib macro)

* Tue Feb 21 2012  <jman@greaser.zultron.com> - 6.2.3-1
- changed python_sitearch to python_sitelib in files section, 
  since package installs in /usr/lib even on x86_64

* Tue Nov 03 2009 Steve Huff <shuff@vecna.org> - 6.1.1-1 - 7987/shuff
- Renamed per RPMforge naming convention.

* Thu Oct 08 2009 Steve Huff <shuff@vecna.org> - 6.1.1-1
- Initial package.

