from discovery.model.dataset import Dataset
import json


def backup():
    with open('./backup.json', 'w',  encoding='utf-8') as file:
        json.dump(list(hit.to_dict() for hit in Dataset.search().scan()), file, indent=2, default=str)


if __name__ == "__main__":
    backup()
