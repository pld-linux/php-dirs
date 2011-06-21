Summary:	Common dirs for different PHP versions
Summary(pl.UTF-8):	Wspólne katalogi dla różnych wersji PHP
Name:		php-dirs
Version:	1.2
Release:	1
License:	GPL
Group:		Base
Source0:	php-session.sh
BuildRequires:	rpmbuild(macros) >= 1.461
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
install -d $RPM_BUILD_ROOT{%{php_data_dir}/tests,/etc/cron.hourly,/var/run/php}
install -d $RPM_BUILD_ROOT%{_docdir}/phpdoc

install %{SOURCE0} $RPM_BUILD_ROOT/etc/cron.hourly

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
%dir %{php_data_dir}
%dir %{php_data_dir}/tests
%dir %{_docdir}/phpdoc
# http needs only x for directory (otherwise it knows session file
# names and can read it contents)
%attr(730,root,http) %dir %verify(not group mode) /var/run/php
%attr(755,root,root) %{_sysconfdir}/cron.hourly/php-session.sh
