/**
 * @file topics.c
 * @author Gibran Fuentes Pineda <gibranfp@turing.iimas.unam.mx>
 * @date 2014
 *
 * @section GPL
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details at
 * http://www.gnu.org/copyleft/gpl.html
 *
 * @brief Definition of structures for handling lists and inverted file structures.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "topics.h"

/**
 * @brief Retrives documents containing a specific topic from a database
 *
 * @param ifindex Inverted file index
 * @param topic Topic to be searched
 */
List topics_retrieve_docs(ListDB *ifindex, List *topic)
{
	return ifindex_query(ifindex, topic);
}

/**
 * @brief Retrieves documents for each given topic from a database
 *
 * @param ifindex Inverted file index
 * @param topics Database of topics to be searched
 */
ListDB topics_retrieve_all_docs(ListDB *ifindex, ListDB *topics)
{
	return ifindex_query_multi(ifindex, topics);
}

/* /\** */
/*  * @brief Ranks a database of documents by relevance */
/*  * */
/*  * @param ifindex Inverted file index */
/*  * @param docs Database of documents given as lists */
/*  * @param topics Database of topics to be searched */
/*  *\/ */
/* void topics_compute_score(ListDB *topics, ListDB *corpus, ListDB *ifindex, */
/*                           double (*func)(ListDB *, ListDB *, ListDB, List *, List *, List *, List *)) */
/* { */
     
/* } */

/* /\** */
/*  * @brief Ranks a database of documents by score */
/*  * */
/*  * @param ifindex Inverted file index */
/*  * @param docs Database of documents given as lists */
/*  * @param topics Database of topics to be searched */
/*  * @param func Function to compute score */
/*  *\/ */
/* void topics_rank_by_score(ListDB *topics, ListDB *corpus, ListDB *ifindex, */
/*                           double (*func)(ListDB *, ListDB *, ListDB, List *, List *, List *, List *)) */
/* { */
     
/* } */
