# stwfsapy
[![Build Status](https://travis-ci.org/zbw/stwfsapy.svg?branch=master)](https://travis-ci.org/zbw/stwfsapy)
[![codecov](https://codecov.io/gh/zbw/stwfsapy/branch/master/graph/badge.svg)](https://codecov.io/gh/zbw/stwfsapy)
## About
This library provides functionality to find the labels of SKOS thesaurus concepts in (short) text.
It is a reimplementation in Python of [stwfsa](https://github.com/zbw/stwfsa) combined with the concept scoring from [1].
A deterministic finite automaton is constructed from the labels of the thesaurus concepts to perform the matching.
In addition, a classifier is trained to score the matched occurrences of the concepts.

## Data Requirements
The construction for the automaton requires a SKOS thesaurus represented as a `rdflib` `Graph`.
Concepts should be related to labels by `skos:prefLabel` or `skos:altLabel`.
In addition it is assumed that concepts are organized in a hierarchy that includes sub-thesauri.
Concepts and sub-thesauri have to be distinguishable by `rdf:type`.
The training of the predictor requires labeled text.
Each training sample should be annotated with one or more concepts from the thesaurus.

## Usage
### Create predictor
First load your thesaurus.
```python
from rdflib import Graph

g = Graph()
g.load('/path/to/your/thesaurus')
```
Define the type URIs for descriptors and sub-thesauri.
You also need to define the relationship that relates sub-thesauri to concepts.
It is beneficial if this relation structures the sub-thesauri.
Furthermore you can indicate whether the thesaurus relation is a specialisation.
For the [STW](https://http://zbw.eu/stw/) this would be
```python
descriptor_type_uri = 'http://zbw.eu/namespaces/zbw-extensions/Descriptor'
thsys_type_uri = 'http://zbw.eu/namespaces/zbw-extensions/Thsys'
thesaurus_relation_type_uri = 'http://www.w3.org/2004/02/skos/core#broader'
is_specialisation = False
```

Create the predictor
```python
from stwfsapy.predictor import StwfsapyPredictor
p = StwfsapyPredictor(
    g,
    descriptor_type_uri,
    thsys_type_uri,
    thesaurus_relation_type_uri,
    is_specialisation,
    langs={'en'},
    simple_english_plural_rules=True)
```
The next step assumes you have loaded your texts into a list `X` and your labels in a list of lists `y`,
such that for all indices `0 <= i < len(X)`. The list at `y[i]` contains the URIs to the correct concepts for `X[i]`.
The concepts should be given by their URI.
Then you can train the classifier:
```python
p.fit(X, y)
```
Afterwards you can get the predicted concepts and scores:
```python
p.suggest_proba(['one input text', 'A completely different input text.']
```
Alternatively you can get a sparse matrix of scores by calling
```python
p.predict_proba(['one input text', 'Another input text.']
```
The indices of the concepts are stored in `p.concept_map_`.

## Save Model
A trained predictor `p` can be stored by calling `p.store('/path/to/storage/location')`.
Afterwards it can be loaded as follows:
```python
from stwfsapy.predictor import StwfsapyPredictor

StwfsapyPredictor.load('/path/to/storage/location')
``` 

## References
[1] [Toepfer, Martin, and Christin Seifert. "Content-based quality estimation for automatic subject indexing of short texts under precision and recall constraints." International Conference on Theory and Practice of Digital Libraries. Springer, Cham, 2018.](https://arxiv.org/abs/1806.02743)
