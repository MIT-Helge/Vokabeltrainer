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

@app.route('/losung', methods=['POST'])
def losung():
    print(request.form)
    if request.method == 'POST':
        vokabeltest = []
        vokabelheft = loadFile(request.form.get('file'))
        for antwort in request.form:
            if antwort != 'file':
                eintrag = {'wort': antwort, 'deins': request.form.get(antwort), 'losung': vokabelheft[antwort],
                           'ergebniss': "Falsch"}
                if request.form.get(antwort) == vokabelheft[antwort]:
                    print('Richtig')
                    eintrag['ergebniss'] = "Richtig"
                else:
                    print('Falsch')
                    eintrag['ergebniss'] = "Falsch"
                vokabeltest.append(eintrag)
        print(vokabeltest)
        return render_template('losungsansicht.html', vokabeltest=vokabeltest)

    return

if __name__ == '__main__':
    app.run()
