# TODO
# - move tmpwatch S: to php-session package (as session files file storage no
#   longer can cleanup itself due dir perms)
Summary:	Common dirs for different PHP versions
Summary(pl.UTF-8):	Wspólne katalogi dla różnych wersji PHP
Name:		php-dirs
Version:	1.5
Release:	2
License:	GPL
Group:		Base
Source0:	php-session.sh
Source1:	%{name}.tmpfiles
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Suggests:	tmpwatch
Provides:	group(http)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common directories for PHP version 4 and version 5.

%description -l pl.UTF-8
Wspólne katalogi dla PHP w wersji 4 oraz 5.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_data_dir}/tests,/etc/cron.hourly,/var/{cache,log,run}/php,/var/log/archive/php} \
	$RPM_BUILD_ROOT%{_docdir}/phpdoc \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

install -p %{SOURCE0} $RPM_BUILD_ROOT/etc/cron.hourly
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 51 http

%postun
if [ "$1" = "0" ]; then
	%groupremove http
fi

%files
%defattr(644,root,root,755)
%{systemdtmpfilesdir}/%{name}.conf
%attr(755,root,root) %{_sysconfdir}/cron.hourly/php-session.sh
%dir %{php_data_dir}
%dir %{php_data_dir}/tests
%dir %{_docdir}/phpdoc
%attr(775,root,http) %dir %verify(not group mode) /var/log/php
%attr(770,root,root) %dir %verify(not group mode) /var/log/archive/php
# no +r, so only predictable names can be used. currently php-soap wsdl cache is there
%attr(730,root,http) %dir %verify(not group mode) /var/cache/php
# http needs only x for directory (otherwise it knows session file
# names and can read it contents)
# keep o+x for fcgi.sock (lighttpd)
%attr(731,root,http) %dir %verify(not group mode) /var/run/php
