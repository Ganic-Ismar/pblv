from .Fahrzeug_class import Fahrzeug
from ...models.Chargingplan import Chargingplan, add_item, setCarId
from ...models.ChargingplanItem import ChargingplanItem, chargingplanItemAddValues

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
        
    def erstelle_planung(self, prognose, fahrzeug) ->Chargingplan:  # korrigierter Methodenheader
        from datetime import datetime

        chargingplan = Chargingplan()
        setCarId(chargingplan,fahrzeug.id)
        pvstrom = 0
        nstrom = 0

        index = 0

        while index < len(fahrzeug.fahrplan):  # Verwendung von fahrzeug.fahrplan, um den leeren Plan zu überprüfen
            for i in fahrzeug.fahrplan:
                if i[4] > 0:
                    # Ankunftsdatum
                    # Formatier

                    fahrplan_ankunft_d = i[0]  # Zugriff auf das Datum im Fahrplan
                    fahrplan_ankunft_t = i[1]
                    fahrplan_ankunft_dt = datetime.combine(fahrplan_ankunft_d, fahrplan_ankunft_t)
                    # Abfahrtsdatum
                    fahrplan_abfahrt_d = i[2]  # Zugriff auf das Datum im Fahrplan
                    fahrplan_abfahrt_t = i[3]
                    fahrplan_abfahrt_dt = datetime.combine(fahrplan_abfahrt_d, fahrplan_abfahrt_t)

                    viertel_kapazitaet = i[4] - (i[4] / 4)

                    for j in prognose.prognose:
                        # Startdatum
                        prognose_start_d = j[0]  # Zugriff auf das Datum in der Prognose
                        prognose_start_t = j[1]  # Zugriff auf die Zeit in der Prognose
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
                                    if maxDauerLadung + 1 >= anzahl_stunden or i[4] >= viertel_kapazitaet :
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
                                    item = ChargingplanItem()
                                    chargingplanItemAddValues(item, aktStartZeitLaden, mengePV, mengeNStrom)
                                    add_item(chargingplan, item)
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
                                    item = ChargingplanItem()
                                    chargingplanItemAddValues(item, aktStartZeitLaden, mengePV, mengeNStrom)
                                    add_item(chargingplan, item)
                                    #self.ladeplan_anzeigen()
                                    break

                            if i[4] > 0:                           
                                if j[3] <= 1/3:
                                    j[3] = 0
                                else:
                                    j[3] -= 1/3
                index += 1
        return chargingplan