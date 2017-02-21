#!/bin/bash

# needs the path of the experiments directory (exps)
if [ $# -eq 0 ]; then
      echo "Error: No arguments supplied"
      exit 1
fi

# needs the path of the experiments directory (exps)
if [ ! -d "$1" ]; then
      echo "Experiments directory $1 doesn't exist"
      exit 1
fi

mkdir -p figs

# plot for NIPS (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/nips_r3_l.pdf\
       $1/exp1/topics/nips_1_r_3_l_86.topics\
       $1/exp1/topics/nips_1_r_3_l_118.topics\
       $1/exp1/topics/nips_1_r_3_l_205.topics\
       $1/exp1/topics/nips_1_r_3_l_315.topics\
       $1/exp1/topics/nips_1_r_3_l_692.topics

# plot for NIPS (r = [2 3 4 5 6] and l = [315])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$r\$ (for \$l = 315\$)" \
       -l "2 3 4 5 6" \
       -p figs/nips_r_l315.pdf\
       $1/exp1/topics/nips_2_r_2_l_315.topics\
       $1/exp1/topics/nips_2_r_3_l_315.topics\
       $1/exp1/topics/nips_2_r_4_l_315.topics\
       $1/exp1/topics/nips_2_r_5_l_315.topics\
       $1/exp1/topics/nips_2_r_6_l_315.topics

# plot for NIPS (r = [2 3 4 5 6] and l = [16 86 432 2165 10830])
python python/utils/plot_coherences.py \
       -x "Different values of the parameters \$r\$ and \$l\$  (for \$s* = 0.2\$)" \
       -l "\$r=2,l=16\$ \$r=3,l=86\$ \$r=4,l=432\$ \$r=5,l=2165\$ \$r=6,l=10830\$" \
       -p figs/nips_r_l_s0.2.pdf\
       $1/exp1/topics/nips_3_r_2_l_16.topics\
       $1/exp1/topics/nips_3_r_3_l_86.topics\
       $1/exp1/topics/nips_3_r_4_l_432.topics\
       $1/exp1/topics/nips_3_r_5_l_2165.topics\
       $1/exp1/topics/nips_3_r_6_l_10830.topics

# plot for Reuters (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/reuters_r3_l.pdf\
       $1/exp1/topics/reuters_1_r_3_l_86.topics\
       $1/exp1/topics/reuters_1_r_3_l_118.topics\
       $1/exp1/topics/reuters_1_r_3_l_205.topics\
       $1/exp1/topics/reuters_1_r_3_l_315.topics\
       $1/exp1/topics/reuters_1_r_3_l_692.topics

# plot for Reuters (r = [2 3 4 5 6] and l = [315])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$r\$ (for \$l = 315\$)" \
       -l "2 3 4 5 6" \
       -p figs/reuters_r_l315.pdf\
       $1/exp1/topics/reuters_2_r_2_l_315.topics\
       $1/exp1/topics/reuters_2_r_3_l_315.topics\
       $1/exp1/topics/reuters_2_r_4_l_315.topics\
       $1/exp1/topics/reuters_2_r_5_l_315.topics\
       $1/exp1/topics/reuters_2_r_6_l_315.topics

# plot for Reuters (r = [2 3 4 5 6] and l = [16 86 432 2165 10830])
python python/utils/plot_coherences.py \
       -x "Different values of the parameters \$r\$ and \$l\$  (for \$s* = 0.2\$)" \
       -l "\$r=2,l=16\$ \$r=3,l=86\$ \$r=4,l=432\$ \$r=5,l=2165\$ \$r=6,l=10830\$" \
       -p figs/reuters_r_l_s0.2.pdf\
       $1/exp1/topics/reuters_3_r_2_l_16.topics\
       $1/exp1/topics/reuters_3_r_3_l_86.topics\
       $1/exp1/topics/reuters_3_r_4_l_432.topics\
       $1/exp1/topics/reuters_3_r_5_l_2165.topics\
       $1/exp1/topics/reuters_3_r_6_l_10830.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng_r3_l.pdf\
       $1/exp2/topics/20ng_r_3_l_86.topics\
       $1/exp2/topics/20ng_r_3_l_118.topics\
       $1/exp2/topics/20ng_r_3_l_205.topics\
       $1/exp2/topics/20ng_r_3_l_315.topics\
       $1/exp2/topics/20ng_r_3_l_692.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692]) with vocabulary of 10k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng10k_r3_l.pdf\
       $1/exp2/topics/20ng10k_r_3_l_86.topics\
       $1/exp2/topics/20ng10k_r_3_l_118.topics\
       $1/exp2/topics/20ng10k_r_3_l_205.topics\
       $1/exp2/topics/20ng10k_r_3_l_315.topics\
       $1/exp2/topics/20ng10k_r_3_l_692.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692]) with vocabulary of 5k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng5k_r3_l.pdf\
       $1/exp2/topics/20ng5k_r_3_l_86.topics\
       $1/exp2/topics/20ng5k_r_3_l_118.topics\
       $1/exp2/topics/20ng5k_r_3_l_205.topics\
       $1/exp2/topics/20ng5k_r_3_l_315.topics\
       $1/exp2/topics/20ng5k_r_3_l_692.topics


