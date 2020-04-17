"""
Try:
python scripts/add_dataset.py "<URL>" "<email>" 0

Test Data:
Git https://github.com/data2health/schemas/blob/master/Dataset/examples/wellderly/wellderly_dataset.json
Raw https://raw.githubusercontent.com/data2health/schemas/master/Dataset/examples/wellderly/wellderly_dataset.json
"""

import logging
import sys

from discovery.utils.indexing import add_dataset_by_url

if __name__ == "__main__":
    assert len(sys.argv) == 4
    logging.basicConfig(level='DEBUG')
    print(add_dataset_by_url(
        url=sys.argv[1],
        user=sys.argv[2],
        private=sys.argv[3] in ('true', '1'),
        class_id='ctsa::bts:CTSADataset'
    ))
