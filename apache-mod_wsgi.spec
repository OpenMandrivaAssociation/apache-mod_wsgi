#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_wsgi
%define load_order 123

Summary:	Python WSGI adapter module for Apache
Name:		apache-%{mod_name}
Version:	3.3
Release:	6
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/modwsgi/
Source0:	http://modwsgi.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	python-devel
BuildRequires:	apache-mpm-prefork >= %{apache_version}

%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.

%prep

%setup -q -n %{mod_name}-%{version}

%build
rm -f configure
autoconf

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs

%make

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule wsgi_module %{_libdir}/%{mod_name}.so
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc LICENCE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
