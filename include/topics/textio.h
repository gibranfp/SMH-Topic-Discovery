/**
 * @file textio.h
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
 * @brief Declaration of structures for handling text corpora
 */
#ifndef TEXTIO_H
#define TEXTIO_H

#include <smh/listdb.h>

typedef struct TermInfo {
     char *term;
     uint id;
     uint corpfreq;
     uint docfreq;
} TermInfo;

typedef struct Vocabulary {
     TermInfo *terms;
     uint size;
} Vocabulary;

void textio_vocabulary_init(Vocabulary *);
void textio_vocabulary_print(Vocabulary *);
void textio_vocabulary_push(Vocabulary *, TermInfo);
Vocabulary textio_vocabulary_load_from_file(char *);
void textio_vocabulary_save_to_file(char *, Vocabulary *);
void textio_print_idlist_as_words(List *, Vocabulary *);
void textio_print_idlistdb_as_words(ListDB *, Vocabulary *);
void textio_save_idlistdb_as_words(char *, ListDB *, Vocabulary *);
#endif
