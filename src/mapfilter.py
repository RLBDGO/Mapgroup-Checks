from pandas import DataFrame, read_csv, Series


class MapFilter(object):

    '''
    Lädt die Daten hinsichtlich
    eines bestimmten Datenformats
    (Stand: 3.12.2019)
    '''

    def __init__(self, file_path, info_1, info_2, info_3, info_4):
        pass

    def load_data(self, file_path):

        '''
        lädt Daten
        '''

        raw_data = DataFrame(read_csv(r'{}'.format(file_path),
                                           sep=';',
                                           encoding='ISO-8859-1',
                                           header=None))

        return raw_data

    def preprocess(self, data, columns):

        '''
        Löscht alle Spalten bis auf columns
        in data
        '''

        # zu löschende Spalten
        to_drop = [c for c in data.columns
                   if c not in columns]

        return data.drop(to_drop, axis=1)

    def measure_coherence(self, to_compare_1, to_compare_2):
        '''
        Misst relative Übereinstimmung
        von zu vergleichenden Infos:

        Übereinstimmungsgrad ergibt sich
        relativem Anteil an Elementen
        in kleinerer Menge von Infos, die
        mit Elementen der größeren Menge
        übereinstimmen
        '''

        # unique zu vergleichende Instanzen
        to_compare_1_unique = self.remove_duplicates(to_compare_1)
        to_compare_2_unique = self.remove_duplicates(to_compare_2)

        # Maß
        measure = lambda x, y: sum([int(x[i] == y[j])
                                    for i in range(len(x))
                                    for j in range(len(y))]) / len(x) if len(x) < len(y) \
            else sum([int(x[i] == y[j])
                      for i in range(len(x))
                      for j in range(len(y))]) / len(y)

        # Resultat
        result = measure(to_compare_1_unique, to_compare_2_unique)

        return result

    def remove_duplicates(self, List):

        '''
        Duplikate in Liste entfernen
        '''

        unique_list = []

        for element in List:
            if element not in unique_list:
                unique_list.append(element)

        return unique_list

    def parse_infos_singleton(self, data, columns):

        '''
        Holt sich Zeilen von columns und die
        darin enthaltenen Infos in brauchbarem
        Format für compare_singleton_infos
        '''

        # Namen der zu vergleichenden Instanzen
        to_compare = [(data[columns[1]].iloc[i], i) for i in range(data[columns[1]].size)]

        # Merkmale der zu vergleichenden Instanzen
        infos = [(to_compare[i][0],
                  Series(data[columns[2]][data[columns[1]] == str(to_compare[i][0])]).tolist(),
                  Series(data[columns[3]][data[columns[1]] == str(to_compare[i][0])]).tolist(),
                  list(set(Series(data[columns[0]][data[columns[1]] == str(to_compare[i][0])]).tolist())))
                 for i in range(len(to_compare))]

        # zu vergleichende Merkmale
        compare_by = []

        # zu vergleichende Merkmale herausparsen
        for i in range(len(infos)):
            for j in range(len(infos[i][2])):
                if '(' in infos[i][2][j]:
                    info = str(infos[i][2][j])
                    value = info.replace('(', '').replace(')', '').replace(' ', '').split(',')
                    compare_by += [(value, i)]

        for i in range(len(infos)):
            for j in range(len(compare_by)):
                if i == compare_by[j][1]:
                    for k in range(len(compare_by[j][0])):
                        infos[i][2].append(compare_by[j][0][k])

        return infos

    def parse_infos_tuple(self, base):

        '''
        Holt sich Zeilen von columns und die
        darin enthaltenen Infos in brauchbarem
        Format
        '''

        # Anzahl an Merkmalen
        n = 2

        # Infos zu zweistelligen Mapgruppen herausparsen
        infos = self.remove_duplicates([(b[0], b[1], b[2], b[3]) for b in base
                                        if len(b[1]) == n])

        # Vergleichsdaten zurechtstutzen
        for info in infos:
            for e in info[2]:
                if '(' in e:
                    info[2].remove(e)

        # Merkmal mitsamt Ausprägung herausparsen
        # & in Infos einbinden
        for i in range(len(infos)):
            infos[i] = list(infos[i])

        for info in infos:
            info += [sorted([info[2][0:2]])]

        return infos

    def parse_infos_triple(self, base):

        '''
        Holt sich Zeilen von columns und die
        darin enthaltenen Infos in brauchbarem
        Format
        '''

        # Anzahl an Merkmalen
        n = 3

        # Infos zu zweistelligen Mapgruppen herausparsen
        infos = self.remove_duplicates([(b[0], b[1], b[2], b[3]) for b in base
                                        if len(b[1]) == n])

        # Vergleichsdaten zurechtstutzen
        for info in infos:
            for e in info[2]:
                if '(' in e:
                    info[2].remove(e)

        # Merkmal mitsamt Ausprägung herausparsen
        # & in Infos einbinden
        for i in range(len(infos)):
            infos[i] = list(infos[i])

        for info in infos:
            info += [sorted([info[2][0:3]])]

        return infos