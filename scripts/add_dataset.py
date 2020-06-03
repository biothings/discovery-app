"""
Try:

python -m scripts.add_dataset --help

Test Data:
Git https://github.com/data2health/schemas/blob/master/Dataset/examples/wellderly/wellderly_dataset.json
Raw https://raw.githubusercontent.com/data2health/schemas/master/Dataset/examples/wellderly/wellderly_dataset.json
"""

import logging

from tornado.options import options, parse_command_line

from discovery.utils.controllers import DatasetController

options.define('url')
options.define('user', default='cwu@scripps.edu')
options.define('private', default=False, type=bool)
options.define('classid', default='ctsa::bts:CTSADataset')
logging.getLogger('elasticsearch').setLevel('WARNING')


if __name__ == "__main__":
    parse_command_line()
    assert options.url
    print(DatasetController.add(
        doc=options.url,
        user=options.user,
        private=options.private,
        class_id=options.classid
    ))
