#!/bin/sh
orig="$1"
tmp=tmp_$$.db
tmp2=tmp2_$$.db

if [ -e $orig/.compacted ] ; then
    exit 0
fi

xapian-compact -F $orig $tmp && mv $orig $tmp2 && mv $tmp $orig && rm -rf $tmp2 && touch $orig/.compacted
