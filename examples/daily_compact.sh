#!/bin/sh
DAY=`date +"%Y%m%d" -d "60 minutes ago"`

./xap_compact ${DAY}.db
