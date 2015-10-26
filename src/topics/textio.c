#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "textio.h"

/**
 * @brief Initializes a vocabulary structure
 *
 * @param vocabulary Vocabulary to be initialized
 */
void textio_vocabulary_init(Vocabulary *vocabulary)
{
     vocabulary->size = 0;
     vocabulary->terms = NULL;
}

/**
 * @brief Prints a vocabulary structure
 *
 * @param vocabulary Vocabulary to be initialized
 */
void textio_vocabulary_print(Vocabulary *vocabulary)
{
     uint i;
     for (i = 0; i < vocabulary->size; i++) {
          printf("%s = %u = %u %u\n",
                 vocabulary->terms[i].term,
                 vocabulary->terms[i].id,
                 vocabulary->terms[i].corpfreq,
                 vocabulary->terms[i].docfreq);
     }
}


/**
 * @brief Adds a new term to the end of a vocabulary
 *
 * @param vocabulary Vocabulary where the term will be added
 * @param term Term to be added
 */
void textio_vocabulary_push(Vocabulary *vocabulary, TermInfo term)
{
     uint newsize = vocabulary->size + 1;

     vocabulary->terms = realloc(vocabulary->terms, newsize * sizeof(TermInfo));
     vocabulary->terms[vocabulary->size] = term;
     vocabulary->size = newsize;
}

/**
 * @brief Reads vocabulary in NIPS format:
 *             term1 = id1 = termfreq1 termdocfreq1
 *                        ...
 *
 * @param filename File with the vocabulary
 * @param vocab Vocabulary
 * @param termod Term ids
 * @param corpfreq Number of times the term appears in the corpus
 * @param docfreq Number of documents where the term appears
 * @param vocsize Number of terms in the vocabulary
 */
Vocabulary textio_vocabulary_load_from_file(char *filename)
{
     FILE *file;
     file = fopen(filename, "r");
     if (file == NULL){
          fprintf(stderr,"Could not open file %s\n", filename);
          exit(EXIT_FAILURE);
     }
     
     char *line = NULL;
     char *token;
     size_t len = 0;
     ssize_t read;
     Vocabulary vocabulary;
     textio_vocabulary_init(&vocabulary);
     while ((read = getline(&line, &len, file)) != -1){
          // term
          token = strtok (line, " = ");
          TermInfo terminfo;
          terminfo.term = (char *) malloc((strlen(token) + 1) * sizeof(char));
          strcpy(terminfo.term, token);

          // term id
          token = strtok (NULL, " = ");
          terminfo.id = atoi(token);
      
          // number of times the term appears in the corpus
          token = strtok (NULL, " = ");
          terminfo.corpfreq = atoi(token);
      
          // number of documents the term appears in the corpus
          token = strtok (NULL," ");
          terminfo.docfreq = atoi(token);

          textio_vocabulary_push(&vocabulary, terminfo);
     }
   
     free(line);

     if (fclose(file)) {
          fprintf(stderr,"Error: Could not close file %s\n", filename);
          exit(EXIT_FAILURE);
     }

     return vocabulary;
}

/**
 * @brief Saves a vocabulary in the following format:
 *             term1 = id1 = termfreq1 termdocfreq1
 *                        ...
 *
 * @param filename Name of the file where the vocabulary is to be saved
 * @param vocab Vocabulary
 */
void textio_vocabulary_save_to_file(char *filename, Vocabulary *vocabulary)
{
     FILE *file;     
     if (!(file = fopen(filename,"w"))) {
          fprintf(stderr,"Error: Could not create file %s\n", filename);
          exit(EXIT_FAILURE);
     }

     uint i;
     for (i = 0; i < vocabulary->size; i++) {
          fprintf(file, "%s = %u = %u %u\n",
                  vocabulary->terms[i].term,
                  vocabulary->terms[i].id,
                  vocabulary->terms[i].corpfreq,
                  vocabulary->terms[i].docfreq);
     }

     if (fclose(file)) {
          fprintf(stderr,"Error: Could not close file %s\n", filename);
          exit(EXIT_FAILURE);
     }
}

/**
 * @brief Prints a list of ids as a word list
 *
 * @param id_list List of ids
 * @param vocabulary Vocabulary
 */
void textio_print_idlist_as_words(List *id_list, Vocabulary *vocabulary)
{
     uint i;
     for (i = 0; i < id_list->size; i++)
          printf ("%s ", vocabulary->terms[id_list->data[i].item].term);
}

/**
 * @brief Prints a database of id lists as word lists
 *
 * @param id_list List of ids
 * @param vocabulary Vocabulary
 */
void textio_print_idlistdb_as_words(ListDB *id_lists, Vocabulary *vocabulary)
{
     uint i;
     for (i = 0; i < id_lists->size; i++){
          textio_print_idlist_as_words(&id_lists->lists[i], vocabulary);
          printf ("\n");
     }    
}

/**
 * @brief Saves a database of id lists as word lists
 *
 * @param filename File where the word lists will be saved
 * @param id_lists ID lists
 * @param vocabulary Vocabulary
 */
void textio_save_idlistdb_as_words(char *filename, ListDB *id_lists, Vocabulary *vocabulary)
{
     FILE *file;     
     if (!(file = fopen(filename,"w"))){
          fprintf(stderr,"Error: Could not create file %s\n", filename);
          exit(EXIT_FAILURE);
     }
     
     uint i, j;
     for (i = 0; i < id_lists->size; i++){
          for (j = 0; j < id_lists->lists[i].size; j++)
               fprintf (file, "%s[%d] ", vocabulary->terms[id_lists->lists[i].data[j].item].term, 
                        id_lists->lists[i].data[j].freq);
          fprintf (file, "\n");
     }

     if (fclose(file)){
          fprintf(stderr,"Error: Could not close file %s\n", filename);
          exit(EXIT_FAILURE);
     }
}
