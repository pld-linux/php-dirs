#!/bin/sh

[ -x /usr/sbin/tmpwatch ] || exit 0

session_dirs="/var/run/php /var/run/php-ug"

# use tmpwatch with --test to remove only files matching to 'sess_*' pattern
cleanup_dir() {
	local session_dir=$1

	test -d "$session_dir" || return

	/usr/sbin/tmpwatch $gc_time $session_dir --test | while read action type file; do
		case "$action $type $file" in
		'removing file '*/sess_*)
			rm "$file"
			;;
		esac
	done
}

# find minimum gc time from any of the php engines
find_gc_time() {
	gc_time=0
	local gc php
	for php in php $(cd /etc && ls -1d php[0-9] php[0-9][0-9] 2> /dev/null); do
		gc=
		if [ -x /usr/bin/$php ]; then
			gc=$($php -r 'echo max(round(ini_get("session.gc_maxlifetime")/3600), 1);' 2> /dev/null)
		elif [ -r /etc/$php/php.ini ]; then
			gc=$(awk -F"=" '/^session.gc_maxlifetime[ \t]*=/ { t=sprintf("%d", ($2/3600)); if (t<1) { t=1; }; print t; exit;}' /etc/$php/php.ini)
		fi
		[ -n "$gc" ] || continue

		if [ "$gc" -lt "$gc_time" ] || [ $gc_time -eq 0 ]; then
			gc_time=$gc
		fi
	done
}

find_gc_time
[ $gc_time -gt 0 ] || exit 0

for session_dir in $session_dirs; do
	cleanup_dir $session_dir
done

exit 0
