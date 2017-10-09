######## Plots in the paper

# #### Coherence boxplots
python python/plotting/plot_coherences.py -x "Cooccurrence Coefficient Threshold ($\eta$)" -c plots/coherence/config/coocurrence_threshold.config -p plots/coherence/pdf/coocurrence_threshold.pdf
python python/plotting/plot_coherences.py -x "Cooccurrence Coefficient Threshold ($\eta$)" -c plots/coherence/config/topK/coocurrence_threshold.config -p plots/coherence/pdf/topK/coocurrence_threshold.k400.pdf

python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/coherence/config/overlap_w0.02.config -p plots/coherence/pdf/overlap_w0.02.pdf
python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/coherence/config/topK/overlap_w0.02.config -p plots/coherence/pdf/topK/overlap_w0.02.k400.pdf

python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/tuple_size.config -p plots/coherence/pdf/tuple_size.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size.config -p plots/coherence/pdf/topK/tuple_size.k400.pdf

python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/tuple_size_wcc0.12.config -p plots/coherence/pdf/tuple_size_wcc0.12.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size_wcc0.12.config -p plots/coherence/pdf/topK/tuple_size_wcc0.12.k400.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size_wcc0.12.k300.config -p plots/coherence/pdf/topK/tuple_size_wcc0.12.k300.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size_wcc0.12.k200.config -p plots/coherence/pdf/topK/tuple_size_wcc0.12.k200.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size_wcc0.12.k100.config -p plots/coherence/pdf/topK/tuple_size_wcc0.12.k100.pdf

python python/plotting/plot_coherences.py -x "Weighting Scheme" -c plots/coherence/config/weighted_expanded_binary_w0.02.config -p plots/coherence/pdf/weighted_expanded_binary_w0.02.pdf
python python/plotting/plot_coherences.py -x "Weighting Scheme" -c plots/coherence/config/topK/weighted_expanded_binary_w0.02.config -p plots/coherence/pdf/topK/weighted_expanded_binary_w0.02.k400.pdf

python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/coherence/config/vocabulary_size_w0.02.config -p plots/coherence/pdf/vocabulary_size_w0.02.pdf
python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/coherence/config/topK/vocabulary_size_w0.02.config -p plots/coherence/pdf/topK/vocabulary_size_w0.02.k400.pdf

python python/plotting/plot_coherences.py -x "Model" -c plots/coherence/config/comparison_smh_lda.config -p plots/coherence/pdf/comparison_smh_lda.pdf


#### Topic size boxplots
python python/plotting/plot_topic_sizes.py -x "Cooccurrence Coefficient Threshold ($\eta$)" -c plots/topic_size/config/coocurrence_threshold.config -p plots/topic_size/pdf/coocurrence_threshold.pdf

python python/plotting/plot_topic_sizes.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/topic_size/config/overlap_w0.02.config -p plots/topic_size/pdf/overlap_w0.02.pdf


python python/plotting/plot_topic_sizes.py -x "Tuple Size" -c plots/topic_size/config/tuple_size.config -p plots/topic_size/pdf/tuple_size.pdf
python python/plotting/plot_topic_sizes.py -x "Tuple Size" -c plots/topic_size/config/tuple_size_wcc0.12.config -p plots/topic_size/pdf/tuple_size_wcc0.12.pdf

python python/plotting/plot_topic_sizes.py -x "Weighting Scheme" -c plots/topic_size/config/weighted_expanded_binary_w0.02.config -p plots/topic_size/pdf/weighted_expanded_binary_w0.02.pdf
python python/plotting/plot_topic_sizes.py -x "Weighting Scheme" -c plots/topic_size/config/weighted_expanded_binary_w0.02_w0.04.config -p plots/topic_size/pdf/weighted_expanded_binary_w0.02_w0.04.pdf

python python/plotting/plot_topic_sizes.py -x "Vocabulary Size" -c plots/topic_size/config/vocabulary_size_w0.02.config -p plots/topic_size/pdf/vocabulary_size_w0.02.pdf
