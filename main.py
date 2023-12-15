import os
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)


def notenberechnungMSA(prozent):
    if prozent >= 95:
        return 1
    elif prozent >= 85:
        return 2
    elif prozent >= 68:
        return 3
    elif prozent >= 50:
        return 4
    elif prozent >= 24:
        return 5
    else:
        return 6


def notenberechnungESA(prozent):
    if prozent >= 96:
        return 1
    elif prozent >= 79:
        return 2
    elif prozent >= 59:
        return 3
    elif prozent >= 40:
        return 4
    elif prozent >= 20:
        return 5
    else:
        return 6


def notenberechnungAHR(prozent):
    if prozent >= 92:
        return 1
    elif prozent >= 81:
        return 2
    elif prozent >= 67:
        return 3
    elif prozent >= 50:
        return 4
    elif prozent >= 30:
        return 5
    else:
        return 6


def loadFile(test):
    vokabelheft = {}
    # Lade Datei test ein als Vokabel;lösung
    with open(test, 'r') as f:
        # pro zeile eine vokabel
        for line in f:
            # trenne vokabel und lösung
            vokabel, losung = line.split(';')
            vokabelheft[vokabel] = losung.strip()
    print(vokabelheft)
    return vokabelheft


@app.route('/<test>')
def test(test):
    vokabelheft = loadFile(test)
    return render_template('index.html', vokabeltest=vokabelheft.keys(), file=test, schroeder="blau")


@app.route('/')
def testt():
    return render_template('Helge.html')


@app.route('/losung', methods=['POST'])
def losung():
    print(request.form)
    if request.method == 'POST':
        AnzahlderVokabeln = len(request.form) - 4
        AnzahlderFehler = 0
        vokabeltest = []
        vokabelheft = loadFile(request.form.get('file'))
        for antwort in request.form:
            if antwort != 'file' and antwort != "prognose" and antwort != "name" and antwort != "klasse":
                eintrag = {'wort': antwort, 'deins': request.form.get(antwort), 'losung': vokabelheft[antwort],
                           'ergebnis': "Falsch"}
                if request.form.get(antwort) == vokabelheft[antwort]:
                    print('Richtig')
                    eintrag['ergebnis'] = "Richtig"
                else:
                    print('Falsch')
                    eintrag['ergebnis'] = "Falsch"
                    AnzahlderFehler = AnzahlderFehler + 1
                vokabeltest.append(eintrag)
        print(AnzahlderFehler)
        print(AnzahlderVokabeln)
        prognose = request.form.get('prognose')
        note = 6
        prozentrichtig = ((AnzahlderVokabeln - AnzahlderFehler) / AnzahlderVokabeln) * 100
        if prognose == "MSA":
            note = notenberechnungMSA(prozentrichtig)
        elif prognose == "ESA":
            note = notenberechnungESA(prozentrichtig)
        elif prognose == "AHR":
            note = notenberechnungAHR(prozentrichtig)
        # Datum_Tag_Klasse_Schüler_Test
        AktuellesDatum = datetime.now().strftime("%Y_%m_%d")
        voller_pfad = os.path.join(os.getcwd(), AktuellesDatum)
        # if not os.path.exists(voller_pfad):
        # os.makedirs(voller_pfad)
        Dateiname = request.form.get("klasse") + " " + request.form.get("name") + " " + request.form.get("file")
        print(Dateiname)
        Webseite=render_template('losungsansicht.html', vokabeltest=vokabeltest,
                               Prozentzahl=prozentrichtig,
                               Note=note, prognose=prognose)
        print(Webseite)
        return Webseite
    return


if __name__ == '__main__':
    app.run()
