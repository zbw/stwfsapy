# Copyright 2020 Leibniz Information Centre for Economics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Set, Iterable, Tuple, DefaultDict
import rdflib
from scipy.sparse import csr_matrix, vstack
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError
from stwfsapy import thesaurus as t
from stwfsapy.util.set_closure import set_closure
from collections import defaultdict


class ThesaurusFeatureTransformation(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            graph: rdflib.Graph,
            concepts: Set[rdflib.term.URIRef],
            thesauri: Set[rdflib.term.URIRef],
            thesaurus_relation: rdflib.term.URIRef,
            inverse_relation: bool = False
            ):
        self.graph = graph
        self.concepts = concepts
        self.thesauri = thesauri
        self.mapping_ = None
        self.thesaurus_relation = thesaurus_relation
        self.inverse_relation = inverse_relation

    def fit(self, X=None, y=None, **kwargs):
        """Creates the mapping from concepts
        to the thesauri that are broader than the concept."""
        broaders = list(t.extract_relation_by_uri(
            self.graph,
            self.thesaurus_relation,
            self.inverse_relation))
        concept_po = _collect_po_from_tuples(
            t.filter_subject_tuples_from_set(broaders, self.concepts))
        thesauri_po = _collect_po_from_tuples(
            t.filter_subject_tuples_from_set(broaders, self.thesauri),
            self.thesauri)
        for thesaurus in self.thesauri:
            thesauri_po[thesaurus].add(thesaurus)
        thesauri_closure = set_closure(thesauri_po)
        thesaurus_indices = dict(zip(
            thesauri_closure,
            range(len(thesauri_closure))))
        concept_thesauri_mapping = {
            concept: set.union(
                *(
                    thesauri_closure.get(broader, set())
                    for broader
                    in broaders
                ))
            for concept, broaders in concept_po.items()
        }
        self.feature_dim_ = len(thesaurus_indices)
        self.mapping_ = {
            str(concept): csr_matrix(
                (
                    [1 for _ in thesaurii],
                    (
                        [0 for _ in thesaurii],
                        [
                            thesaurus_indices[thesaurus]
                            for thesaurus
                            in thesaurii]
                    )
                ),
                shape=(1, len(thesaurus_indices))
            )
            for concept, thesaurii
            in concept_thesauri_mapping.items()
        }
        return self

    def _transform_single(self, x):
        # No default dict, so the transform can be pickled
        try:
            res = self.mapping_[x]
        except KeyError:
            res = csr_matrix(
                ([], ([], [])),
                shape=(1, self.feature_dim_)
            )
        return res

    def transform(self, X) -> csr_matrix:
        if not self.mapping_:
            raise NotFittedError
        return vstack([self._transform_single(x) for x in X])


def _collect_po_from_tuples(
        tuples: Iterable[Tuple[rdflib.term.URIRef, rdflib.term.URIRef]],
        base_elements: Set[rdflib.term.URIRef] = set()
        ) -> DefaultDict[rdflib.term.URIRef, Set[rdflib.term.URIRef]]:
    ret = defaultdict(set)
    for e in base_elements:
        ret[e].add(e)
    for narrower, broader in tuples:
        ret[narrower].add(broader)
    return ret
