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


function run_exp {
	name=$1
	mkdir -p exps/wiki$1
	mkdir -p exps/wiki$1/models
	mkdir -p exps/wiki$1/topics

	check data/wikipedia/wiki${name}.tf.ifs
	if [ "$ANS" == "yes" ]; then
	smhcmd ifindex\
		data/wikipedia/wiki${name}.corpus\
		data/wikipedia/wiki${name}.tf.ifs
	fi

	check data/wikipedia/wiki${name}.bin.ifs
	if [ "$ANS" == "yes" ]; then
	smhcmd ifindex -w 1\
		data/wikipedia/wiki${name}.corpus\
		data/wikipedia/wiki${name}.bin.ifs
	fi

	check exps/wikipedia/topics/wiki${name}.topics
	if [ "$ANS" == "yes" ]; then
	time python python/mine.py\
		--model_pref exps/wiki$1/models/wiki${name}_\
		--topics_pref exps/wiki$1/topics/wiki${name}_\
		--clus --min_cluster_size 2\
		--min_coherence 2.0\
		--cutoff 3\
		--thres 0.6\
		-p 2 0.2\
		-p 2 0.15\
		-p 2 0.10\
		--voca en data/wikipedia/wiki.en.vocab\
		--voca es data/wikipedia/wiki.en.es.vocab\
		--voca de data/wikipedia/wiki.en.de.vocab\
		--voca cy data/wikipedia/wiki.en.cy.vocab\
		--voca fa data/wikipedia/wiki.en.fa.vocab\
		--voca fr data/wikipedia/wiki.en.fr.vocab\
		--voca he data/wikipedia/wiki.en.he.vocab\
		--voca it data/wikipedia/wiki.en.it.vocab\
		--voca pl data/wikipedia/wiki.en.pl.vocab\
		--voca ru data/wikipedia/wiki.en.ru.vocab\
		--voca pt data/wikipedia/wiki.en.pt.vocab\
		--voca el data/wikipedia/wiki.en.el.vocab\
		data/wikipedia/wiki${name}.tf.ifs\
		data/wikipedia/wiki${name}.tf.ifs
	fi
}


run_exp ".en.full"

