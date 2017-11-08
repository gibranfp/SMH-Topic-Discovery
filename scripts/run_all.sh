#!/bin/bash
#
# Script to discover topics with SMH and LDA.
#
bash scripts/evaluate_smh_cooccurrence_threshold.sh experiments/topic_discovery/smh
bash scripts/evaluate_smh_tuple_size.sh experiments/topic_discovery/smh
bash scripts/evaluate_smh_vocabulary_size.sh experiments/topic_discovery/smh
bash scripts/evaluate_smh_overlap.sh experiments/topic_discovery/smh
bash scripts/run_smh_topK.sh experiments/topic_discovery/smh
bash scripts/run_lda.sh experiments/topic_discovery/lda
