class Fahrzeug:
    def __init__(self, modell, antrieb, akkukapazität, verbrauch, ladeleistung):
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


# Klasse für die Prognose
class Prognose:
    def __init__(self):
        self.prognose = []

    def prognose_hinzufügen(self, datum, start, ende, wert):
        self.prognose.append([datum, start, ende, wert])

    def prognose_anzeigen(self):
        print("Prognose")
        print("Datum\tStart\tEnde\tWert\t")
        for eintrag in self.fahrplan:
            print(*eintrag, sep='\t')


# Main:
# Auto1 anlegen
auto1 = Fahrzeug("BMW i4", "Vollelektrisch", 60, 14.4, 4)
auto1.fahrplan_hinzufügen("01.01.2020", "14:40", "02.01.2020", "06:00", "25")
auto1.fahrplan_hinzufügen("02.01.2020", "12:45", "03.01.2020", "06:10", "21")
auto1.fahrplan_hinzufügen("03.01.2020", "14:00", "04.01.2020", "11:05", "18")
auto1.fahrplan_hinzufügen("04.01.2020", "19:10", "06.01.2020", "17:20", "60")
auto1.fahrplan_anzeigen()

#Auto2 anlegen
auto2 = Fahrzeug("Tesla Model 3", "Vollelektrisch", 80, 16.3, 4)
auto2.fahrplan_hinzufügen("01.01.2020", "13:00", "02.01.2020", "17:00", "13")
auto2.fahrplan_hinzufügen("02.01.2020", "21:00", "03.01.2020", "14:11", "21")
auto2.fahrplan_hinzufügen("03.01.2020", "15:05", "03.01.2020", "17:00", "5")
auto2.fahrplan_hinzufügen("03.01.2020", "19:10", "04.01.2020", "15:30", "30")
auto2.fahrplan_hinzufügen("04.01.2020", "19:00", "05.01.2020", "17:25", "62")
auto2.fahrplan_hinzufügen("05.01.2020", "21:10", "06.01.2020", "14:35", "12")
auto2.fahrplan_anzeigen()

#Prognose erzeugen
prognose = Prognose()
prognose.prognose_hinzufügen
