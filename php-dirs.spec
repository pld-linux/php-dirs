Summary:	Common dirs for different PHP versions
Name:		php-dirs
Version:	0.9
Release:	0.1
License:	GPL
Group:		Base
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpsharedir	%{_datadir}/php

%description
Common directories for PHP version 4 and version 5.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/php,/var/run/php,/etc/tmpwatch}

echo '/var/run/php 720' > $RPM_BUILD_ROOT/etc/tmpwatch/php.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_datadir}/php
%attr(770,root,http) %dir %verify(not group mode) /var/run/php
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/php.conf
