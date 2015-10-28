#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <smh/listdb.h>
#include "textio.h"
#include "topics.h"

#define red "\033[0;31m"
#define cyan "\033[0;36m"
#define green "\033[0;32m"
#define blue "\033[0;34m"
#define brown "\033[0;33m"
#define magenta "\033[0;35m"
#define none "\033[0m"

#define MAX_LIST_SIZE 10
#define ELEMENT_MAX_VALUE 15

/* uint topics_sort_partition(ListDB *topics, double *coef, uint left, uint right) */
/* { */
/* 	double pval = coef[right]; */
/* 	uint i = left, j; */
/* 	for (j = left; j < right; j++){ */
/* 		if (coef[j] >= pval){ */
/* 			List tmp = topics->lists[i]; */
/* 			topics->lists[i] = topics->lists[j]; */
/* 			topics->lists[j] = tmp; */
/* 			double tmpcoef = coef[i]; */
/* 			coef[i] = coef[j]; */
/* 			coef[j] = tmpcoef; */
/* 			i++; */
/* 		} */
/* 	} */

/* 	List tmp = topics->lists[i]; */
/* 	topics->lists[i] = topics->lists[right]; */
/* 	topics->lists[right] = tmp; */
/* 	double tmpcoef = coef[i]; */
/* 	coef[i] = coef[right]; */
/* 	coef[right] = tmpcoef; */
/* } */

/* void topics_sort_custom(ListDB *topics, double *coef, uint left, uint right) */
/* { */
/* 	int pivot; */
     
/* 	if (left < right){ */
/* 		pivot = topics_sort_partition(topics, coef, left, right); */
/* 		topics_sort_custom(topics, coef, left, pivot - 1); */
/* 		topics_sort_custom(topics, coef, pivot + 1, right); */
/* 	} */
	 
/* } */

void rank_topic(char *ifname, char *topicname)
{
	uint i, j;
	ListDB ifindex = listdb_load_from_file(ifname);
	ListDB topics = listdb_load_from_file(topicname);
	double *coef = (double *) calloc(topics.size, sizeof(double));
     
	for (i = 0; i < topics.size; i++)
	{
		if (topics.lists[i].size > 1){
			double topic_jaccard = 0.0;
			double topic_inter = 0.0;
			uint ref = topics.lists[i].data[0].item;
			for (j = 1; j <= 100 && j < topics.lists[i].size; j++){
				uint term = topics.lists[i].data[j].item;;

				uint inter = list_intersection_size(&ifindex.lists[ref],
                                                &ifindex.lists[term]);
				topic_jaccard += (double) list_jaccard(&ifindex.lists[ref],
                                                   &ifindex.lists[term]);
            topic_inter += (double)inter;
			}
			coef[i] = (double) topic_jaccard * (double) topic_inter * (double) topics.lists[i].size;
		}
		else
			coef[i] = 0.0;
	}

	char output[10000];
	strcpy (output, topicname);
	strcat (output,".scores");
	FILE *file;
	printf("Writing coefficients to %s . . . \n", output);
	file = fopen(output,"w");
	for (i = 0; i < topics.size; i ++)
		fprintf(file,"%lf\n", coef[i]);
	fclose(file);
}

void textio_vocabulary(char *input, char *output)
{
     Vocabulary voc = textio_vocabulary_load_from_file(input);
     textio_vocabulary_print(&voc);
     textio_vocabulary_save_to_file(output, &voc);
}

void textio_idlist(char *vocname, char *idname, char *output)
{
     ListDB idlists = listdb_load_from_file(idname);
     Vocabulary voc = textio_vocabulary_load_from_file(vocname);
     textio_print_idlistdb_as_words(&idlists, &voc);
     textio_save_idlistdb_as_words(output, &idlists, &voc);
}

int main(int argc, char **argv)
{
     //rank_topic(argv[1], argv[2]);
     /* textio_vocabulary(argv[1], argv[2]); */
     textio_idlist(argv[1], argv[2], argv[3]);
     
	return 0;
}
