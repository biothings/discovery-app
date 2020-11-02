"""
Try:

python -m scripts.add_dataset --help

Test Data:
Git https://github.com/data2health/schemas/blob/master/Dataset/examples/wellderly/wellderly_dataset.json
Raw https://raw.githubusercontent.com/data2health/schemas/master/Dataset/examples/wellderly/wellderly_dataset.json
"""

import logging

from tornado.options import options, parse_command_line

from discovery.registry import datasets

options.define('url')
options.define('user', default='cwu@scripps.edu')
options.define('schema', default='ctsa::bts:CTSADataset')
options.define('private', default=False, type=bool)

logging.getLogger('elasticsearch').setLevel('WARNING')


if __name__ == "__main__":
    parse_command_line()
    assert options.url
    print(datasets.add(
        doc=options.url,
        user=options.user,
        schema=options.schema,
        private=options.private
    ))
