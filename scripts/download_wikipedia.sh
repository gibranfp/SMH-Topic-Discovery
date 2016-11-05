#!/bin/bash

function check {
	ANS='yes'
	echo $1
	if [ -f $1 ]; then
		read -r -p "${1} exists, $2? [y/N] " response
		if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
		then
			ANS='yes'
		else
			ANS='no'
		fi
	fi
}


function download {
	LANG=$1
	DATE=$2
	check data/wikipedia/wiki${LANG}.page.sql.gz "should i download again"
	if [ "$ANS" == "yes" ]; then
		wget -O data/wikipedia/wiki${LANG}.page.sql.gz https://dumps.wikimedia.org/${LANG}wiki/${DATE}/${LANG}wiki-${DATE}-page.sql.gz
		gunzip -c data/wikipedia/wiki${LANG}.page.sql.gz > data/wikipedia/wiki${LANG}.page.sql
	fi

	check data/wikipedia/wiki${LANG}.links.gz  "should i download again"
	if [ "$ANS" == "yes" ]; then
		wget -O data/wikipedia/wiki${LANG}.links.gz https://dumps.wikimedia.org/${LANG}wiki/${DATE}/${LANG}wiki-${DATE}-langlinks.sql.gz
		gunzip -c data/wikipedia/wiki${LANG}.links.gz > data/wikipedia/wiki${LANG}.links.sql
	fi

	check data/wikipedia/wiki${LANG}.articles.bz2 "should i download again"
	if [ "$ANS" == "yes" ]; then
		wget -O data/wikipedia/wiki${LANG}.articles.bz2 https://dumps.wikimedia.org/${LANG}wiki/${DATE}/${LANG}wiki-${DATE}-pages-articles.xml.bz2
	fi

	check data/wikipedia/wiki${LANG}.xml
	if [ "$ANS" == "yes" ]; then
		mkdir extracted
		python python/WikiExtractor.py --no-templates  -cb 1M -o extracted  data/wikipedia/wiki${LANG}.articles.bz2
		find extracted -name '*.bz2' -exec bzip2 -d -c {} \; > data/wikipedia/wiki${LANG}.xml
		rm -rf extracted
	fi
}


#download en 20160501
#download es 20160501
#download de 20160501
#download cy 20160501
#download fa 20160501
#download fi 20160501
#download fr 20160501
#download he 20160501
#download it 20160501
#download pl 20160501
#download ru 20160501
download pt 20160501
#download el 20160501




