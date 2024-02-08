class Fahrzeug:
    def __init__(self, id, modell, antrieb, akkukapazität, verbrauch, ladeleistung):
        self.id = id
        self.modell = modell
        self.antrieb = antrieb
        self.akkukapazität = akkukapazität
        self.verbrauch = verbrauch
        self.ladeleistung = ladeleistung
        self.fahrplan = []

    def fahrplan_hinzufügen(self, datum_ankunft, zeit_ankunft, datum_abfahrt, zeit_abfahrt, ladebedarf):
        self.fahrplan.append([datum_ankunft, zeit_ankunft, datum_abfahrt, zeit_abfahrt, ladebedarf])

    def fahrplan_anzeigen(self):
        print("Fahrplan für", self.modell)
        print("Datum Ankunft\tZeit Ankunft\tDatum Abfahrt\tZeit Abfahrt\tLadebedarf")
        for eintrag in self.fahrplan:
            print(*eintrag, sep='\t')