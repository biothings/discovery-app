'''
    Create Indexes and Index Core Datasources
    Specify logging level by:
         --logging=debug|info|warning|error|none
'''


from tornado.options import parse_command_line

from discovery.utils.indices import setup_data

if __name__ == "__main__":
    parse_command_line()
    print(setup_data().result())
