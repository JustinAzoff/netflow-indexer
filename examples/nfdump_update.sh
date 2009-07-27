#!/bin/sh

DAY=`date +"%Y%m%d" -d "60 minutes ago"`

netflow-index-update -i nfdump  /data/nfdump_xap /data/nfsen/profiles/live/podium/nfcapd.${DAY}*
