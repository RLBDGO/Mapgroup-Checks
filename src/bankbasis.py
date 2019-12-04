from src.mapfilter import MapFilter
from pandas import DataFrame, read_csv


class BankBasis(MapFilter):

    def __init__(self, file_path, info_1, info_2, info_3, info_4):

        super().__init__(file_path, info_1, info_2, info_3, info_4)

        # Daten laden
        self.raw_data = DataFrame(read_csv(r'{}'.format(file_path),
                                           sep=';',
                                           encoding='ISO-8859-1',
                                           header=None))
        # Relevante Spalten
        self.columns = [info_1, info_2, info_3, info_4]

        # vorverarbeitete Daten
        self.data = self.preprocess(data=self.raw_data,
                                    columns=self.columns).drop([0],
                                                               axis=0)

        # herausgeparste Infos
        # zu einstelligen Mapgruppen
        self.infos_singleton = self.parse_infos_singleton(data=self.data,
                                                          columns=self.columns)

        # Resultat bzgl.
        # einstelliger Mapgruppen
        self.singleton_result = self.compare_singleton_instances(infos=self.infos_singleton)

        # herausgeparste Infos
        # zu zweistelligen Mapgruppen
        self.infos_tuple = self.parse_infos_tuple(base=self.infos_singleton)

        # Verbesserungsoptionen unter
        # zweistellige Mapgruppen
        self.tuple_opt = self.opt_candidates(data=self.infos_tuple,
                                             n=2)

        # Inkonsistenzen unter
        # zweistelligen Mapgruppen
        self.tuple_inc = self.inc_candidates(data=self.infos_tuple)

        # herausgeparste Infos
        # zu dreistelligen Mapgruppen
        self.infos_triple = self.parse_infos_triple(base=self.infos_singleton)

        # Verbesserungsoptionen unter
        # dreistelligen Mapgruppen
        self.triple_opt = self.opt_candidates(data=self.infos_triple,
                                              n=3)

        # Inkonsistenzen unter
        # dreistelligen Mapgruppen
        self.triple_inc = self.inc_candidates(data= self.infos_triple)

        # Ergebnisse
        self.result = self.singleton_result + self.tuple_opt +\
                      self.triple_opt + self.tuple_inc + self.triple_inc

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
        fill_up_to = max(lengths) - n

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
        coherence_measures = [
            (to_compare_1, to_compare_2, self.measure_coherence(df[to_compare_1], df[to_compare_2]))
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
                i += [int(i[-1] * i[2])]
            else:
                i.remove(i[-1])
                i += [int(i[-1] * i[2])]

        for i in range(len(incon)):
            if incon[i][-1] <= incon[i][-2]:
                incon[i].remove(incon[i][-2])
                incon[i] += [int(incon[i][-1] * incon[i][2])]
            else:
                incon[i].remove(incon[i][-1])
                incon[i] += [int(incon[i][-1] * incon[i][2])]

        for i in incom:
            output_messages += [f'  INKOMPATIBILITAET   |   Inkompatibilitaet zwischen {i[0]} und {i[1]}     ']
        for i in incon:
            output_messages += [f'  INKONSISTENZ        |   Inkonsistenz zwischen {i[0]} und {i[1]}          ']

        return output_messages

    def opt_candidates(self, data, n):

        '''
        Findet Mapgruppen, die
        eine potenzielle Verbesserungsoption
        aufweisen, d.h. sich integrieren lassen
        '''

        # Wir prüfen, wie viele der jeweils
        # ersten Elemente der Merkmalsausprägungen
        # übereinstimmen
        compare = lambda x, y: sum([int(i == j) for i in x for j in y])/n

        # Wir prüfen ob selbe Quelle gegeben ist
        check = lambda x, y: x[-2] == y[-2]

        # herausparsen
        results = []

        for i in data:
            for j in data:
                value = compare(self.remove_duplicates(i[-1][0]),
                                self.remove_duplicates(j[-1][0]))
                if value >= 0.5 and value < 1 and (check(i, j) == True) and i != j:
                    results += [(i[0], j[0], value)]

        for r_1 in results:
            for r_2 in results:
                if r_1[0] == r_2[1] and r_1[1] == r_2[0]:
                    results.remove(r_2)

        # output
        output_messages = []

        for r in results:
            output_messages += [f'  INTEGRATION         |   Integration zwischen {r[0]} und {r[1]} moeglich  ']

        return output_messages

    def inc_candidates(self, data):

        '''
        Findet Duplikate
        '''

        # herausparsen
        results = []

        for i in data:
            for j in data:
                if i[1] == j[1] and i[2] == i[2] and i[3] == j[3] and i[4] == j[4] and i != j:
                    results += [(i[0], j[0])]

        for r_1 in results:
            for r_2 in results:
                if r_1[0] == r_2[1] and r_1[1] == r_2[0]:
                    results.remove(r_2)

        # output
        output_messages = []

        for r in results:
            output_messages += [f'  INKONSISTENZ        |   Inkonsistenz zwischen {r[0]} und {r[1]}          ']

        return output_messages