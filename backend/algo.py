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

    def ladeplan_hinzufügen(self, datum, start, ladeanweisung):
        self.ladeplan.append([datum, start, ladeanweisung])
        
    def erstelle_planung():
        from datetime import datetime

        while auto1.fahrplan.ladebedarf > 0:
            for i in auto1.fahrplan:
                #Ankunftsdatum
                fahrplan_ankunft_d = datetime.strptime(i.datum_ankunft, "%d.%m.%Y")
                fahrplan_ankunft_t = datetime.strptime(i.zeit_ankunft, "%H:%M") 
                fahrplan_ankunft_dt = datetime.combine(fahrplan_ankunft_d, fahrplan_ankunft_t)
                #Abfahrtsdatum
                fahrplan_abfahrt_d = datetime.strptime(i.datum_abfahrt, "%d.%m.%Y")
                fahrplan_abfahrt_t = datetime.strptime(i.zeit_abfahrt, "%H:%M") 
                fahrplan_abfahrt_dt = datetime.combine(fahrplan_abfahrt_d, fahrplan_abfahrt_t)

                for j in prognose.prognose:
                    #Startdatum
                    prognose_start_d = datetime.strptime(j.datum_ankunft, "%d.%m.%Y")
                    prognose_start_t = datetime.strptime(j.zeit_ankunft, "%H:%M") 
                    prognose_start_dt = datetime.combine(prognose_start_d, prognose_start_t)

                    if prognose_start_dt >= fahrplan_ankunft_dt:
                        #PV Strom verfügbar?
                        if j.wert > 0 and j.wert <= 1/3:
                            j.wert = 0
                            auto1.fahrplan.ladebedarf - 1/3
                        else:
                            j.wert - 1/3
                            auto1.fahrplan.ladebedarf - 1/3






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
prognose.prognose_anzeigen()

