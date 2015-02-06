#Module-Specific definitions
%define apache_version 2.2.8
%define mod_name mod_wsgi
%define mod_conf B23_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Python WSGI adapter module for Apache
Name:		apache-%{mod_name}
Version:	3.4
Release:	2
Group:		System/Servers
License:	Apache License
URL:		http://code.google.com/p/modwsgi/
Source0:	http://modwsgi.googlecode.com/files/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
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

cp %{SOURCE1} %{mod_conf}

%build
rm -f configure
autoconf

%configure2_5x --localstatedir=/var/lib \
    --with-apxs=%{_bindir}/apxs

%make

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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

%clean

%files
%doc LICENCE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 3.3-4mdv2011.0
+ Revision: 678443
- mass rebuild

* Wed Nov 03 2010 Michael Scherer <misc@mandriva.org> 3.3-3mdv2011.0
+ Revision: 592700
- rebuild for python 2.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3-2mdv2011.0
+ Revision: 588089
- rebuild

* Tue Oct 19 2010 Oden Eriksson <oeriksson@mandriva.com> 3.3-1mdv2011.0
+ Revision: 586711
- 3.3

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.5-3mdv2010.1
+ Revision: 516265
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.5-2mdv2010.0
+ Revision: 406682
- rebuild

* Sun Jun 21 2009 Oden Eriksson <oeriksson@mandriva.com> 2.5-1mdv2010.0
+ Revision: 387751
- 2.5
- nuke redundant patches

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-3mdv2009.1
+ Revision: 326274
- rebuild

* Mon Dec 29 2008 Michael Scherer <misc@mandriva.org> 2.3-2mdv2009.1
+ Revision: 320992
- add patch for format string error
- rebuild for new python

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3-1mdv2009.1
+ Revision: 294280
- 2.3

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1-1mdv2009.0
+ Revision: 270290
- 2.1

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0-3mdv2009.0
+ Revision: 235131
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0-2mdv2009.0
+ Revision: 215674
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

* Sat May 10 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0-1mdv2009.0
+ Revision: 205396
- 2.0

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2-2mdv2008.1
+ Revision: 182876
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Oct 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2-1mdv2008.1
+ Revision: 103921
- fix deps
- import apache-mod_wsgi


* Tue Oct 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2-1mdv2008.1
- initial Mandriva package
