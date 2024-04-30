import logging

from discovery.model.dataset import Dataset

niaidContext = {
"schema": "http://schema.org/",
"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
"bioschemas": "https://discovery.biothings.io/view/bioschemas/",
"niaid": "https://discovery.biothings.io/view/niaid/",
"nde": "https://discovery.biothings.io/view/nde/"
}

def updateContext():
    """
    Update datasets missing @context and update @types with outdated names
    """
    ids = []
    needs_renaming =[]
    docs = Dataset.search()
    for doc in docs.scan():
        d = doc.to_dict()
        context = d.get("@context")
        datasetID = getattr(getattr(doc, 'meta', None), 'id', None)
        typ = getattr(doc, "@type", None)
        if not context:
            ids.append(datasetID)
            # doc.update(**{"@context": niaidContext})
        if 'niaid:Niaid' in typ:
            needs_renaming.append(typ)
            # doc.update(**{"@type": "niaid:Dataset"})

    print(len(ids))
    print(ids)
    print("++++++++++++++++++")
    print(len(needs_renaming))
    print(needs_renaming)



if __name__ == "__main__":
    updateContext()
