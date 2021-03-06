# TODO
# - ldap schema package: docs/schema/dhcp.schema
# - system fpdf
# - system seclib
Summary:	Administration of LDAP users, groups and hosts via Web GUI
Summary(de.UTF-8):	Administration von Benutzern, Gruppen und Hosts für LDAP-Server
Summary(pl.UTF-8):	LDAP Account Manager (LAM) - interfejs WWW do zarządzania kontami na serwerze LDAP
Name:		ldap-account-manager
Version:	3.9
Release:	3
License:	GPL v2+
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/lam/%{name}-%{version}.tar.gz
# Source0-md5:	44f33cfd2a900ad9739692a7f4844f51
Source1:	apache.conf
Source2:	lighttpd.conf
Source3:	httpd.conf
URL:		http://lam.sourceforge.net/
Patch0:		configdir.patch
Patch1:		loginbysearch.patch
Patch2:		%{name}-shadowAccount.patch
BuildRequires:	perl-base
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl-base
Requires:	php(core) >= 5.0
Requires:	php(gettext)
Requires:	php(hash)
Requires:	php(iconv)
Requires:	php(json)
Requires:	php(ldap)
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(spl)
Requires:	php(xml)
Requires:	php(zip)
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_phpdocdir	%{_docdir}/phpdoc

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

%description -l de.UTF-8
LDAP Account Manager (LAM) läuft auf einem exisierenden Webserver. LAM
verwaltet Benutzer, Gruppen und Hosts. Zur Zeit werden folgende
Account-Typen unterstützt: Samba 3, Unix, Kolab 2, Addressbuch
Einträge, NIS mail Aliase und MAC-Addressen. Es gibt eine Baumansicht
mit der man die LDAP-Daten direkt bearbeiten kann. Zum Anlegen von
Accounts können Vorlagen definiert werden. Es können mehrere
Konfigurations-Profile definiert werden. Account-Informationen können
als PDF exportiert werden. Außerdem exisitiert ein Script mit dem man
Quotas und Home-Verzeichnisse verwalten kann.

%package lamdaemon
Summary:	Quota and home directory management for LDAP Account Manager
Summary(de.UTF-8):	Verwaltung von Quotas und Heimatverzeichnissen für LDAP Account Manager
Group:		Applications/WWW
Requires:	perl-base
Requires:	sudo

%description lamdaemon
Lamdaemon is part of LDAP Account Manager. This package needs to be
installed on the server where the home directories reside and/or
quotas should be managed.

%description lamdaemon -l de.UTF-8
Lamdaemon ist Teil von LDAP Account Manager. Dieses Paket wird auf dem
Server installiert, auf dem Quotas und Heimatverzeichnisse verwaltet
werden sollen.

%package phpdoc
Summary:	Online manual for LDAP Account Manager
Summary(pl.UTF-8):	Dokumentacja online do LDAP Account Manager
Group:		Documentation
Requires:	php-dirs

%description phpdoc
Documentation for LDAP Account Manager.

%description phpdoc -l pl.UTF-8
Dokumentacja do LDAP Account Manager.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cp -p config/config.cfg{_sample,}
cp -p config/lam.conf{_sample,}
mv config/*_sample .

find -name .htaccess | xargs rm

rm COPYING Makefile.in configure install.sh

rm locale/*/LC_MESSAGES/*.po

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_phpdocdir}/%{name}} \
	$RPM_BUILD_ROOT{/var/lib/%{name}/{sess,tmp},%{_sbindir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}

# daemon
mv $RPM_BUILD_ROOT%{_appdir}/lib/lamdaemon.pl $RPM_BUILD_ROOT%{_sbindir}

# config
mv $RPM_BUILD_ROOT{%{_appdir}/config/*,%{_sysconfdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

# apidocs
mv $RPM_BUILD_ROOT{%{_appdir}/docs/devel,%{_phpdocdir}/%{name}/devel}
mv $RPM_BUILD_ROOT{%{_appdir}/docs/manual,%{_phpdocdir}/%{name}/manual}

# in %doc, or otherwise unneeded
rm $RPM_BUILD_ROOT%{_appdir}/{HISTORY,README,copyright,configure.ac}

rm -rf $RPM_BUILD_ROOT%{_appdir}/{sess,tmp}
ln -s /var/lib/%{name}/sess $RPM_BUILD_ROOT%{_appdir}/sess
ln -s /var/lib/%{name}/tmp $RPM_BUILD_ROOT%{_appdir}/tmp

%pretrans
# migrate dir to symlinks, don't worry about permissions, those be handled by rpm
if [ -d %{_appdir}/sess -a ! -L %{_appdir}/sess ]; then
	install -d /var/lib/%{name}/sess
	mv %{_appdir}/sess/* /var/lib/%{name}/sess 2>/dev/null
	rm -rf %{_appdir}/sess
	ln -sf /var/lib/%{name}/sess %{_appdir}/sess
fi
if [ -d %{_appdir}/tmp -a ! -L %{_appdir}/tmp ]; then
	install -d /var/lib/%{name}/tmp
	mv %{_appdir}/tmp/* /var/lib/%{name}/tmp 2>/dev/null
	rm -rf %{_appdir}/tmp
	ln -sf /var/lib/%{name}/tmp %{_appdir}/tmp
fi
exit 0

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY README copyright
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.cfg
%attr(660,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lam.conf
#%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/passwordMailTemplate.txt
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/shells
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/language
%dir %attr(750,root,http) %{_sysconfdir}/pdf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pdf/default.*.xml
%dir %attr(750,root,http) %{_sysconfdir}/pdf/logos
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pdf/logos/*.jpg
%dir %attr(750,root,http) %{_sysconfdir}/profiles
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/profiles/default.*
%dir %attr(750,root,http) %{_sysconfdir}/selfService
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/selfService/default.*

%dir %{_appdir}
%{_appdir}/VERSION
%{_appdir}/*_sample
%{_appdir}/graphics
%{_appdir}/help
%{_appdir}/lib
%{_appdir}/style
%{_appdir}/templates
%{_appdir}/index.html

%dir %{_appdir}/locale
# XXX: verify language codes
%lang(ca_ES) %{_appdir}/locale/ca_ES
%lang(cs) %{_appdir}/locale/cs_CZ
%lang(de) %{_appdir}/locale/de_DE
%lang(es) %{_appdir}/locale/es_ES
%lang(fr) %{_appdir}/locale/fr_FR
%lang(hu) %{_appdir}/locale/hu_HU
%lang(it) %{_appdir}/locale/it_IT
%lang(ja) %{_appdir}/locale/ja_JP
%lang(nl) %{_appdir}/locale/nl_NL
%lang(pl) %{_appdir}/locale/pl_PL
%lang(pt_BR) %{_appdir}/locale/pt_BR
%lang(ru) %{_appdir}/locale/ru_RU
%lang(zh_CN) %{_appdir}/locale/zh_CN
%lang(zh_TW) %{_appdir}/locale/zh_TW
%lang(sk) %{_appdir}/locale/sk_SK

%dir %dir %attr(750,root,http) /var/lib/%{name}
%dir %attr(770,root,http) /var/lib/%{name}/sess
%dir %attr(770,root,http) /var/lib/%{name}/tmp
# symlinks to /var/lib/...
%{_appdir}/sess
%{_appdir}/tmp

%files lamdaemon
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lamdaemon.pl

%files phpdoc
%defattr(644,root,root,755)
%{_phpdocdir}/%{name}
