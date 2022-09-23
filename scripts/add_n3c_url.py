import logging

import requests

import config
from discovery.model import Dataset

logging.basicConfig(level="DEBUG")


def get_titles():

    response = requests.post(
        "https://n3c-help.atlassian.net/rest/api/3/search",
        auth=(config.N3C_AUTH_USER, config.N3C_AUTH_PASSWORD),
        json={
            "jql": 'project = "10016"',
            "fields": ["description"],
            "maxResults": 20,  # we know there are only 19 records
            "startAt": 0,
        },
    ).json()
    for issue in response["issues"]:
        try:
            title = issue["fields"]["description"]["content"][3]["content"][0]["content"][0][
                "content"
            ][1]["text"]
        except (KeyError, IndexError):
            pass
        else:
            yield (title, issue["self"])


def update_url():
    for title, url in get_titles():
        print(title)
        print(url)
        search = Dataset.search()
        search = search.query("match", name=title)
        for dataset in search:
            # since we did a match query on a text field
            if dataset.name == title:
                print(dataset.meta.id)
                _dataset = Dataset.get(dataset.meta.id)
                _dataset["_n3c"] = {"url": url}
                _dataset.save()
        print()


if __name__ == "__main__":
    update_url()
