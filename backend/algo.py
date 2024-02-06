class Fahrzeug:
    def __init__(self, modell, antrieb, akkukapazität, verbrauch, ladeleistung):
        self.modell = modell
        self.antrieb = antrieb
        self.akkukapazität = akkukapazität
        self.verbrauch = verbrauch
        self.ladeleistung = ladeleistung
        self.fahrplan = []

    def fahrplan_hinzufügen(self, zeit, ort, aktion, dauer):
        self.fahrplan.append([zeit, ort, aktion, dauer])

    def fahrplan_anzeigen(self):
        print("Fahrplan für", self.modell)
        print("Zeit\tOrt\tAktion\tDauer")
        for eintrag in self.fahrplan:
            print(*eintrag, sep='\t')


# Beispielverwendung:
auto = Fahrzeug("Tesla Model S", "Elektro", 75, 20, 50)
auto.fahrplan_hinzufügen("08:00", "Berlin", "Fahren", "1 Stunde")
auto.fahrplan_hinzufügen("09:00", "Hamburg", "Laden", "30 Minuten")
auto.fahrplan_hinzufügen("09:30", "Hamburg", "Fahren", "2 Stunden")
auto.fahrplan_hinzufügen("11:30", "Bremen", "Fahren", "1 Stunde")
auto.fahrplan_anzeigen()
