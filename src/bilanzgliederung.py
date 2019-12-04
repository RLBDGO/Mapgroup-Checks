from src.mapfilter import MapFilter
from pandas import DataFrame, read_csv, Series


class BilanzGliederung(MapFilter):

    def __init__(self, file_path, info_1, info_2, info_3, info_4, info_5, info_6):

        super().__init__(file_path, info_1, info_2, info_3, info_4)

        # Daten laden
        self.raw_data = DataFrame(read_csv(r'{}'.format(file_path),
                                           sep=';',
                                           encoding='ISO-8859-1',
                                           header=None))
        # Relevante Spalten
        self.columns = [info_1, info_2, info_3,
                        info_4, info_5, info_6]

        # vorverarbeitete Daten
        self.data = self.preprocess(data=self.raw_data,
                                    columns=self.columns).drop([0],
                                                               axis=0)

        # herausgeparste Infos
        # zu einstelligen Mapgruppen
        self.infos_singleton = self.parse_infos(data=self.data,
                                                columns=self.columns)

    def parse_infos(self, data, columns):

        '''
        Holt sich Zeilen von columns und die
        darin enthaltenen Infos in brauchbarem
        Format für compare_singleton_infos_
        '''

        # Namen der zu vergleichenden Instanzen
        to_compare = [(data[columns[0]].iloc[i], i) for i in range(data[columns[1]].size)]

        # Merkmale der zu vergleichenden Instanzen
        infos = [(to_compare[i][0],
                  Series(data[columns[1]][data[columns[0]] == str(to_compare[i][0])]).tolist(),
                  Series(data[columns[2]][data[columns[0]] == str(to_compare[i][0])]).tolist(),
                  Series(data[columns[3]][data[columns[0]] == str(to_compare[i][0])]).tolist(),
                  Series(data[columns[4]][data[columns[0]] == str(to_compare[i][0])]).tolist(),
                  list(set(Series(data[columns[5]][data[columns[0]] == str(to_compare[i][0])]).tolist())))
                 for i in range(len(to_compare))]

        # zu vergleichende Merkmale
        compare_by = []

        # zu vergleichende Merkmale herausparsen
        for i in range(len(infos)):
            for j in range(len(infos[i][-1])):
                if '(' in infos[i][-1][j]:
                    info = str(infos[i][-1][j])
                    value = info.replace('(', '').replace(')', '').replace(' ', '').split(',')
                    compare_by += [(value, i)]

        for i in range(len(infos)):
            for j in range(len(compare_by)):
                if i == compare_by[j][1]:
                    for k in range(len(compare_by[j][0])):
                        infos[i][-1].append(compare_by[j][0][k])

        return infos



test = BilanzGliederung('test_case_bg/BilanzGliederung.csv', 10, 11, 12, 13, 14, 15)
#print(test.data)
print(test.parse_infos(data=test.data, columns=test.columns))