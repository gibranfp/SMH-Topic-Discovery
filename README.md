B1;4205;0c# Topic discovery with Sampled Min-Hashing

## Installation

Install dependencies (use ~sudo~ for system-wide installation):

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
* 20NewsGruop
* Wikipedia

If you have access to a copy of Reuters copora it will prompt you with this option, otherwise ignore it.
