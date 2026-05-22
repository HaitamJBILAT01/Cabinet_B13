# Cabinet B13 — Portail de Gestion Juridique

Application web Django de gestion de cabinet d'avocats.

## Prérequis

- Python 3.10+
- pip

## Installation

```bash
# 1. Cloner le projet et créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Appliquer les migrations
python manage.py migrate

# 4. Créer un super-utilisateur
python manage.py createsuperuser

# 5. (Optionnel) Générer des données de test
python manage.py fake_data

# 6. Lancer le serveur
python manage.py runserver
```

Accéder à l'application : http://127.0.0.1:8000/

## Structure du projet

```
Cabinet_B13/
├── cabinet_core/          # Configuration Django (settings, urls, wsgi, asgi)
├── comptes/               # Authentification & gestion des utilisateurs
├── dossiers/              # Logique métier (dossiers, clients, audiences, documents)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── mixins.py
│   └── templates/dossiers/
├── templates/             # Templates globaux (base, dashboard)
├── static/                # Fichiers statiques (Bootstrap)
├── media/                 # Fichiers uploadés (générés à l'exécution)
├── manage.py
└── requirements.txt
```

## Applications

| App | Rôle |
|-----|------|
| `comptes` | Modèle utilisateur personnalisé, authentification |
| `dossiers` | Clients, dossiers juridiques, interventions, audiences, documents |

## Base de données

SQLite par défaut. Pour utiliser MySQL, décommenter le bloc dans `cabinet_core/settings.py` et installer `mysqlclient`.
