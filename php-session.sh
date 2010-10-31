#!/bin/sh

[ -x /usr/sbin/tmpwatch ] || exit

if [ -x /usr/bin/php ]; then
	RUNTIME5=$(/usr/bin/php -r '$t = round(ini_get("session.gc_maxlifetime")/3600); if ($t<1) $t=1; echo $t;' 2> /dev/null)
elif [ -r /etc/php/php.ini ]; then
	RUNTIME5=$(awk -F"=" '/^session.gc_maxlifetime[ \t]*=/ { t=sprintf("%d", ($2/3600)); if (t<1) { t=1; }; print t; exit;}' /etc/php/php.ini)
fi

if [ -x /usr/bin/php4 ]; then
	RUNTIME4=$(/usr/bin/php4 -r '$t = round(ini_get("session.gc_maxlifetime")/3600); if ($t<1) $t=1; echo $t;' 2> /dev/null)
elif [ -r /etc/php4/php.ini ]; then
	RUNTIME4=$(awk -F"=" '/^session.gc_maxlifetime[ \t]*=/ { t=sprintf("%d", ($2/3600)); if (t<1) { t=1; }; print t; exit;}' /etc/php4/php.ini)
fi

[ -z "$RUNTIME5" ] && [ -z "$RUNTIME4" ] && exit

[ "${RUNTIME4:-0}" -ge "${RUNTIME5:-0}" ] && RUNTIME=$((RUNTIME4)) || RUNTIME=$((RUNTIME5))

/usr/sbin/tmpwatch ${RUNTIME} /var/run/php
