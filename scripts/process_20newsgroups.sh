mkdir -p data/20newsgroups
for SIZE in {1000..10000..1000}
do
    python python/corpus/ref2corpus.py \
           experiments/ref_corpus/20newsgroups/20newsgroups.ref.txt \
           data/stopwords_english.txt \
           data/20newsgroups \
           --cutoff $SIZE &
done
wait

mkdir -p data/20newsgroups/valid_strictest
for SIZE in {1000..10000..1000}
do
    python python/corpus/ref2corpus_valid_strictest.py \
           experiments/ref_corpus/20newsgroups/20newsgroups.ref.txt \
           data/stopwords_english.txt \
           data/20newsgroups/valid_strictest \
           --cutoff $SIZE &
done
wait

mkdir -p data/20newsgroups/valid_stricter
for SIZE in {1000..10000..1000}
do
    python python/corpus/ref2corpus_valid_stricter.py \
           experiments/ref_corpus/20newsgroups/20newsgroups.ref.txt \
           data/stopwords_english.txt \
           data/20newsgroups/valid_stricter \
           --cutoff $SIZE &
done
wait

mkdir -p data/20newsgroups/valid_strict
for SIZE in {1000..10000..1000}
do
    python python/corpus/ref2corpus_valid_strict.py \
           experiments/ref_corpus/20newsgroups/20newsgroups.ref.txt \
           data/stopwords_english.txt \
           data/20newsgroups/valid_strict \
           --cutoff $SIZE
done
wait

mkdir -p data/20newsgroups/valid_mild
for SIZE in {1000..10000..1000}
do
    python python/corpus/ref2corpus_valid_mild.py \
           experiments/ref_corpus/20newsgroups/20newsgroups.ref.txt \
           data/stopwords_english.txt \
           data/20newsgroups/valid_mild \
           --cutoff $SIZE
done
wait
