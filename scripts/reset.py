'''
    Reset es indexes

    - Remove existing indexes
    - Data will be deleted

'''

from tornado.log import enable_pretty_logging

from discovery.utils.indices import reset_data

if __name__ == "__main__":
    enable_pretty_logging()
    reset_data()
