# TODO
# - webapps
%define		_name	lam
Summary:	LDAP Account Manager (LAM) - a webfrontend for managing accounts stored in an LDAP server
Summary(pl.UTF-8):	LDAP Account Manager (LAM) - interfejs WWW do zarządzania kontami na serwerze LDAP
Name:		ldap-account-manager
Version:	0.4.9
Release:	0.3
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/lam/%{name}_%{version}.tar.gz
Source1:	%{name}.httpd
# Source0-md5:	6478d91210dbf13c9d49b7aa1a971be1
URL:		http://lam.sourceforge.net/
Requires:	php(gettext)
Requires:	php(ldap)
Requires:	php(pcre)
Requires:	webserver = apache
# fuck mcrypt works without this, locking page
#Requires:	php-mcrypt
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_confdir	%{_sysconfdir}/%{name}

%description
LDAP Account Manager (LAM) is a webfrontend for managing accounts
stored in an LDAP server. Features:
- management of Unix user and group accounts (posixAccount/posixGroup)
- management of Samba 2.x/3 user and host accounts
  (sambaAccount/sambaSamAccount)
- profiles for account creation
- editor for organizational units (OU)
- account creation via file upload
- automatic creation/deletion of home directories
- setting quotas
- support for LDAP+SSL
- multi-language support (English, French, German, Hungarian,
  Japanese)
- multiple configuration files
- PDF output for user/group/host accounts
- additional text for user PDFs
- supports multiple password hashes


%description -l pl.UTF-8
LDAP Account Manager (LAM) to interfejs WWW do zarządzania kontami
przechowywanymi na serwerze LDAP. Możliwości:
- zarządzanie kontami uniksowych użytkowników i grup
  (posixAccount/posixGroup)
- zarządzanie kontami użytkowników i hostów Samby 2.x/3
  (sambaAccount/sambaSamAccount)
- tworzenie profili dla kont
- edytor jednostej organizacyjnych (OU)
- tworzenie kont poprzez upload plików
- automatyczne tworzenie/usuwanie katalogów domowych
- ustawianie quot
- obsługa LDAP+SSL
- obsługa wielu języków (angielski, francuski, niemiecki, węgierski,
  japoński)
- wiele plików konfiguracyjnych
- wyjście PDF dla kont użytkowników/grup/hostów
- dodatkowy tekst dla PDF-ów użytkownika
- obsługa wielu skrótów haseł

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_confdir},%{_sysconfdir}/httpd} \
	$RPM_BUILD_ROOT%{_appdir}/{config,doc,graphics,help,sess,style,tmp,templates,lib,locale}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

install	index.html			$RPM_BUILD_ROOT%{_appdir}
cp -a	config/*			$RPM_BUILD_ROOT%{_appdir}/config
install	config/config.cfg_sample	$RPM_BUILD_ROOT%{_appdir}/config/config.cfg
install	config/lam.conf_sample		$RPM_BUILD_ROOT%{_appdir}/config/lam.conf
install	graphics/*.{png,jpg}		$RPM_BUILD_ROOT%{_appdir}/graphics
install	help/*.inc			$RPM_BUILD_ROOT%{_appdir}/help
install	lib/*.{inc,php}			$RPM_BUILD_ROOT%{_appdir}/lib
install	sess/.htaccess			$RPM_BUILD_ROOT%{_appdir}/sess
install	style/*css			$RPM_BUILD_ROOT%{_appdir}/style
cp -a	templates/*			$RPM_BUILD_ROOT%{_appdir}/templates
install	tmp/.htaccess			$RPM_BUILD_ROOT%{_appdir}/tmp
cp -a	locale/*			$RPM_BUILD_ROOT%{_appdir}/locale

rm -f 	$RPM_BUILD_ROOT%{_appdir}/config/*.sample

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
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_appdir}/config/*.cfg
%config(noreplace) %verify(not md5 mtime size) %{_appdir}/config/*.conf
%attr(740,http,http) %{_appdir}/sess
%attr(740,http,http) %{_appdir}/tmp
# XXX: dup
%{_appdir}
