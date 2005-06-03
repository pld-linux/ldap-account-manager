%define		_name	lam
Summary:	LDAP Account Manager (LAM) is a webfrontend for managing accounts stored in an openLDAP server
Name:		ldap-account-manager
Version:	0.4.9
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/lam/%{name}_%{version}.tar.gz
Source1:	%{name}.httpd
# Source0-md5:	6478d91210dbf13c9d49b7aa1a971be1
URL:		http://lam.sourceforge.net/
Requires:	apache
Requires:	php-ldap
# fuck mcrypt works without this, locking page
#Requires:	php-mcrypt
Requires:	php-gettext
Requires:	php-pcre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_confdir	%{_sysconfdir}/%{name}

%description
LDAP Account Manager (LAM) is a webfrontend for managing accounts stored in an openLDAP server.
Features:
- management of Unix user and group accounts (posixAccount/posixGroup)
- management of Samba 2.x/3 user and host accounts (sambaAccount/sambaSamAccount)
- profiles for account creation
- editor for organizational units (OU)
- account creation via file upload
- automatic creation/deletion of home directories
- setting quotas
- support for LDAP+SSL
- multi-language support (English, French, German, Hungarian, Japanese)
- multiple configuration files
- PDF output for user/group/host accounts
- additional text for user PDFs
- supports multiple password hashes


%description -l pl
-

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_confdir},%{_sysconfdir}/httpd} \
	$RPM_BUILD_ROOT%{_appdir}/{config,doc,graphics,sess,style,tmp,templates,lib,locale}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

install	index.html			$RPM_BUILD_ROOT%{_appdir}
install	config/config.cfg_sample	$RPM_BUILD_ROOT%{_appdir}/config/config.cfg
install	config/lam.conf_sample		$RPM_BUILD_ROOT%{_appdir}/config/lam.conf
install	templates/*.php			$RPM_BUILD_ROOT%{_appdir}/templates
install	lib/*.{inc,php}			$RPM_BUILD_ROOT%{_appdir}/lib
install	sess/.htaccess			$RPM_BUILD_ROOT%{_appdir}/sess
install	tmp/.htaccess			$RPM_BUILD_ROOT%{_appdir}/tmp
install	style/*css			$RPM_BUILD_ROOT%{_appdir}/style
install	graphics/*.{png,jpg}		$RPM_BUILD_ROOT%{_appdir}/graphics
cp -a	locale/*			$RPM_BUILD_ROOT%{_appdir}/locale

#ln -sf	%{_confdir}/config.php 	$RPM_BUILD_ROOT%{_appdir}/config.php

#mv -f	$RPM_BUILD_ROOT%{_appdir}/config.php.example $RPM_BUILD_ROOT%{_appdir}/config.php
#rm -f	$RPM_BUILD_ROOT%{_appdir}/config.php.example

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf; then
	echo "Include %{_sysconfdir}/httpd/%{name}.conf" >> %{_sysconfdir}/httpd/httpd.conf
elif [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
	 ln -sf %{_sysconfdir}/httpd/%{name}.conf %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	%{_sbindir}/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d %{_sysconfdir}/httpd/httpd.conf ]; then
		rm -f %{_sysconfdir}/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" %{_sysconfdir}/httpd/httpd.conf > \
			%{_sysconfdir}/httpd/httpd.conf.tmp
		mv -f %{_sysconfdir}/httpd/httpd.conf.tmp %{_sysconfdir}/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			%{_sbindir}/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc docs/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%config(noreplace) %verify(not size mtime md5) %{_appdir}/config/*.cfg
%config(noreplace) %verify(not size mtime md5) %{_appdir}/config/*.conf
%attr(740,http,http) %{_appdir}/sess
%attr(740,http,http) %{_appdir}/tmp
%{_appdir}
