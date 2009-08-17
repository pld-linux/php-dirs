#!/bin/sh
if [ -x /usr/bin/php.cli ] ; then
	RUNTIME5=$(/usr/bin/php.cli -r 'echo 1+(int)(ini_get("session.gc_maxlifetime")/3600);' 2> /dev/null)
elif [ -r /etc/php/php.ini ]; then
	RUNTIME5=$(awk -F"=" '/^session.gc_maxlifetime[[:space:]]*=/ { t=sprintf("%d", 1+($2/3600)); print t;}' /etc/php/php.ini)
fi

if [ -x /usr/bin/php4.cli ] ; then
	RUNTIME4=$(/usr/bin/php4.cli -r 'echo 1+(int)(ini_get("session.gc_maxlifetime")/3600);' 2> /dev/null)
elif [ -r /etc/php4/php.ini ]; then
	RUNTIME4=$(awk -F"=" '/^session.gc_maxlifetime[[:space:]]*=/ { t=sprintf("%d", 1+($2/3600)); print t;}' /etc/php4/php.ini)
fi

[ -z "$RUNTIME5" ] && RUNTIME5="1h"

if [ -n "$RUNTIME5" ]; then
	/usr/sbin/tmpwatch ${RUNTIME5} /var/run/php
fi

if [ -n "$RUNTIME4" -a "$RUNTIME5" != "$RUNTIME4" ]; then
	/usr/sbin/tmpwatch ${RUNTIME4} /var/run/php
fi
