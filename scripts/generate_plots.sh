######## Plots in the paper

# #### Coherence boxplots
python python/plotting/plot_coherences.py -x "JCC Threshold ($\eta$)" -c plots/config/coocurrence_threshold.config -p plots/pdf/coocurrence_threshold.pdf
python python/plotting/plot_coherences.py -x "JCC Threshold ($\eta$)" -c plots/config/topK/coocurrence_threshold.config -p plots/pdf/topK/coocurrence_threshold.k400.pdf

python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/config/overlap.config -p plots/pdf/overlap.pdf
python python/plotting/plot_coherences.py -x "Overlap Coefficient Threshold ($\epsilon$)" -c plots/config/topK/overlap.config -p plots/pdf/topK/overlap.k400.pdf

python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/config/tuple_size.config -p plots/pdf/tuple_size.pdf
python python/plotting/plot_coherences.py -x "Tuple Size" -c plots/config/topK/tuple_size.config -p plots/pdf/topK/tuple_size.k400.pdf

python python/plotting/plot_coherences.py -x "Scheme" -c plots/config/expanded_binary.config -p plots/pdf/expanded_binary.pdf
python python/plotting/plot_coherences.py -x "Scheme" -c plots/config/topK/expanded_binary.config -p plots/pdf/topK/expanded_binary.k400.pdf

python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/config/vocabulary_size.config -p plots/pdf/vocabulary_size.pdf
python python/plotting/plot_coherences.py -x "Vocabulary Size" -c plots/config/topK/vocabulary_size.config -p plots/pdf/topK/vocabulary_size.k400.pdf

python python/plotting/plot_coherences.py -t -r 60.0 -x "Method" -c plots/config/comparison_smh_lda.config -p plots/pdf/comparison_smh_lda.pdf
