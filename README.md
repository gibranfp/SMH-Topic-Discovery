# Topic discovery with Sampled Min-Hashing

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

* NIPS
* 20 Newsgroups
* English Wikipedia
* Spanish Wikipedia
* If you have access to a copy of the Reuters corpus, the script will prompt you to add the path to it.

## Running experiments

To run the experiments, from the main directory:
~~~~
bash scripts/prepare_db.sh -a

~~~~
