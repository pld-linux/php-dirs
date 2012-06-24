Summary:	Common dirs for different PHP versions
Summary(pl):	Wsp�lne katalogi dla r�nych wersji PHP
Name:		php-dirs
Version:	0.9
Release:	0.1
License:	GPL
Group:		Base
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Provides:	group(http)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_tmpwatchdir	/etc/tmpwatch

%description
Common directories for PHP version 4 and version 5.

%description -l pl
Wsp�lne katalogi dla PHP w wersji 4 oraz 5.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/php,/var/run/php,%{_tmpwatchdir}}

echo '/var/run/php 720' > $RPM_BUILD_ROOT%{_tmpwatchdir}/php.conf

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
%dir %{_datadir}/php
%attr(770,root,http) %dir %verify(not group mode) /var/run/php
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_tmpwatchdir}/php.conf
