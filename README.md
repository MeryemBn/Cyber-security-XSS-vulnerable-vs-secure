# xss_project

Mini-projet pour démontrer Stored XSS (version vulnérable) et sa mitigation (version sécurisée).

## Structure
- `vulnerable/` : version vulnérable (port 5000)
- `secure/` : version sécurisée (port 5001)

## Exécution (Linux / macOS)
### Vulnerable
cd vulnerable
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
Ouvrir http://127.0.0.1:5000

### Secure
cd ../secure
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app_secure.py
Ouvrir http://127.0.0.1:5001

(Windows : remplacer activation par `.\venv\Scripts\activate`)

## Démonstration "Break It" (en local)
Dans version vulnérable, poster dans le champ commentaire :
`<script>alert('XSS demo')</script>`
La popup doit apparaître.

Dans version sécurisée, poster le même payload -> il ne doit pas s'exécuter.

## Remarques éthiques
Tester uniquement en environnement local/isolé.
