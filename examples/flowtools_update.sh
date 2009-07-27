#!/bin/sh

LOCALBIN=/usr/local/bin
FLOWPATH=/usr/local/var/db/flows/packeteer
DBPATH=/usr/local/var/db/flows/nfi

YEAR=`date -v -1H +'%Y'`
MONTH=`date -v -1H +'%m'`
DAY=`date -v -1H +'%d'`
HOUR=`date -v -1H +'%H'`

cd ${DBPATH}
FILEGLOB=${FLOWPATH}/${YEAR}/${YEAR}-${MONTH}/${YEAR}-${MONTH}-${DAY}/ft-v05.${YEAR}-${MONTH}-${DAY}.${HOUR}'*'

${LOCALBIN}/netflow-index-flowtools ${FILEGLOB}

if [ ${HOUR} -eq "23" ]; then
    ORIGINALDB=${DBPATH}/${YEAR}-${MONTH}-${DAY}.db
    PRESERVEDB=${DBPATH}/PRESERVE_$$.db
    TEMPDB=${DBPATH}/TMP_$$.db
    ${LOCALBIN}/xapian-compact -F ${ORIGINALDB} ${TEMPDB} &&
    /bin/mv ${ORIGINALDB} ${PRESERVEDB} &&
    /bin/mv ${TEMPDB} ${ORIGINALDB} &&
    /bin/rm -rf ${TEMPDB} ${PRESERVEDB}
fi
