import stwfsapy.thesaurus as t


def test_label_unwrap(tuples):
    unwrapped = list(t._unwrap_labels(tuples))
    assert len(tuples) == len(unwrapped)
    for original, transformed in zip(tuples, unwrapped):
        assert isinstance(transformed[1], str)
        assert original[1].toPython() == transformed[1]
        assert original[0] == transformed[0]
