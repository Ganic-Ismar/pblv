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
        wertPro5min = wert/1000/12
        self.prognose.append([datum, start, ende, wertPro5min])

    def prognose_anzeigen(self):
        print("Prognose")
        print("Datum\tStart\tEnde\tWert\t")
        for eintrag in self.prognose:
            print(*eintrag, sep='\t')

# Klasse für die Planung
class Planung:
    def __init__(self):
        from datetime import datetime
        self.ladeplan = []

    def ladeplan_hinzufügen(self, zeitpunkt, mengePV, mengeNStrom):
        self.ladeplan.append([zeitpunkt, mengePV, mengeNStrom])

    def ladeplan_anzeigen(self):
        print("Ladeplan")
        print("Datum\tStart\tPVStrom\tNStrom\t")
        for eintrag in self.ladeplan:
            print(*eintrag, sep='\t')
        print("-------------------------")
        
    def erstelle_planung(self, prognose, fahrzeug):  # korrigierter Methodenheader
        from datetime import datetime

        self.ladeplan = []

        pvstrom = 0
        nstrom = 0

        index = 0

        while index < len(fahrzeug.fahrplan):  # Verwendung von fahrzeug.fahrplan, um den leeren Plan zu überprüfen
            for i in fahrzeug.fahrplan:
                if i[4] > 0:
                    # Ankunftsdatum
                    fahrplan_ankunft_d = datetime.strptime(i[0], "%d.%m.%Y")
                    fahrplan_ankunft_t = datetime.strptime(i[1], "%H:%M").time()
                    fahrplan_ankunft_dt = datetime.combine(fahrplan_ankunft_d, fahrplan_ankunft_t)
                    # Abfahrtsdatum
                    fahrplan_abfahrt_d = datetime.strptime(i[2], "%d.%m.%Y")  # Zugriff auf das Datum im Fahrplan
                    fahrplan_abfahrt_t = datetime.strptime(i[3], "%H:%M").time()
                    fahrplan_abfahrt_dt = datetime.combine(fahrplan_abfahrt_d, fahrplan_abfahrt_t)

                    for j in prognose.prognose:
                        # Startdatum
                        prognose_start_d = datetime.strptime(j[0], "%d.%m.%Y")  # Zugriff auf das Datum in der Prognose
                        prognose_start_t = datetime.strptime(j[1], "%H:%M").time()  # Zugriff auf die Zeit in der Prognose
                        prognose_start_dt = datetime.combine(prognose_start_d, prognose_start_t)

                        if prognose_start_dt.replace(minute=0) >= fahrplan_ankunft_dt.replace(minute=0) and prognose_start_dt < fahrplan_abfahrt_dt and i[4] > 0:
                            aktStartZeitLaden = prognose_start_dt

                            maxDauerLadung = i[4] / fahrzeug.ladeleistung

                            zeitBisAbfahrt = fahrplan_abfahrt_dt - prognose_start_dt
                            anzahl_stunden = float(zeitBisAbfahrt.total_seconds() / 3600)

                            durchlaeufe = 12
                            if fahrplan_ankunft_dt.replace(minute=0) == prognose_start_dt.replace(minute=0):
                                durchlaeufe = int((60-fahrplan_ankunft_dt.minute)/5)
                                aktStartZeitLaden = fahrplan_ankunft_dt
                            if fahrplan_abfahrt_dt.replace(minute=0) == prognose_start_dt.replace(minute=0):
                                durchlaeufe = int(fahrplan_abfahrt_dt.minute/5)


                            #5 Minuten Intervalle durchlaufen
                            for x in range(durchlaeufe):
                                
                                if x != 0:
                                    aktStartZeitLaden = aktStartZeitLaden.replace(minute=(aktStartZeitLaden.minute + 5))

                                mengePV = 0
                                mengeNStrom = 0

                                if i[4] > 1/3:
                                    if maxDauerLadung + 1 >= anzahl_stunden:
                                        #Ab hier muss dauerhaft geladen werden

                                        #Zwischen 0 und 1/3 verfügbar
                                        if j[3] <= 1/3:
                                            i[4] -= 1/3

                                            pvstrom += j[3]
                                            mengePV += j[3]
                                            nstrom += 1/3 - j[3]
                                            mengeNStrom += 1/3 - j[3]

                                        #Mehr als möglich zur Verfügung
                                        else:
                                            i[4] -= 1/3

                                            pvstrom += 1/3
                                            mengePV += 1/3
                                    else:
                                        #Hier wird nur geladen, wenn PV Strom verfügbar ist

                                        #Zwischen 0 und 1/3 verfügbar
                                        if j[3] > 0 and j[3] <= 1/3:
                                            i[4] -= j[3]

                                            pvstrom += j[3]
                                            mengePV += j[3]

                                        #Mehr als möglich zur Verfügbar
                                        elif j[3] > 1/3:
                                            i[4] -= 1/3

                                            pvstrom += 1/3
                                            mengePV += 1/3

                                    self.ladeplan_hinzufügen(aktStartZeitLaden, mengePV, mengeNStrom)
                                else:
                                    if j[3] > 0:
                                        if i[4] < j[3]:
                                            # PV Strom vorhanden, aber mehr als benötigt -> nur mit verbleibendem PV Strom laden
                                            pvstrom += i[4]
                                            mengePV += i[4]
                                            j[3] = j[3] - i[4]
                                        elif i[4] > j[3]:
                                            # PV Strom vorhanden, aber weniger als benötigt -> mit PV und Netzstrom laden
                                            pvstrom += j[3]
                                            mengePV += j[3]
                                            nstrom += i[4] - j[3]
                                            mengeNStrom += i[4] - j[3]
                                            j[3] = 0
                                    else:
                                        # Kein PV Strom vorhanden -> mit Netzstrom laden
                                        nstrom += i[4]
                                        mengeNStrom += i[4]

                                    i[4] = 0
                                    self.ladeplan_hinzufügen(aktStartZeitLaden, mengePV, mengeNStrom)
                                    self.ladeplan_anzeigen()
                                    break

                            if i[4] > 0:                           
                                if j[3] <= 1/3:
                                    j[3] = 0
                                else:
                                    j[3] -= 1/3
                index += 1