# plot for NIPS (r = 3 and l = [86 118 205 315 692]) with vocabulary of 1k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692 2020 5544" \
       -p figs/nips1k_r3_l.pdf\
       $1/exp2/topics/nips1k_r_3_l_86.topics\
       $1/exp2/topics/nips1k_r_3_l_118.topics\
       $1/exp2/topics/nips1k_r_3_l_205.topics\
       $1/exp2/topics/nips1k_r_3_l_315.topics\
       $1/exp2/topics/nips1k_r_3_l_692.topics\
       $1/exp2/topics/nips1k_r_3_l_2020.topics\
       $1/exp2/topics/nips1k_r_3_l_5544.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng_exp3_r3_l.pdf\
       $1/exp3/topics/20ng_r_3_l_86.topics\
       $1/exp3/topics/20ng_r_3_l_118.topics\
       $1/exp3/topics/20ng_r_3_l_205.topics\
       $1/exp3/topics/20ng_r_3_l_315.topics\
       $1/exp3/topics/20ng_r_3_l_692.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692]) with vocabulary of 10k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng10k_exp3_r3_l.pdf\
       $1/exp3/topics/20ng10k_r_3_l_86.topics\
       $1/exp3/topics/20ng10k_r_3_l_118.topics\
       $1/exp3/topics/20ng10k_r_3_l_205.topics\
       $1/exp3/topics/20ng10k_r_3_l_315.topics\
       $1/exp3/topics/20ng10k_r_3_l_692.topics

# plot for 20 Newsgroups (r = 3 and l = [86 118 205 315 692]) with vocabulary of 5k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/20ng5k_exp3_r3_l.pdf\
       $1/exp3/topics/20ng5k_r_3_l_86.topics\
       $1/exp3/topics/20ng5k_r_3_l_118.topics\
       $1/exp3/topics/20ng5k_r_3_l_205.topics\
       $1/exp3/topics/20ng5k_r_3_l_315.topics\
       $1/exp3/topics/20ng5k_r_3_l_692.topics


# plot for NIPS (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/nips_exp3_r3_l.pdf\
       $1/exp3/topics/nips_r_3_l_86.topics\
       $1/exp3/topics/nips_r_3_l_118.topics\
       $1/exp3/topics/nips_r_3_l_205.topics\
       $1/exp3/topics/nips_r_3_l_315.topics\
       $1/exp3/topics/nips_r_3_l_692.topics

# plot for NIPS (r = 3 and l = [86 118 205 315 692]) with vocabulary of 1k
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/nips1k_exp3_r3_l.pdf\
       $1/exp3/topics/nips1k_r_3_l_86.topics\
       $1/exp3/topics/nips1k_r_3_l_118.topics\
       $1/exp3/topics/nips1k_r_3_l_205.topics\
       $1/exp3/topics/nips1k_r_3_l_315.topics\
       $1/exp3/topics/nips1k_r_3_l_692.topics

# plot for Reuters (r = 3 and l = [86 118 205 315 692])
python python/utils/plot_coherences.py \
       -x "Different values of the parameter \$l\$ (for \$r = 3\$)" \
       -l "86 118 205 315 692" \
       -p figs/reuters_exp3_r3_l.pdf\
       $1/exp3/topics/reuters_r_3_l_86.topics\
       $1/exp3/topics/reuters_r_3_l_118.topics\
       $1/exp3/topics/reuters_r_3_l_205.topics\
       $1/exp3/topics/reuters_r_3_l_315.topics\
       $1/exp3/topics/reuters_r_3_l_692.topics
