from discovery.model.dataset import Dataset

niaidContext = {
"schema": "http://schema.org/",
"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
"rdfs": "http://www.w3.org/2000/01/rdf-schema#",
"bioschemas": "https://discovery.biothings.io/ns/bioschemas/",
"niaid": "https://discovery.biothings.io/ns/niaid/",
}

def updateContext():
    """
    Update datasets missing @context and update @types with outdated names
    """
    # ids = []
    # needs_renaming =[]
    docs = Dataset.search()
    for doc in docs.scan():
        context = getattr(doc, '@context', None)
        # dataset_id = getattr(getattr(doc, 'meta', None), 'id', None)
        clss_type = getattr(doc, "@type", None)
        if not context:
            if ":" not in clss_type:
                # add context and fix class name
                added_prefix = "niaid:" + clss_type
                # ids.append(added_prefix)
                doc.update(**{"@context": niaidContext, "@type": added_prefix})
            else:
                # add context
                # ids.append('JUST CONTEXT')
                doc.update(**{"@context": niaidContext})
        if 'niaid:Niaid' in clss_type:
            updated_name = clss_type.replace("niaid:Niaid", "niaid:")
            # needs_renaming.append(clss_type + " >>> " + updated_name)
            doc.update(**{"@type": updated_name})

    # print(len(ids))
    # print(ids)
    # print("++++++++++++++++++")
    # print(len(needs_renaming))
    # print(needs_renaming)



if __name__ == "__main__":
    updateContext()
