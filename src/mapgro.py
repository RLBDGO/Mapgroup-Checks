from pandas import DataFrame, read_csv, Series

class BBS(object):

    
    def __init__(self, file_path, quelle, mapgruppe, merkmal, werte):

        # Daten laden
        self.raw_data = DataFrame(read_csv(r'{}'.format(file_path),
                                       sep=';',
                                       encoding='ISO-8859-1',
                                       header=None))

        # Relevante Spalten
        self.columns = [quelle, mapgruppe, merkmal, werte]

        # vorverarbeitete Daten
        self.data = self.preprocess(data=self.raw_data,
                                    columns=self.columns).drop([0],
                                                               axis=0)

        # herausgeparste Infos
        self.infos = self.parse_infos(data=self.data,
                                      columns=self.columns)

        # Resultate
        self.results = self.compare_singleton_instances(self.infos) + \
                        self.compare_tuple_instances(self.infos)
        
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

    def preprocess(self, data, columns):

        '''
        Löscht alle Spalten bis auf columns
        in data
        '''

        # zu löschende Spalten
        to_drop = [c for c in data.columns
                   if c not in columns]

        return data.drop(to_drop, axis=1)

    def parse_infos(self, data, columns):

        '''
        Holt sich Zeilen von columns und die
        darin enthaltenen Infos in brauchbarem
        Format
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

    def remove_duplicates(self, List):

        '''
        Duplikate in Liste entfernen
        '''

        unique_list = []

        for element in List:
            if element not in unique_list:
                unique_list.append(element)

        return unique_list

    def compare_singleton_instances(self, infos):

        '''
        Vergleicht jene Instanzen miteinander
        die lediglich ein Merkmal aufweisen
        '''

        # Anzahl der Infos
        n = 1

        # Vergleichsdaten
        data = [(info[0], info[2], info[3]) for info in infos
                if len(info[1]) == n]

        # Namen der zu vergleichenden Instanzen
        to_compare = [info[0] for info in data]

        # Längen der Werte-Arrays
        lengths = [len(info[1]) for info in data]

        # Maximale Länge
        fill_up_to = max(lengths)-n

        # Infos bzgl. der Werte  zurechtstutzen
        # betrachte Struktur von data,
        # um verstehen, was hier passiert
        for i in range(len(data)):
            if '(' in data[i][1][0]:
                data[i][1].remove(data[i][1][0])

        # Infos zusammenfassen
        value_infos = [info[1] for info in data]

        # da wir im Anschluss einen Dataframe nutzen
        # müssen wir beachten, dass alle Infos-arrays
        # gleich lang sein müssen
        # hier werden Infos im Hinblick auf fill_up_to
        # normalisiert
        for info in value_infos:
            while len(info) < fill_up_to:
                info += [info[0]]

        # Dataframe/Matrix bauen anhanddessen
        # wir alle Instanzen miteinander
        # vergleichen können 
        df = DataFrame(dict(zip(to_compare, value_infos)))

        # Werte in df konvertieren
        for c in df.columns:
            df[c] = df[c].astype('int64')

        # Kohärenzmaß anwenden
        coherence_measures = [(to_compare_1, to_compare_2, self.measure_coherence(df[to_compare_1], df[to_compare_2]))
                              for to_compare_1 in df.columns for to_compare_2 in df.columns
                              if to_compare_1 != to_compare_2]

        # herausparsen von Dopplungen
        # unter coherence_measures
        for m1 in coherence_measures:
            for m2 in coherence_measures:
                if (m1[0] == m2[1] and m1[1] == m2[0]):
                    coherence_measures.remove(m2)

        # potenzielle Inkonsistenzen
        pot_inc = []

        # potenziell inkonsistent gdw. maß > 0
        for m in coherence_measures:
            if m[2] > 0:
                pot_inc += [[m[0], m[1], m[2]]]

        # notwendige infos um herauszufinden
        # ob wirklich inkonsistent, herausholen
        for i in range(len(pot_inc)):
            for j in range(len(infos)):
                if pot_inc[i][0] == infos[j][0]:
                    pot_inc[i] += infos[j][3]
                if pot_inc[i][1] == infos[j][0]:
                    pot_inc[i] += infos[j][3]
        for i in range(len(pot_inc)):
            for j in range(len(infos)):
                if pot_inc[i][0] == infos[j][0]:
                    pot_inc[i] += infos[j][1]
                if pot_inc[i][1] == infos[j][0]:
                    pot_inc[i] += infos[j][1]
        for i in range(len(pot_inc)):
            for j in range(len(infos)):
                if pot_inc[i][0] == infos[j][0]:
                    pot_inc[i] += [len(set(infos[j][2]))]
                if pot_inc[i][1] == infos[j][0]:
                    pot_inc[i] += [len(set(infos[j][2]))]


        # inkonsistente/inkompatible Instanzen
        inc = [[pi[0], pi[1], pi[2], int(pi[-3] != pi[-4]), pi[-2], pi[-1]] for pi in pot_inc
               if (pi[-5] == pi[-6] or pi[-3] != pi[-3])]

        output_messages = []
        incom = []
        incon = []

        if len(inc) != 0:
            for i in inc:
                if i[-3] == 1:
                    incom += [i]
                else:
                    incon += [i]
        else:
            output_messages = ''

        for i in incom:
            if i[-1] <= i[-2]:
                i.remove(i[-2])
                i += [int(i[-1]*i[2])]
            else:
                i.remove(i[-1])
                i += [int(i[-1]*i[2])]

        for i in range(len(incon)):
            if incon[i][-1] <= incon[i][-2]:
                incon[i].remove(incon[i][-2])
                incon[i] += [int(incon[i][-1]*incon[i][2])]
            else:
                incon[i].remove(incon[i][-1])
                incon[i] += [int(incon[i][-1]*incon[i][2])]

        for i in incom:
            output_messages += [f'| Inkompatibilität zwischen {i[0]} und {i[1]}   |   Anzahl gleicher Elemente: {i[-1]}   |']
        for i in incon:
            output_messages += [f'| Inkonsistenz zwischen {i[0]} und {i[1]}       |   Anzahl gleicher Elemente: {i[-1]}   |']

        return output_messages

    def compare_tuple_instances(self, infos):

        # Anzahl der Infos
        n = 2

        # Vergleichsdaten
        data = [(info[0], info[2], info[3]) for info in infos
                if len(info[1]) == n]

        # Vergleichsdaten zurechtstutzen
        for i in range(len(data)):
            if '(' in data[i][1][0]:
                data[i][1].remove(data[i][1][0])

        # Vergleichstupel bilden & in Vergleichsdaten einbauen
        Tuple = []

        for i in range(len(data)):
            t_1 = data[i][1][0]
            Tuple += [(t_1, data[i][1][j]) for j in range(len(data[i][1]))
                      if (t_1 != data[i][1][j])]

        for i in range(len(data)):
            data[i] = list(data[i])

        for i in range(len(data)):
            l_1 = len(data[i][1]) - (n-1)
            l_2 = len(data[i][1])
            for _ in range(0, l_1):
                data[i][1] += [Tuple[0]]
                Tuple.pop(0)
            for _ in range(0, l_2):
                data[i][1].pop(0)
                data[i][1] += [[data[i][1][j][0]] for j in range(len(data[i][1]))]
                data[i][1] = self.remove_duplicates((data[i][1]))
                data[i][1].pop(-2)

        data = self.remove_duplicates(data)

        # Verbesserungsoptionen eruieren
        opt = []

        for info_1 in data:
            for info_2 in data:
                if info_1[1][-1] == info_2[1][-1] and info_1[-1] == info_2[-1] and info_1[1] != info_2[1]:
                    opt += [(info_1[0], info_2[0])]
                    for o_1 in opt:
                        for o_2 in opt:
                            if o_1[0] == o_2[1] and o_2[0] == o_1[1]:
                                opt.remove(o_2)

        # Hinzunahme von Arraylängen der
        # jeweiligen Mapgruppen in opt
        for i in range(len(opt)):
            opt[i] = list(opt[i])
        for o in opt:
            for info in data:
                if o[0] == info[0]:
                    o += [len(info[1])]
                if o[1] == info[0]:
                    o += [len(info[1])]

        # Längen der Werte-Arrays
        lengths = [len(info[1]) for info in data]

        # Maximale Länge
        fill_up_to = max(lengths)

        # Namen der zu vergleichenden Instanzen
        to_compare = [info[0] for info in data]

        # Infos zusammenfassen
        value_infos = [info[1] for info in data]

        # da wir im Anschluss einen Dataframe nutzen
        # müssen wir beachten, dass alle Infos-arrays
        # gleich lang sein müssen
        # hier werden Infos im Hinblick auf fill_up_to
        # normalisiert
        for info in value_infos:
            while len(info) < fill_up_to:
                info += [info[0]]

        # Dataframe/Matrix bauen anhanddessen
        # wir alle Instanzen miteinander
        # vergleichen können
        df = DataFrame(dict(zip(to_compare, value_infos)))

        # Kohärenzmaß anwenden
        coherence_measures = [(to_compare_1, to_compare_2, self.measure_coherence(df[to_compare_1], df[to_compare_2]))
                              for to_compare_1 in df.columns for to_compare_2 in df.columns
                              if to_compare_1 != to_compare_2]

        # herausparsen von Dopplungen
        # unter coherence_measures
        for m1 in coherence_measures:
            for m2 in coherence_measures:
                if (m1[0] == m2[1] and m1[1] == m2[0]):
                    coherence_measures.remove(m2)

        # coherence_measures info
        # opt einbinden
        for o in opt:
            for m in coherence_measures:
                if o[0] == m[0] and o[1] == m[1] or o[1] == m[0] and o[0] == m[1]:
                    o += [m[2]]

        # Schnitt zwischen coherence measures &
        # opt bzgl. Maß > 0 eruieren
        for m in coherence_measures:
            for o in opt:
                if m[2] > 0 and ((m[0] == o[0] and m[1] == o[1]) or (m[1] == o[0] and m[0] == o[1])):
                    coherence_measures.remove(m)

        # Hinzunahme von Arraylängen der
        # jeweiligen Mapgruppen in coherence_measures
        for i in range(len(coherence_measures)):
            coherence_measures[i] = list(coherence_measures[i])
        for i in range(len(coherence_measures)):
            coherence_measures[i] = list(coherence_measures[i])
        for m in coherence_measures:
            for info in data:
                if m[0] == info[0]:
                    m += [len(info[1])]
                if m[1] == info[0]:
                    m += [len(info[1])]

        # Anzahl gleicher Elemente
        # in opt berechnen
        for o in opt:
            if o[-2] <= o[-3]:
                o += [o[-2]*o[-1]]
            else:
                o += [o[-3] * o[-1]]

        # Inkonsistenzen herausparsen
        inc = []
        for m in coherence_measures:
            if m[2] > 0:
                inc += [m]

        # Anzahl gleicher Elemente
        # in inc berechnen
        for i in inc:
            if i[-1] <= o[-2]:
                i += [i[-1]*i[-3]]
            else:
                i += [i[-2] * i[-3]]

        # Output konfigurieren
        output_messages = []

        if len(inc) != 0 or len(opt) != 0:
            for i in inc:
                try:
                    output_messages += [f'| Inkonsistenz zwischen {i[0]} und {i[1]}       |   Anzahl gleicher Elemente: {int(i[-1])}   |']
                except Exception:
                    None
            for o in opt:
                try:
                    output_messages += [f'| Verbesserung zwischen {o[0]} und {o[1]}       |   Anzahl gleicher Elemente: {int(o[-1])}   |']
                except Exception:
                    None
        else:
            output_messages = ''

        return output_messages

o = BBS('test_case/testdata.csv', 5, 10, 13, 15)
#print(o.compare_tuple_instances(o.infos, o.data))
#print(o.compare_singleton_instances(o.infos))
#print(o.results)