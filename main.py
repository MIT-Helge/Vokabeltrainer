from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('index.html', vokabeltest=vokabelheft.keys(), file=test)

@app.route('/')
def testt():
    return render_template('Helge.html')

@app.route('/losung', methods=['POST'])
def losung():
    print(request.form)
    if request.method == 'POST':
        AnzahlderVokabeln= len(request.form)-1
        AnzahlderFehler= 0
        vokabeltest = []
        vokabelheft = loadFile(request.form.get('file'))
        for antwort in request.form:
            if antwort != 'file':
                eintrag = {'wort': antwort, 'deins': request.form.get(antwort), 'losung': vokabelheft[antwort],
                           'ergebnis': "Falsch"}
                if request.form.get(antwort) == vokabelheft[antwort]:
                    print('Richtig')
                    eintrag['ergebnis'] = "Richtig"
                else:
                    print('Falsch')
                    eintrag['ergebnis'] = "Falsch"
                    AnzahlderFehler=AnzahlderFehler+1
                vokabeltest.append(eintrag)
        print(AnzahlderFehler)
        print(AnzahlderVokabeln)
        return render_template('losungsansicht.html', vokabeltest=vokabeltest, Prozentzahl=(AnzahlderFehler/100*AnzahlderVokabeln))

    return

if __name__ == '__main__':
    app.run()
