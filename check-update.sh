#!/bin/sh
curl "https://github.com/Microsoft/cpprestsdk/tags" 2>/dev/null |grep "tag/v" |sed -e 's,.*tag/v,,;s,\".*,,;' |head -n1

