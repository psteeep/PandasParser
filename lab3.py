"""
Author: Stepchenko Pavlo

"""

import json
import sys
from loader import load


def info_about_doer():
    print("Stepchenko Pavlo Victorovich, K13, Variant 9")


def variant9():
    print("Знайти всі задачі, які в кожній спробі були розв'язані не більше ніж на 90%. Вивести по них інформації:\n"
          "умова, кількість спроб, середня розв'язуваність(округлена до цілого)\n"
          "на наступних рядках, починаючи з табуляції вивести спроби по цих задачах (по одній на рядок):\n"
          "прізвище, ім'я, відсоток набраних балів, рік\n"
          "Сортування: прізвище, ім'я, відсоток набраних балів (за спаданням), рік\n"
          "Задачі сортуємо: кількість спроб (з вионаним округленням), умова.\n")


def load_ini(cfg):
    """
    A function that downloads a parameter file and checks its contents
    :param cfg: name config file
    :return: dict with params
    """
    with open(cfg, encoding="UTF=8") as p:
        conf = json.load(p)
        if 'input' in conf and 'output' in conf:
            if 'csv' in conf['input'] and 'json' in conf['input'] and 'encoding' in conf['input'] and 'fname' in \
                    conf['output'] and 'encoding' in conf['output']:
                return conf
            else:
                raise KeyError
        else:
            raise KeyError


def main(init_name):
    """
    The main function that reads the configuration file and transmits information from it to the load function
    """

    info_about_doer()
    variant9()
    print("*****")
    try:
        print("ini {0}:".format(init_name), end="")
        conf = load_ini(init_name)
        print("OK")
        load(conf['input']['csv'], conf['input']['json'], conf['output']['fname'], conf['input']['encoding'])
    except KeyError:
        print("\n***** init file error *****")


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except FileNotFoundError:
        print('***** program aborted *****')
        print('***** command line error *****')
    except FileExistsError:
        print('***** program aborted *****')
        print('***** command line error *****')
    except IndexError:
        print('***** program aborted *****')
        print('***** command line error *****')