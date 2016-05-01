# TODO
# - move tmpwatch S: to php-session package (as session files file storage no
#   longer can cleanup itself due dir perms)
Summary:	Common dirs for PHP
Summary(pl.UTF-8):	Wspólne katalogi dla PHP
Name:		php-dirs
Version:	1.7
Release:	1
License:	GPL
Group:		Base
Source0:	php-session.sh
Source1:	%{name}.tmpfiles
Source2:	crontab
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Suggests:	tmpwatch
Conflicts:	php-pear < 4:1.4-2
Provides:	group(http)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib

%description
Common directories for PHP.

%description -l pl.UTF-8
Wspólne katalogi dla PHP.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,/var/{cache,log,run}/php,/var/log/archive/php} \
	$RPM_BUILD_ROOT%{_docdir}/phpdoc \
	$RPM_BUILD_ROOT%{_libexecdir} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

install -p %{SOURCE0} $RPM_BUILD_ROOT%{_libexecdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/php-session

while read dir; do
	install -d $RPM_BUILD_ROOT$dir
done <<EOF
%{php_data_dir}/tests
%{php_data_dir}/Symfony/Bridge
%{php_data_dir}/Symfony/Component
EOF

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
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/php-session
%{systemdtmpfilesdir}/%{name}.conf
%attr(755,root,root) %{_libexecdir}/php-session.sh
%{php_data_dir}

%dir %{_docdir}/phpdoc
%attr(775,root,http) %dir %verify(not group mode) /var/log/php
%attr(770,root,root) %dir %verify(not group mode) /var/log/archive/php

# no +r, so only predictable names can be used. currently php-soap wsdl cache is there
%attr(730,root,http) %dir %verify(not group mode) /var/cache/php

# http needs only +x for directory
# (otherwise it knows session file names and can read it contents)
# keep o+x for fcgi.sock (lighttpd)
%attr(731,root,http) %dir %verify(not group mode) /var/run/php
