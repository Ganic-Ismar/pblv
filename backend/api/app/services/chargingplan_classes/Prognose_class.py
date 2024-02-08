class Prognose:
    def __init__(self):
        self.prognose = []

    def prognose_hinzufügen(self, datum, start, ende, wert):
        wertPro5min = wert/1000/12
        self.prognose.append([datum, start, ende, wertPro5min])

    def prognose_anzeigen(self):
        print("Prognose")
        print("Datum\tStart\tEnde\tWert\t")
        for eintrag in self.prognose:
            print(*eintrag, sep='\t')