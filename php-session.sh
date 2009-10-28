#!/bin/sh
if [ -x /usr/bin/php ] ; then
	RUNTIME5=$(/usr/bin/php -r '$t = round(ini_get("session.gc_maxlifetime")/3600); if ($t<1) $t=1; echo $t;' 2> /dev/null)
elif [ -r /etc/php/php.ini ]; then
	RUNTIME5=$(awk -F"=" '/^session.gc_maxlifetime[ \t]*=/ { t=sprintf("%d", ($2/3600)); if (t<1) { t=1; }; print t; exit;}' /etc/php/php.ini)
fi

if [ -x /usr/bin/php4 ] ; then
	RUNTIME4=$(/usr/bin/php4 -r '$t = round(ini_get("session.gc_maxlifetime")/3600); if ($t<1) $t=1; echo $t;' 2> /dev/null)
elif [ -r /etc/php4/php.ini ]; then
	RUNTIME4=$(awk -F"=" '/^session.gc_maxlifetime[ \t]*=/ { t=sprintf("%d", ($2/3600)); if (t<1) { t=1; }; print t; exit;}' /etc/php4/php.ini)
fi

[ -z "$RUNTIME5" ] && RUNTIME5="1h"

if [ -n "$RUNTIME5" ]; then
	/usr/sbin/tmpwatch ${RUNTIME5} /var/run/php
fi

if [ -n "$RUNTIME4" -a "$RUNTIME5" != "$RUNTIME4" ]; then
	/usr/sbin/tmpwatch ${RUNTIME4} /var/run/php
fi
