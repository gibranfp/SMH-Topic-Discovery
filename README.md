# Topic discovery with Sampled Min-Hashing

## Requirements
* Python 2.7
* scikit-learn
* NumPy
* NLTK (with `punkt`, `averaged_perceptron_tagger` and `wordnet`)
* [Sampled-MinHashing](https://github.com/gibranfp/Sampled-MinHashing)

## Installation

Install dependencies (use `sudo` for system-wide installation):

~~~~	
pip install sklearn nltk
~~~~

Download NLTK's required resources by doing:

~~~~
python -m nltk.downloader punkt averaged_perceptron_tagger wordnet
~~~~

Install Sampled-MinHashing (see README at https://github.com/gibranfp/Sampled-MinHashing).

## Corpora
It will download the followind resources/corpora using 'scripts/prepare\_db.sh':

* 20 Newsgroups 
* English Wikipedia
* Spanish Wikipedia
* If you have access to a copy of the Reuters corpus, the script will prompt you to add the path to it.

## Running experiments

To run the experiments, from the main directory:
~~~~
bash scripts/prepare_db.sh -a
bash scripts/run_all.sh
~~~~

## Sample Topics
These are some sample topics discovered from20 Newsgroups, Reuters, and English and Spanish Wikipedia (see [](example_topics) directory for complete lists of topics).  Note that in the 20 Newsgroups corpus topics that loosely correspond to the main thematic of the different newsgroups from where the documents were collected, for example topics related to religion, computers, sports, cryptography, politics, space and medicine. 
On the other hand, most topics from the Reuters corpus are related to major world events, important world news, economy, finance, popular sports and technology. Finally, a wide variety of topics were discovered from both Spanish and English editions of Wikipedia, including demography, history, sports, series, and music.

| 20 Newsgroups (Top 10 words) |
|:--------------------:|
|religion, atheist, religious, atheism, belief, christian, faith, argument, bear, catholic|
|os, cpu, pc, memory, windows, microsoft, price, fast, late, manager|
|game, season, team, play, score, minnesota, win, move, league, playoff|
|rfc, crypt, cryptography, hash, snefru, verification, communication, privacy, answers, signature|
|decision, president, department, justice, attorney, question, official, responsibility, yesterday, conversation|

| Reuters (Top 10 words) |
|:--------------------:|
|point, index, market, high, stock, close, end, share, trade, rise|
|voter, election, poll, party, opinion, prime, seat, candidate, presidential, hold|
|play, team, match, game, win, season, cup, couch, final, champion|
|wrongful, fujisaki, nicole, acquit, ronald, jury, juror, hiroshi, murder, petrocelli|
|spongiform, encephalopathy, bovine, jakob, creutzfeldt, mad, cow, wasting, cjd, bse|

|Spanish Wikipedia (Top 10 words) |
|:--------------------:|
|religion, atheist, religious, atheism, belief, christian, faith, argument, bear, catholic|
|os, cpu, pc, memory, windows, microsoft, price, fast, late, manager|
|game, season, team, play, score, minnesota, win, move, league, playoff|
|rfc, crypt, cryptography, hash, snefru, verification, communication, privacy, answers, signature|
|decision, president, department, justice, attorney, question, official, responsibility, yesterday, conversation|

| English Wikipedia (Top 10 words) |
|:--------------------:|
|religion, atheist, religious, atheism, belief, christian, faith, argument, bear, catholic|
|os, cpu, pc, memory, windows, microsoft, price, fast, late, manager|
|game, season, team, play, score, minnesota, win, move, league, playoff|
|rfc, crypt, cryptography, hash, snefru, verification, communication, privacy, answers, signature|
|decision, president, department, justice, attorney, question, official, responsibility, yesterday, conversation|

## References

```
@Article{smh_topics2019,
  author = {Gibran Fuentes-Pineda and Ivan Vladimir Meza-Ruiz},
  title = {Topic discovery in massive text corpora based on Min-Hashing},
  journal = {Expert Systems with Applications},
  volume = {136},
  pages = {62--72},
  year = {2019},
}
```
