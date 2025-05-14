"""
Update outdated context with /view instead of new /ns namespaces
"""
import logging
from discovery.model.schema import Schema
from discovery.model import Dataset

# context example:

# @context: {
#     "schema": "http://schema.org/",
#     "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
#     "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
#     "bioschemas": "https://discovery.biothings.io/ns/bioschemas/",
#     "niaid": "https://discovery.biothings.io/view/niaid/",
#     "nde": "https://discovery.biothings.io/view/nde/"
# }


def updateDocs(type=None):
    '''
    Update documents to replace "/view/" with "/ns/" in specific values of @context.
    Only modify necessary values, preserving the rest of the context as-is.
    '''
    if type == "dataset":
        docs = Dataset.search()
    else:
        docs = Schema.search()
    updated_count = 0
    scanned_count = 0

    for doc in docs.scan():
        scanned_count += 1

        context = doc.to_dict().get("@context", None)

        if context and isinstance(context, dict):
            updated = False

            for key, value in context.items():
                if isinstance(value, str) and "discovery.biothings.io/view/" in value:
                    context[key] = value.replace("/view/", "/ns/")
                    updated = True
                    logging.info(f'Will update @context[{key}] for document {doc.meta.id}')
                    print(f'Will update @context[{key}] for document {doc.meta.id}')

            if updated:
                # Uncomment when ready to update
                doc.update(**{"@context": context})
                updated_count += 1
            else:
                logging.info(f'No changes needed for document {doc.meta.id}')
                print(f'No changes needed for document {doc.meta.id}')
        else:
            logging.warning(f'Document {doc.meta.id} has no valid @context')

    print(f"Total documents scanned: {scanned_count}")
    print(f"Total documents updated: {updated_count}")
    logging.info(f"Total documents scanned: {scanned_count}")
    logging.info(f"Total documents updated: {updated_count}")


if __name__ == "__main__":
    updateDocs()