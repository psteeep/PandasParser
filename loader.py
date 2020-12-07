"""
Author: Stepchenko Pavlo

"""


import json
from pandas_using import Panda, DataConflict, CsvIncorrect


def load_stat(name_json, encoding):
    """
    A function that loads an additional file and returns statistics
    :param name_json: json file name
    :param encoding: json file encoding
    :return: dict
    """
    with open(name_json, encoding=encoding) as json_file:
        stat = json.load(json_file)
        if "amount_problems" in stat and "amount_records" in stat:
            return stat
        else:
            raise KeyError


def load(name_csv, name_json, output, encoding):
    """
    A function that creates a Pandas class object for loading and processing a csv file,
     as well as loading an json file, comparing their information and outputting the processed
     information to the output file
    :param name_csv: csv file name
    :param name_json: json file name
    :param output: output txt file name
    :param encoding: encoding of files
    :return: output file
    """
    try:
        print("input-csv {0}:".format(name_csv), end="")
        information = Panda(name_csv, encoding, output)
        information.check_csv_data()
        print("OK")
        print("input-json {0}:".format(name_json), end="")
        stat = load_stat(name_json, encoding)
        print("OK")
        print("json?=csv:", end="")
        information.fit(stat)
        print("OK")
        print("output {0}:".format(output), end="")
        information.runner()
        print("OK")
    except KeyError:
        print("\n***** incorrect input json-file *****")
    except PermissionError:
        print("\n***** json file error *****")
    except DataConflict:
        print("\n***** json file error *****")
    except CsvIncorrect:
        print("\n***** incorrect input csv-file *****")
