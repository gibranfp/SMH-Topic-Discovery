mkdir -p data/reuters
for SIZE in {10000..100000..10000}
do
    python python/corpus/ref2corpus.py \
           experiments/ref_corpus/reuters/reuters.ref.txt \
           data/stopwords_english.txt \
           data/reuters \
           --cutoff $SIZE &
done
wait

mkdir -p data/reuters/valid_strictest
for SIZE in {10000..100000..10000}
do
    python python/corpus/ref2corpus_valid_strictest.py \
           experiments/ref_corpus/reuters/reuters.ref.txt \
           data/stopwords_english.txt \
           data/reuters/valid_strictest \
           --cutoff $SIZE &
done
wait

mkdir -p data/reuters/valid_stricter
for SIZE in {10000..100000..10000}
do
    python python/corpus/ref2corpus_valid_stricter.py \
           experiments/ref_corpus/reuters/reuters.ref.txt \
           data/stopwords_english.txt \
           data/reuters/valid_stricter \
           --cutoff $SIZE &
done
wait

mkdir -p data/reuters/valid_strict
for SIZE in {10000..100000..10000}
do
    python python/corpus/ref2corpus_valid_strict.py \
           experiments/ref_corpus/reuters/reuters.ref.txt \
           data/stopwords_english.txt \
           data/reuters/valid_strict \
           --cutoff $SIZE
done
wait

mkdir -p data/reuters/valid_mild
for SIZE in {10000..100000..10000}
do
    python python/corpus/ref2corpus_valid_mild.py \
           experiments/ref_corpus/reuters/reuters.ref.txt \
           data/stopwords_english.txt \
           data/reuters/valid_mild \
           --cutoff $SIZE
done
wait
