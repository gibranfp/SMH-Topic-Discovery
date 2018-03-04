#/usr/bin/env python
# -*- coding: utf-8
#
# Gibran Fuentes-Pineda <gibranfp@unam.mx>
# IIMAS, UNAM
# 2017
#
# -------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------
"""
Plots probability of collision as a function of co-occurrence
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import log, pow

def get_number_of_tables(r, jcc):
    """
    Computes number of tables from co-occurrence threshold and tuples size
    """
    return int(round(log(0.5) / log(1 - jcc**r)))
    
def collision_probability(s, r, l):
    """
    Collision probability
    """
    return 1 - (1 - s**r)**l

def plot_tuple_collision(tuple_size = [(1, 'crimson'), (2, 'lightblue'), (3, 'goldenrod'), (6, 'coral'), (9, 'teal')]):
    """
    Plots Min-Hashing probability of collision for different tuples sizes
    """
    plt.figure(1)
    jcc = np.linspace(0, 1, num = 1000)
    for r in tuple_size:
        plt.plot(jcc, jcc**r[0], c = r[1], label = "r = " + str(r[0]))

    plt.xlabel("$JCC_B(B_1, B_2, \ldots, B_k)$")
    plt.ylabel("$P(g(B_1) = g(B_2) = \cdots = g(B_k))$")
    plt.grid()
    plt.legend()
    plt.savefig('mh_tuple_collision.pdf')

def plot_unit_filter(jcc_thres = [(0.2, '-'), (0.6, '--')], \
                     tuple_size = [(3, 'goldenrod'), (6, 'coral'), (9, 'teal')]):
    """
    Plots Min-Hashing probability of collision for different tuples sizes,
    co-occurrence thresholds and co-occurrence values 
    """
    plt.figure(2)
    jcc = np.linspace(0, 1, num = 1000)
    for i,j in enumerate(jcc_thres):
        for k,r in enumerate(tuple_size):
            l = get_number_of_tables(r[0], j[0])
            plt.plot(jcc, collision_probability(jcc, r[0], l), c = r[1], ls = j[1], \
                     label = "r = " + str(r[0]) + ", l = " + str(l))

    plt.xlabel("$JCC_B(B_1, B_2 \ldots, B_k)$")
    plt.ylabel("$P_{collision}(B_1, B_2, \ldots, B_k)$")
    plt.grid()
    plt.legend()
    plt.savefig('mh_unit_filter.pdf')

def main():
    plot_tuple_collision()
    plot_unit_filter()

if __name__ == "__main__":
    main()
