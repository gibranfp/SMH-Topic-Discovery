######## Plots in the paper

# #### Coherence boxplots
python python/plotting/plot_coherences.py -x "JCC Threshold ($\eta$)" -c plots/coherence/config/coocurrence_threshold.config -p plots/coherence/pdf/coocurrence_threshold.pdf
python python/plotting/plot_coherences.py -x "JCC Threshold ($\eta$)" -c plots/coherence/config/topK/coocurrence_threshold.config -p plots/coherence/pdf/topK/coocurrence_threshold.k400.pdf

python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/coherence/config/overlap.config -p plots/coherence/pdf/overlap.pdf
python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/coherence/config/topK/overlap.config -p plots/coherence/pdf/topK/overlap.k400.pdf

python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/tuple_size.config -p plots/coherence/pdf/tuple_size.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/coherence/config/topK/tuple_size.config -p plots/coherence/pdf/topK/tuple_size.k400.pdf

python python/plotting/plot_coherences.py -x "Scheme" -c plots/coherence/config/expanded_binary.config -p plots/coherence/pdf/expanded_binary.pdf
python python/plotting/plot_coherences.py -x "Scheme" -c plots/coherence/config/topK/expanded_binary.config -p plots/coherence/pdf/topK/expanded_binary.k400.pdf

python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/coherence/config/vocabulary_size.config -p plots/coherence/pdf/vocabulary_size.pdf
python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/coherence/config/topK/vocabulary_size.config -p plots/coherence/pdf/topK/vocabulary_size.k400.pdf

python python/plotting/plot_coherences.py -t -r 60.0 -x "Method" -c plots/coherence/config/comparison_smh_lda.config -p plots/coherence/pdf/comparison_smh_lda.pdf
