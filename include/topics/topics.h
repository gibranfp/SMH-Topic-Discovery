/**
 * @file topics.h
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
 * @brief Declaration of structures for handling lists and inverted file structures.
 */
#ifndef TOPICS_H
#define TOPICS_H
#include <smh/ifindex.h>

List topics_retrieve_docs(ListDB *, List *);
ListDB topics_retrieve_all_docs(ListDB *, ListDB *);
#endif
