FILES=`find $1 -name "*_top10.topics"`

# echo "Concatenating all top 10 topics in $1"/
cat $FILES > $1/all_top10_topics.txt

# echo "Computing word occurrence..."
python ../topic_interpretability/ComputeWordCount.py $1/all_top10_topics.topics data/ref > $1/all_top10_topics_wordcounts.txt

for F in $FILES
do
    filepath="${F%.*}"
    filename=$(basename $F)
    filename="${filename%.*}"
    dirpath=$(dirname $F)
    echo "Computing the observed coherence for $F ..."
    python ../topic_interpretability/ComputeObservedCoherence.py $F npmi experiments/topic_discovery/smh/all_top10_topics_wordcounts.txt > $dirpath/$filename.coh
done
