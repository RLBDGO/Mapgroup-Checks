[logo]: https://www.elkem.com/globalassets/foundry/tech-advice/icon_tech-advice_reproducibility-and-consistency.png

![alt text][logo]

# Mapgroup Checks

Prüft diverse Mapgruppen-Filter auf spezifische Art von Inkonsistenz, Inkompatibilität & Verbesserungsoptionen.


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
        
        
        -----
        
        
          def compare_triple_instances(self, infos):

        # Anzahl der Infos
        n = 3

        # Vergleichsdaten
        data = [(info[0], info[2], info[3]) for info in infos
                if len(info[1]) == n]

        # Vergleichsdaten zurechtstutzen
        for info in data:
            for e in info[1]:
                if '(' in e:
                    info[1].remove(e)

        data = self.remove_duplicates(data)

        # Vergleichstupel bilden & in Vergleichsdaten einbauen
        #Triple = []

        #for i in range(len(data)):
         #   data[i] = list(data[i])

        #for i in range(len(data)):
         #   t_1 = data[i][1][0]
          #  t_2 = data[i][1][1]
           # Triple += [(t_1, t_2, data[i][1][j]) for j in range(len(data[i][1]))
            #          if (t_1 != data[i][1][j]) and (t_2 != data[i][1][j])]

        #for j in range(len(data[i][1])):
            #if (t_1 != data[i][1][j]) and (t_2 != data[i][1][j]):
                #data[i][1] += [(t_1, t_2, data[i][1][j])]




        #for info in data:
         #   l_1 = len(info[1]) - (n-1)
          #  l_2 = len(info[1])
           # for _ in range(l_1):
            #    info[1] += [Triple[0]]
             #   Triple.pop(0)
            #for _ in range(l_2):
             #   info[1].pop(0)
              #  info[1] = self.remove_duplicates((info[1]))

        #for i in range(len(data)):
         #   data[i][1] += [data[i][1][0][0]]
          #  data[i][1] += [data[i][1][0][1]]



        # Verbesserungsoptionen eruieren
        #opt = []

        #inter = lambda x, y: sum([int(i == j) for i in x for j in y])/len(x) == 1
        #for info_1 in data:
         #   for info_2 in data:
          #      if inter(info_1[-2:], info_2[-2:]) and info_1[-1] == info_2[-1] and info_1[1] != info_2[1]:
           #         opt += [(info_1[0], info_2[0])]
            #        for o_1 in opt:
             #           for o_2 in opt:
              #              if o_1[0] == o_2[1] and o_2[0] == o_1[1]:
               #                 opt.remove(o_2)

        # Hinzunahme von Arraylängen der
        # jeweiligen Mapgruppen in opt
        #for i in range(len(opt)):
         #   opt[i] = list(opt[i])
        #for o in opt:
         #   for info in data:
          #      if o[0] == info[0]:
           #         o += [len(info[1])]
            #    if o[1] == info[0]:
             #       o += [len(info[1])]

        # Längen der Werte-Arrays
        #lengths = [len(info[1]) for info in data]

        # Maximale Länge
        #fill_up_to = max(lengths)

        # Namen der zu vergleichenden Instanzen
        #to_compare = [info[0] for info in data]

        # Infos zusammenfassen
        #value_infos = [info[1] for info in data]

        # da wir im Anschluss einen Dataframe nutzen
        # müssen wir beachten, dass alle Infos-arrays
        # gleich lang sein müssen
        # hier werden Infos im Hinblick auf fill_up_to
        # normalisiert
        #for info in value_infos:
         #   while len(info) < fill_up_to:
          #      info += [info[0]]

        # Dataframe/Matrix bauen anhanddessen
        # wir alle Instanzen miteinander
        # vergleichen können
        #df = DataFrame(dict(zip(to_compare, value_infos)))

        # Kohärenzmaß anwenden
        #coherence_measures = [(to_compare_1, to_compare_2, self.measure_coherence(df[to_compare_1], df[to_compare_2]))
         #                     for to_compare_1 in df.columns for to_compare_2 in df.columns
          #                    if to_compare_1 != to_compare_2]

        # herausparsen von Dopplungen
        # unter coherence_measures
        #for m1 in coherence_measures:
         #   for m2 in coherence_measures:
          #      if (m1[0] == m2[1] and m1[1] == m2[0]):
           #         coherence_measures.remove(m2)

        # coherence_measures info
        # opt einbinden
        #for o in opt:
         #   for m in coherence_measures:
          #      if o[0] == m[0] and o[1] == m[1] or o[1] == m[0] and o[0] == m[1]:
           #         o += [m[2]]

        # Schnitt zwischen coherence measures &
        # opt bzgl. Maß > 0 eruieren
        #for m in coherence_measures:
         #   for o in opt:
          #      if m[2] > 0 and ((m[0] == o[0] and m[1] == o[1]) or (m[1] == o[0] and m[0] == o[1])):
           #         coherence_measures.remove(m)

        # Hinzunahme von Arraylängen der
        # jeweiligen Mapgruppen in coherence_measures
        #for i in range(len(coherence_measures)):
         #   coherence_measures[i] = list(coherence_measures[i])
        #for i in range(len(coherence_measures)):
         #   coherence_measures[i] = list(coherence_measures[i])
        #for m in coherence_measures:
         #   for info in data:
          #      if m[0] == info[0]:
           #         m += [len(info[1])]
            #    if m[1] == info[0]:
            #        m += [len(info[1])]

        # Anzahl gleicher Elemente
        # in opt berechnen
        #for o in opt:
         #   if o[-2] <= o[-3]:
          #      o += [o[-2]*o[-1]]
           # else:
            #    o += [o[-3] * o[-1]]

        # Inkonsistenzen herausparsen
        #inc = []
        #for m in coherence_measures:
         #   if m[2] > 0:
          #      inc += [m]

        # Anzahl gleicher Elemente
        # in inc berechnen
        #for i in inc:
         #   if i[-1] <= i[-2]:
          #      i += [i[-1]*i[-3]]
           # else:
            #    i += [i[-2] * i[-3]]

        # Output konfigurieren
        #output_messages = []

        #if len(inc) != 0 or len(opt) != 0:
         #   for i in inc:
          #      try:
           #         output_messages += [f'| Inkonsistenz zwischen {i[0]} und {i[1]}       |   Anzahl gleicher Elemente: {int(i[-1])}   |']
            #    except Exception:
             #       None
            #for o in opt:
             #   try:
              #      output_messages += [f'| Verbesserung zwischen {o[0]} und {o[1]}       |   Anzahl gleicher Elemente: {int(o[-1])}   |']
               # except Exception:
                #    None
        #else:
         #   output_messages = ''

        return data
