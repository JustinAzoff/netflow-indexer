#!/bin/sh
orig="$1"
tmp=tmp_$$.db
tmp2=tmp2_$$.db
quartzcompact -F $orig $tmp && mv $orig $tmp2 && mv $tmp $orig && rm -rf $tmp2
