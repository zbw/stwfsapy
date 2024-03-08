# stwfsapy
[![CI](https://github.com/zbw/stwfsapy/actions/workflows/ci.yml/badge.svg)](https://github.com/zbw/stwfsapy/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/zbw/stwfsapy/branch/master/graph/badge.svg)](https://codecov.io/gh/zbw/stwfsapy)
## About
This library provides the functionality to find SKOS thesaurus concepts in a text.
It is a reimplementation in Python of [stwfsa](https://github.com/zbw/stwfsa) combined with the concept scoring from [1].
A deterministic finite automaton is constructed from the labels of the thesaurus concepts to perform the matching.
In addition, a classifier is trained to score the matched concept occurrences.

## Data Requirements
The construction of the automaton requires a SKOS thesaurus represented as a `rdflib` `Graph`.
Concepts should be related to labels by `skos:prefLabel`, `skos:altLabel`, `zbwext:altLabelNarrower`, `zbwext:altLabelRelated` or `skos:hiddenLabel`.
Concepts have to be identifiable by `rdf:type`.
The training of the predictor requires annotated text.
Each training sample should be annotated with one or more concepts from the thesaurus.

## Installation 

### Requirements

Python ``>= 3.9`` is required.

### With pip
stwfsapy is available on [PyPI](pypi.org) . You can install stwfsapy using pip:

``pip install stwfsapy``

This will install a python package called `stwfsapy`.

Note that it is generally recommended to use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to avoid 
 conflicting behaviour with the system package manager.

### From source
You also have the option to checkout the repository and install the packages from source. You need
[poetry](https://python-poetry.org) to perform the task:

```shell
# call inside the project directory
poetry install --without ci 
```

## Usage
### Create predictor
First load your thesaurus.
```python
from rdflib import Graph

g = Graph()
g.parse('/path/to/your/thesaurus')
```
First, define the type URI for descriptors.
If your thesaurus is structured into sub-thesauri by providing categories for the concepts of the thesaurus using,
e.g., `skos:Collection`, you can optionally specify the type of these categories via a URI.
In this case you should also specify the relation that relates concepts to categories.
Furthermore you can indicate whether this relation is a specialisation relation (as opposed to a generalisation relation, which is the default).
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
The next step assumes you have loaded your texts into a list `X` and your labels into a list of lists `y`,
such that for all indices `0 <= i < len(X)`. The list at `y[i]` contains the URIs to the correct concepts for `X[i]`.
The concepts should be given by their URI.
Then you can train the classifier:
```python
p.fit(X, y)
```
Afterwards you can get the predicted concepts and scores:
```python
p.suggest_proba(['one input text', 'A completely different input text.'])
```
Alternatively you can get a sparse matrix of scores by calling
```python
p.predict_proba(['one input text', 'Another input text.'])
```
The indices of the concepts are stored in `p.concept_map_`.

### Options
All options for the predictor are documented at https://stwfsapy.readthedocs.io/ .

### Save Model
A trained predictor `p` can be stored by calling `p.store('/path/to/storage/location')`.
Afterwards it can be loaded as follows:
```python
from stwfsapy.predictor import StwfsapyPredictor

StwfsapyPredictor.load('/path/to/storage/location')
``` 

## Contribute

Contributions via pull requests are welcome. Please create an issue beforehand
to explain and discuss the reasons for the respective contribution.

## References
[1] [Toepfer, Martin, and Christin Seifert. "Fusion architectures for automatic subject indexing under concept drift" International Journal on Digital Libraries (IJDL), 2018.](https://ris.utwente.nl/ws/portalfiles/portal/248044709/Toepfer2018fusion.pdf)

## Context information
This code was created as part of the subject indexing automation effort at [ZBW – Leibniz Information Centre for Economics](https://www.zbw.eu/en/). See [our homepage](https://www.zbw.eu/en/about-us/knowledge-organisation/automation-of-subject-indexing-using-methods-from-artificial-intelligence) for more information, publications, and contact details.
