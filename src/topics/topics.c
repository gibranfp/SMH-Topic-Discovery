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

/**
 * @brief Computes scores of a database of topics
 *
 * @param topics Database of topics
 * @param corpus Database of documents
 */
Score *topics_document_score(ListDB *topics, ListDB *corpus)
{
     uint i, j;
     Score *scores = (Score *) malloc(topics->size * sizeof(Score));
     
     for (i = 0; i < topics->size; i++) {
          scores[i].value = 0.0;
          scores[i].index = i;
          for (j = 0; j < corpus->size; j++){
               uint inter = list_intersection_size(&topics->lists[i], &corpus->lists[j]) + 1;
               double prob = (double) inter / corpus->lists[j].size;
               scores[i].value += 
          }
     }

     return scores;
}

/**
 * @brief Computes scores of a database of topics
 *
 * @param topics Database of topics
 * @param corpus Database of documents
 */
double *topics_mean_distances(ListDB *topics)
{
     uint i, j;
     double *mean_dist = malloc(topics->size * sizeof(double));
     
     for (i = 0; i < topics->size; i++) {
          double topic_dist = 0.0;
          for (j = 0; j < topics->size; j++)
               topic_dist += 1.0 - list_jaccard(&topics->lists[i], &topics->lists[j]);

          mean_dist[i] = topic_dist / topics->size;
     }

     mean_dist;
}

/**
 * @brief Computes scores of a database of topics
 *
 * @param topics Database of topics
 * @param corpus Database of documents
 */
double *topics_min_distances(ListDB *topics)
{
     uint i, j;
     double *min_dist = malloc(topics->size * sizeof(double));
     
     for (i = 0; i < topics->size; i++) {
          min_dist[i] = 1.0;
          for (j = 1; j < topics->size; j++){
               if (i != j) {
                    double topic_dist = 1.0 - list_jaccard(&topics->lists[i], &topics2->lists[j]);
                    if (min_dist[i] > topic_dist)
                         min_dist[i] = topic_dist;
               }
          }
     }
     
     return min_dist;
}
