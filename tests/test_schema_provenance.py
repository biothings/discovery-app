"""
Test capture of schema change notes (dct:provenance) on classes, issue #209
"""

from discovery.utils.adapters import SchemaAdapter


def _schema(class_extra=None, context_extra=None):
    context = {
        "schema": "http://schema.org/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "provtest": "http://example.org/provtest/",
    }
    context.update(context_extra or {})
    cls = {
        "@id": "provtest:ProvTestClass",
        "@type": "rdfs:Class",
        "rdfs:comment": "A class used to test dct:provenance capture.",
        "rdfs:label": "ProvTestClass",
        "rdfs:subClassOf": {"@id": "schema:Thing"},
    }
    cls.update(class_extra or {})
    return {"@context": context, "@graph": [cls]}


def _get_class(doc):
    classes = SchemaAdapter(doc).get_class_defs()
    return next(c for c in classes if c["name"] == "provtest:ProvTestClass")


def test_provenance_with_dct_in_context():
    doc = _schema(
        {"dct:provenance": "Added property foo"},
        {"dct": "http://purl.org/dc/terms/"},
    )
    assert _get_class(doc)["provenance"] == "Added property foo"


def test_provenance_without_dct_in_context():
    doc = _schema({"dct:provenance": "Added property foo"})
    assert _get_class(doc)["provenance"] == "Added property foo"


def test_provenance_value_object():
    doc = _schema(
        {"dcterms:provenance": {"@value": "Made bar required", "@language": "en"}},
        {"dcterms": "http://purl.org/dc/terms/"},
    )
    assert _get_class(doc)["provenance"] == "Made bar required"


def test_no_provenance():
    assert "provenance" not in _get_class(_schema())
