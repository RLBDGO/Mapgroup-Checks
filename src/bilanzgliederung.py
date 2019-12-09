from src.mapfilter import MapFilter
from pandas import DataFrame, read_csv, Series


class BilanzGliederung(MapFilter):

    def __init__(self, file_path, info_1, info_2, info_3, info_4, info_5):

        super().__init__(file_path, info_1, info_2, info_3, info_4)

        # Daten laden
        self.raw_data = DataFrame(read_csv(r'{}'.format(file_path),
                                           sep=';',
                                           encoding='ISO-8859-1',
                                           header=None))

        # BG-Schlüssel
        self.bgs = info_1

        # Mapgruppe
        self.mg = info_2

        # Merkmal
        self.m = info_3

        # Relation BalanceAmountEUR@>
        self.ba = info_4

        # Werte
        self.v = info_5

        # Relevante Spalten
        self.columns = [self.bgs, self.mg, self.m,
                        self.ba, self.v]

        # vorverarbeitete Daten
        self.data = self.preprocess(data=self.raw_data,
                                    columns=self.columns).drop([0],
                                                               axis=0)

        # herausgeparste Infos
        self.infos = self.parse_infos(data=self.data,
                                      columns=self.columns)

        # Resultat
        self.result = self.compare_tuples() + self.compare_triples()

    def parse_infos(self, data, columns):
        '''
        Holt sich grundlegende Infos
        in brauchbarem Format
        '''

        # Mapgruppe -> [ [Mapgruppe], [] ]
        infos = self.remove_duplicates([[data[columns[1]].iloc[i], []]
                                        for i in range(data[columns[1]].size)])

        # KontoartCodes -> [ KontoartCode ]
        koarcs = Series(data[columns[4]][data[columns[2]] == 'KontoartCode']).tolist()

        # SachKontoNr -> [ SachKontoNr ]
        sakos = [list(set(Series(data[columns[4]][data[columns[1]] == str(infos[i][0])]).tolist()))
                 for i in range(len(infos))]

        # Sako = 0
        # wird nicht berücksichtigt
        for s in sakos:
            for i in s:
                if i == '0':
                    s.remove(i)

        # BalanceAmountEUR@>-Relation
        #  -> [ (Mapgruppe, [Relationen]) ]
        bas = [(info[0],
                Series(data[columns[3]][data[columns[1]] == str(info[0])]).tolist())
               for info in infos]

        # Bilanzgliederungsschlüssel
        bs = [(info[0],
               self.remove_duplicates(Series(data[columns[0]][data[columns[1]] == str(info[0])]).tolist()))
              for info in infos]

        # sakos herausparsen
        for s in sakos:
            for i in range(len(s)):
                if '(' in s[i]:
                    info = str(s[i])
                    value = info.replace('(', '').replace(')', '').replace(' ', '').split(',')
                    s += value
                    s.remove(info)

        # Tupel bilden
        # aus koarcs und sakos
        # infos -> [ Mapgruppe, [(koarc, sako)] ]
        for i in range(len(sakos)):
            infos[i][1] += [(koarcs[i], sakos[i][j])
                            for j in range(len(sakos[i]))
                            if koarcs[i] != sakos[i][j]]

        # BalanceAmountEUR@>-Relation
        # wenn gegeben, hinzufügen
        for i in range(len(infos)):
            rs = bas[i][1]
            for r in rs:
                if r in ['>', '<', '>=', '<=']:
                    infos[i] += [r]

        # Bilanzgliederungsschlüssel
        # hinzufügen
        for i in range(len(infos)):
            b = bs[i][1]
            for s in b:
                infos[i] += [s]

        return infos

    def compare_tuples(self):
        '''
        Auf Basis der herausgeparsten
        Infos werden zweistellige
        Mapgruppen miteinander verglichen
        '''

        # Tupel sind zweistellig
        n = 2

        # zweistellige Mapgruppen
        # herausparsen
        infos = [info for info in self.infos
                 if len(info) == n+1]

        # Kohärenzmaß anwenden
        # -> [ (Mapgruppe 1, Mapgruppe 2, Wert,
        #       Bilanzgliederungsschlüssel 1,
        #       Bilanzgliederungsschlüssel 2) ]
        coherence_measures = []

        for i in infos:
            for j in infos:
                if i != j:
                    coherence_measures += [(i[0], j[0],
                                            self.measure_coherence(i[-2], j[-2]),
                                            i[-1], j[-1])]

        # herausparsen von Dopplungen
        # unter coherence_measures
        for m1 in coherence_measures:
            for m2 in coherence_measures:
                if (m1[0] == m2[1] and m1[1] == m2[0]):
                    coherence_measures.remove(m2)

        # Probleme herausfinden
        # p = Bilanzgliederungsschlüssel gleich
        # duplikat gdw. Maß > 0 & p
        # integriere gdw. Maß == 1 & p
        # inkonsistent gdw. Maß > 0 & not p
        inc = []
        intg = []
        dup = []

        for m in coherence_measures:
            if 0 < m[2] < 1 and m[3] == m[4]:
                intg += [[m[0], m[1], m[2]]]
            elif m[2] == 1 and m[3] == m[4]:
                dup += [[m[0], m[1], m[2]]]
            elif m[2] > 0 and m[3] != m[4]:
                inc += [[m[0], m[1], m[2]]]

        # Output konfigurieren
        output_messages = []

        for i in intg:
            output_messages += [f'  INTEGRATION         |   Integration zwischen {i[0]} und {i[1]} moeglich  ']
        for i in dup:
            output_messages += [f'  DUPLIKAT            |   {i[0]} und {i[1]} sind Duplikate                 ']
        for i in inc:
            output_messages += [f'  INKONSISTENZ        |   Inkonsistenz zwischen {i[0]} und {i[1]}          ']

        return output_messages

    def compare_triples(self):
        '''
        Auf Basis der herausgeparsten
        Infos werden dreistellige
        Mapgruppen miteinander verglichen
        '''

        # Tripel sind zweistellig
        n = 3

        # zweistellige Mapgruppen
        # herausparsen
        infos = [info for info in self.infos
                 if len(info) == n+1]

        # Kohärenzmaß anwenden
        # -> [ (Mapgruppe 1, Mapgruppe 2, Wert,
        #       BalanceAmountEUR@> 1,
        #       BalanceAmountEUR@> 2,
        #       Bilanzgliederungsschlüssel 1,
        #       Bilanzgliederungsschlüssel 2) ]
        coherence_measures = []

        for i in infos:
            for j in infos:
                if i != j:
                    coherence_measures += [(i[0], j[0],
                                            self.measure_coherence(i[-3], j[-3]),
                                            i[-2], j[-2],
                                            i[-1], j[-1])]

        # herausparsen von Dopplungen
        # unter coherence_measures
        for m1 in coherence_measures:
            for m2 in coherence_measures:
                if m1[0] == m2[1] and m1[1] == m2[0]:
                    coherence_measures.remove(m2)

        # Probleme herausfinden
        inc = []
        intg = []
        dup = []

        for m in coherence_measures:
            if 0 < m[2] < 1 and m[3] == m[4] and m[5] != m[6]:
                intg += [[m[0], m[1], m[2]]]
            elif m[2] == 1 and m[3] == m[4] and m[5] == m[6]:
                dup += [[m[0], m[1], m[2]]]
            elif m[2] > 0 and m[3] != m[4] and m[5] != m[6]:
                inc += [[m[0], m[1], m[2]]]

        # Output konfigurieren
        output_messages = []

        for i in intg:
            output_messages += [f'  INTEGRATION         |   Integration zwischen {i[0]} und {i[1]} moeglich  ']
        for i in dup:
            output_messages += [f'  DUPLIKAT            |   {i[0]} und {i[1]} sind Duplikate                 ']
        for i in inc:
            output_messages += [f'  INKONSISTENZ        |   Inkonsistenz zwischen {i[0]} und {i[1]}          ']

        return output_messages

