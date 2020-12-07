"""
Author: Stepchenko Pavlo

"""

import pandas as pd


class Panda:
    """
    A class that processes, sorts, and outputs the required information using Pandas methods
    """

    def __init__(self, name_csv, encoding, output):
        self.name_csv = name_csv
        self.output = output
        self.encoding = encoding
        self.problem = pd.read_csv(name_csv, sep=";", encoding=encoding,
                                   dtype={'dd': 'int64', 'yyyy': 'int64', 'name1': 'str', 'keywords': 'object',
                                          'name2': 'str',
                                          'stat': 'int64', 'mm': 'int64'})

    def check_csv_data(self):
        # checks restrictions on csv file

        check1 = self.problem[self.problem.yyyy == 4].empty
        check2 = self.problem[self.problem.name1.str.len() > 20].empty
        check3 = self.problem[self.problem.name2.str.len() > 21].empty
        check4 = self.problem[self.problem.keywords.str.len() > 56].empty
        check5 = self.problem[(self.problem.stat < 0) | (self.problem.stat > 1000)].empty
        if check1 and check2 and check3 and check5 and check4:
            return True
        else:
            raise CsvIncorrect

    def fit(self, json_data):
        # checks the correspondence of the main and additional files

        if json_data['amount_records'] == len(self.problem) and json_data[
            'amount_problems'] == self.problem.keywords.nunique():
            return True
        else:
            raise DataConflict

    def __sort(self):
        # is looking for students according to variant

        res_a = self.problem.groupby(['keywords', 'name2', "name1"]).stat.idxmax()
        res0 = res_a.sort_values()
        self.res = self.problem.loc[res0].apply(lambda rec: rec.stat < 90, axis=1)

    def __max_ky(self):
        max_keywords = self.problem.loc[self.res].groupby('keywords').name1.count().nlargest(1, keep='all')

        self.problem.loc[
            self.problem.keywords.isin(max_keywords.index) & (self.problem.index.isin(self.res)), ['keywords', 'name2',
                                                                                                   'name1',
                                                                                                   'stat',
                                                                                                   'yyyy']].sort_values(
            by=['keywords'])

    def __creating_merge(self):
        # create two additional columns

        groups = self.problem.loc[self.res].groupby('keywords')
        self.keyword = groups.stat.mean()
        self.trying = groups.keywords.count()
        self.keyword.name = 'mean'
        self.trying.name = 'attempts'

    def __merge_use(self):
        # adding two columns and sort final info

        result1 = pd.merge(self.problem.loc[self.res], self.keyword, left_on='keywords', right_index=True)
        self.result = pd.merge(result1, self.trying, left_on='keywords', right_index=True)
        self.result.sort_values(by=['attempts', 'mean', 'stat'],
                                ascending=[False, False, False], inplace=True)

    def __out(self):
        # write info in output file

        with open(self.output, 'w') as f:
            var = 0
            for label, g in self.result.groupby(['keywords', 'attempts', 'mean']).groups.items():
                f.write("\n" * var + " {} {} {}".format(*label))
                for i in g:
                    tmp = self.problem.iloc[i]
                    f.write('\n\t {} {} {} {}'.format(tmp.name2, tmp.name1, tmp.stat, tmp.yyyy))
                var = 1

    def runner(self):
        Panda.__sort(self)
        Panda.__max_ky(self)
        Panda.__creating_merge(self)
        Panda.__merge_use(self)
        Panda.__out(self)


class DataConflict(BaseException):
    pass


class CsvIncorrect(BaseException):
    pass
