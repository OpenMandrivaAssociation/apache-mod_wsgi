%define _disable_ld_no_undefined %nil

#Module-Specific definitions
%define apache_version 2.4.46
%define mod_name mod_wsgi
%define mod_conf B23_%{mod_name}.conf
%define mod_so %{mod_name}.so

%bcond_without	python
%bcond_without	docs

Summary:	Python WSGI adapter module for Apache
Name:		apache-%{mod_name}
Version:	5.0.2
Release:	1
Group:		System/Servers
License:	Apache License
URL:		https://github.com/GrahamDumpleton/mod_wsgi
Source0:	https://github.com/GrahamDumpleton/mod_wsgi/archive/%{version}/mod_wsgi-%{version}.tar.gz
Source1:	%{mod_conf}
Source2:	wsgi-python3.conf
Patch0:		mod_wsgi-4.5.20-exports.patch
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	apache-mpm-prefork >= %{apache_version}
BuildRequires:  pkgconfig(apr-1)

Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}

%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.

%files
%license LICENSE
%doc README.rst
%config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%{_libdir}/apache/%{mod_so}

#---------------------------------------------------------------------------

%if %{with python}
%package -n python-%{mod_name}
Summary:	Python module for %{mod_name}
Requires:	apache	
Requires:	%{name} = %{EVRD}
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(setuptools)
%if %{with docs}
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)
%endif

%description -n python-%{mod_name}
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.

This packages provides a python python module for %{mod_name}.

%files -n python-%{mod_name}
%license LICENSE
%doc CREDITS.rst README.rst
%config(noreplace) %{_sysconfdir}/httpd/modules.d/*wsgi-python3.conf
%{py_platsitedir}/mod_wsgi-*.*-info
%{py_platsitedir}/mod_wsgi
%{_bindir}/mod_wsgi-express
%endif

#---------------------------------------------------------------------------

%prep
%autosetup -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}
sed -i "s|_MODULE_DIR_|%{_libdir}/apache|g" %{mod_conf}

cp %{SOURCE2} 10-wsgi-python3.conf
sed -i "s|_MODULE_DIR_|%{_libdir}/apache|g" 10-wsgi-python3.conf

%build
export LDFLAGS="%{ldflags} -L%{_libdir}"
export CFLAGS="%{optflags} -fno-strict-aliasing"

%config_update
%configure \
	 --enable-shared \
	--localstatedir=/var/lib \
	--with-apxs=%{_bindir}/apxs
%make_build

%if %{with python}
%py_build
%endif

%if %{with docs}
%make_build -C docs html
%endif

%install
%py_install

install -pm 0755 -d %{buildroot}%{_libdir}/apache
install -pm 0755 src/server/.libs/%{mod_so} %{buildroot}%{_libdir}/apache

install -pm 0755 -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -pm 0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}
install -pm 0644 10-wsgi-python3.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