class Erzeugung:
    def __init__(self):
        self.erzeugung = []

    def erzeugung_hinzufügen(self, datum, zeit, erzeugungInWatt):
        wertInkWh = erzeugungInWatt/1000
        wertInkWhpro5min = wertInkWh/12
        self.erzeugung.append([datum, zeit, erzeugungInWatt, wertInkWh, wertInkWhpro5min])

    def erzeugung_anzeigen(self):
        print("Erzeugung")
        print("Datum\tStart\tEnde\tWert\t")
        for eintrag in self.erzeugung:
            print(*eintrag, sep='\t')


# Main:
# Auto1 anlegen
auto1 = Fahrzeug("BMW i4", "Vollelektrisch", 60, 14.4, 4)
auto1.fahrplan_hinzufügen("01.01.2020", "14:40", "02.01.2020", "06:00", 25)
auto1.fahrplan_hinzufügen("02.01.2020", "12:45", "03.01.2020", "06:10", 21)
auto1.fahrplan_hinzufügen("03.01.2020", "14:00", "04.01.2020", "11:05", 18)
auto1.fahrplan_hinzufügen("04.01.2020", "19:10", "06.01.2020", "17:20", 60)

#Auto2 anlegen
auto2 = Fahrzeug("Tesla Model 3", "Vollelektrisch", 80, 16.3, 4)
auto2.fahrplan_hinzufügen("01.01.2020", "13:00", "02.01.2020", "17:00", 13)
auto2.fahrplan_hinzufügen("02.01.2020", "21:00", "03.01.2020", "14:11", 21)
auto2.fahrplan_hinzufügen("03.01.2020", "15:05", "03.01.2020", "17:00", 5)
auto2.fahrplan_hinzufügen("03.01.2020", "19:10", "04.01.2020", "15:30", 30)
auto2.fahrplan_hinzufügen("04.01.2020", "19:00", "05.01.2020", "17:25", 62)
auto2.fahrplan_hinzufügen("05.01.2020", "21:10", "06.01.2020", "14:35", 12)

