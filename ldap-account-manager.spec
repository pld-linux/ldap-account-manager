#
%define		_name	lam
Summary:	LDAP Account Manager (LAM) - a webfrontend for managing accounts stored in an LDAP server
Summary(pl.UTF-8):	LDAP Account Manager (LAM) - interfejs WWW do zarządzania kontami na serwerze LDAP
Name:		ldap-account-manager
Version:	2.3.0
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/lam/%{name}-%{version}.tar.gz
# Source0-md5:	ceb5c6b795be2f3030b695b7f105e6f2
URL:		http://lam.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	php(gettext)
Requires:	php(iconv)
Requires:	php(ldap)
Requires:	php(mhash)
Requires:	php(pcre)
Requires:	php(xml)
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
LDAP Account Manager (LAM) is a webfrontend for managing accounts
stored in an LDAP server.

Features:
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
przechowywanymi na serwerze LDAP.

Możliwości:
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

cat > apache.conf <<'EOF'
Alias /%{_name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{_name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}} \
	$RPM_BUILD_ROOT%{_appdir}/{config,graphics,help,sess,style,tmp,templates,lib,locale}

install	index.html			$RPM_BUILD_ROOT%{_appdir}
cp -a	config/*			$RPM_BUILD_ROOT%{_appdir}/config
install	config/config.cfg_sample	$RPM_BUILD_ROOT%{_sysconfdir}/config.cfg
install	config/lam.conf_sample		$RPM_BUILD_ROOT%{_sysconfdir}/lam.conf
install	graphics/*.{png,jpg}		$RPM_BUILD_ROOT%{_appdir}/graphics
install	help/help.inc			$RPM_BUILD_ROOT%{_appdir}/help
cp -a	lib/*				$RPM_BUILD_ROOT%{_appdir}/lib
install	sess/.htaccess			$RPM_BUILD_ROOT%{_appdir}/sess
install	style/*css			$RPM_BUILD_ROOT%{_appdir}/style
cp -a	templates/*			$RPM_BUILD_ROOT%{_appdir}/templates
install	tmp/.htaccess			$RPM_BUILD_ROOT%{_appdir}/tmp
cp -a	locale/*			$RPM_BUILD_ROOT%{_appdir}/locale

rm -f 	$RPM_BUILD_ROOT%{_appdir}/config/*_sample

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

ln -s %{_sysconfdir}/config.cfg $RPM_BUILD_ROOT%{_appdir}/config/config.cfg
ln -s %{_sysconfdir}/lam.conf $RPM_BUILD_ROOT%{_appdir}/config/lam.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lam.conf
%dir %{_appdir}
%dir %attr(740,http,http) %{_appdir}/sess
%{_appdir}/sess/.htaccess
%dir %attr(740,http,http) %{_appdir}/tmp
%{_appdir}/tmp/.htaccess
%{_appdir}/config
%{_appdir}/graphics
%{_appdir}/help
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/style
%{_appdir}/templates
%{_appdir}/index.html
