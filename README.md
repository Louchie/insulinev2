Emeraude CHO LIN WING
Lucie YU

--------------------TP3--------------------
Pour lancer le serveur : uvicorn src.api:app --reload
Utilisation de Postman -> requêtes dans le PDF envoyé

--------------------TP1--------------------
Lancer les tests : 

Créez un environnement virtuel :
python -m venv env
Activez l'environnement virtuel :
Sur Windows : env\Scripts\activate
Sur macOS et Linux : source env/bin/activate

Installer: pip install coverage
coverage run -m pytest
coverage report