#Prognose erzeugen
prognose = Prognose()
prognose.prognose_hinzufügen("01.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "08:00", "08:59", 113.05)
prognose.prognose_hinzufügen("01.01.2020", "09:00", "09:59", 1119.3)
prognose.prognose_hinzufügen("01.01.2020", "10:00", "10:59", 663.6)
prognose.prognose_hinzufügen("01.01.2020", "11:00", "11:59", 1693.02)
prognose.prognose_hinzufügen("01.01.2020", "12:00", "12:59", 691.54)
prognose.prognose_hinzufügen("01.01.2020", "13:00", "13:59", 1392.68)
prognose.prognose_hinzufügen("01.01.2020", "14:00", "14:59", 798.87)
prognose.prognose_hinzufügen("01.01.2020", "15:00", "15:59", 374.9)
prognose.prognose_hinzufügen("01.01.2020", "16:00", "16:59", 22.125)
prognose.prognose_hinzufügen("01.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("01.01.2020", "23:00", "23:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "08:00", "08:59", 23.01)
prognose.prognose_hinzufügen("02.01.2020", "09:00", "09:59", 203.5)
prognose.prognose_hinzufügen("02.01.2020", "10:00", "10:59", 990.6)
prognose.prognose_hinzufügen("02.01.2020", "11:00", "11:59", 1143.83)
prognose.prognose_hinzufügen("02.01.2020", "12:00", "12:59", 781.44)
prognose.prognose_hinzufügen("02.01.2020", "13:00", "13:59", 631.4)
prognose.prognose_hinzufügen("02.01.2020", "14:00", "14:59", 546.12)
prognose.prognose_hinzufügen("02.01.2020", "15:00", "15:59", 109.6046)
prognose.prognose_hinzufügen("02.01.2020", "16:00", "16:59", 366.24)
prognose.prognose_hinzufügen("02.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("02.01.2020", "23:00", "23:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "08:00", "08:59", 128.8)
prognose.prognose_hinzufügen("03.01.2020", "09:00", "09:59", 901.6)
prognose.prognose_hinzufügen("03.01.2020", "10:00", "10:59", 1479.87)
prognose.prognose_hinzufügen("03.01.2020", "11:00", "11:59", 1219.34)
prognose.prognose_hinzufügen("03.01.2020", "12:00", "12:59", 1814.14)
prognose.prognose_hinzufügen("03.01.2020", "13:00", "13:59", 3562.36)
prognose.prognose_hinzufügen("03.01.2020", "14:00", "14:59", 1513.84)
prognose.prognose_hinzufügen("03.01.2020", "15:00", "15:59", 209.56)
prognose.prognose_hinzufügen("03.01.2020", "16:00", "16:59", 31.32)
prognose.prognose_hinzufügen("03.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("03.01.2020", "23:00", "23:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "08:00", "08:59", 47.88)
prognose.prognose_hinzufügen("04.01.2020", "09:00", "09:59", 660.03)
prognose.prognose_hinzufügen("04.01.2020", "10:00", "10:59", 213.12)
prognose.prognose_hinzufügen("04.01.2020", "11:00", "11:59", 163.18)
prognose.prognose_hinzufügen("04.01.2020", "12:00", "12:59", 116.28)
prognose.prognose_hinzufügen("04.01.2020", "13:00", "13:59", 787.36)
prognose.prognose_hinzufügen("04.01.2020", "14:00", "14:59", 323.01)
prognose.prognose_hinzufügen("04.01.2020", "15:00", "15:59", 141.48)
prognose.prognose_hinzufügen("04.01.2020", "16:00", "16:59", 42)
prognose.prognose_hinzufügen("04.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("04.01.2020", "23:00", "23:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "08:00", "08:59", 122.2)
prognose.prognose_hinzufügen("05.01.2020", "09:00", "09:59", 1007.37)
prognose.prognose_hinzufügen("05.01.2020", "10:00", "10:59", 1311.12)
prognose.prognose_hinzufügen("05.01.2020", "11:00", "11:59", 2713.95)
prognose.prognose_hinzufügen("05.01.2020", "12:00", "12:59", 2521.64)
prognose.prognose_hinzufügen("05.01.2020", "13:00", "13:59", 847.09)
prognose.prognose_hinzufügen("05.01.2020", "14:00", "14:59", 409.4)
prognose.prognose_hinzufügen("05.01.2020", "15:00", "15:59", 636.23)
prognose.prognose_hinzufügen("05.01.2020", "16:00", "16:59", 120.6)
prognose.prognose_hinzufügen("05.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("05.01.2020", "23:00", "23:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "00:00", "00:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "01:00", "01:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "02:00", "02:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "03:00", "03:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "04:00", "04:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "05:00", "05:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "06:00", "06:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "07:00", "07:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "08:00", "08:59", 132.08)
prognose.prognose_hinzufügen("06.01.2020", "09:00", "09:59", 1582.08)
prognose.prognose_hinzufügen("06.01.2020", "10:00", "10:59", 1309.5)
prognose.prognose_hinzufügen("06.01.2020", "11:00", "11:59", 2310.75)
prognose.prognose_hinzufügen("06.01.2020", "12:00", "12:59", 2147.95)
prognose.prognose_hinzufügen("06.01.2020", "13:00", "13:59", 997.1)
prognose.prognose_hinzufügen("06.01.2020", "14:00", "14:59", 3029.1)
prognose.prognose_hinzufügen("06.01.2020", "15:00", "15:59", 830.76)
prognose.prognose_hinzufügen("06.01.2020", "16:00", "16:59", 99.4)
prognose.prognose_hinzufügen("06.01.2020", "17:00", "17:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "18:00", "18:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "19:00", "19:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "20:00", "20:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "21:00", "21:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "22:00", "22:59", 0)
prognose.prognose_hinzufügen("06.01.2020", "23:00", "23:59", 0)

#Erzeugungsdaten anlegen
erzeugung = Erzeugung()
erzeugung.erzeugung_hinzufügen
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "02:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "03:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "04:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "05:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "06:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "07:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "08:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "09:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "10:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "11:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "12:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "13:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "14:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "15:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "16:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "17:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "18:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "19:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "20:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "21:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "22:55", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:00", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:05", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:10", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:15", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:20", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:25", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:30", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:35", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:40", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:45", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:50", 0)
erzeugung.erzeugung_hinzufügen("01.01.2020", "23:55", 0)

planung = Planung()
planung.erstelle_planung(prognose, auto1)
planung.erstelle_planung(prognose, auto2)
print("")