# 🧭 INF37407 – Application de moissonnage et d’exposition de métadonnées (CanWin)

## 👥 Membres
- **Amadou Bah**
- **Yannick**

---

## 🧩 Description du projet

Ce projet a été développé dans le cadre du cours **INF37407** et consiste à créer une **application Django** capable de :
- Moissonner les **métadonnées** du catalogue **CanWin CKAN**.
- Stocker ces métadonnées dans une base de données **MySQL**.
- Les exposer via :
  - Une **API REST sécurisée** (authentification par token, documentation Swagger).
  - Une **API GraphQL sécurisée par JWT**.

> ⚠️ Le moissonnage a été implémenté uniquement pour le catalogue **CanWin**.

---

## 🏗️ Structure du projet
```
Tech_inforoute/
│
├── manage.py
├── requirements.txt
├── .env
│
├──Api_rest/ # Application principale Django
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── harvesting/ # Moissonnage (CanWin)
│ ├── models.py
│ ├── services/canwin.py
│ ├── management/commands/fetch_data.py
│ └── ...
│
├── api/ # API REST et GraphQL
│ ├── views.py
│ ├── serializers.py
│ ├── schema.py
│ ├── urls.py
│ └── permissions.py
│
└── users/ # Gestion des utilisateurs et authentification
├── views.py
├── serializers.py
├── urls.py
└── permissions.py
```
---

## ⚙️ Installation et configuration

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/Amadou001/Tech_inforoute.git
cd Tech_inforoute
```

## Créer et activer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

## nstaller les dépendances

```bash
pip install -r requirements.txt
```

## Configurer la base de données MySQL
Dans **settings.py**

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "Canwin",
        "USER": "root",
        "PASSWORD": "votre_mot_de_passe",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

## Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

## Moissonner les données CanWin
```bash
python manage.py fetch_data
```

## 🔐 Authentification
Les endpoints REST utilisent l’authentification par Token (**rest_framework.authtoken**).

| Méthode | URL                    | Description                                     |
| ------- | ---------------------- | ----------------------------------------------- |
| `POST`  | `/api/users/register/` | Créer un utilisateur                            |
| `POST`  | `/api/users/login/`    | Authentifier un utilisateur et obtenir un token |
| `POST`  | `/api/users/logout/`   | Supprimer le token (déconnexion)                |
| `POST`  | `/api/users/delete/`   | Supprimer un utilisateur                        |

Après authentification, ajoutez le header suivant à vos requêtes :

```makefile
Authorization: Token <votre_token>
```

# API GraphQL
L’authentification de GraphQL est assurée par **JWT** via le module **django-graphql-jwt**.

🔹 Obtenir un token :

```graphql
mutation {
  tokenAuth(username: "amadou", password: "motdepasse") {
    token
  }
}
```

🔹 Vérifier un token :

```graphql
mutation {
  verifyToken(token: "eyJ0eXAiOiJKV1QiLCJh...") {
    payload
  }
}
```

🔹 Rafraîchir un token :

```graphql
mutation {
  refreshToken(refreshToken: "eyJ0eXAiOiJKV1QiLCJh...") {
    token
  }
}
```

Ensuite, ajoutez ce header dans vos requêtes GraphQL :

```makefile
Authorization: JWT <votre_token>
```

🔹 Exemple de requête sécurisée :

```graphql
{
  allDatasets(search: "ice") {
    id
    title
    organization {
      name
    }
  }
}

```

# 📚 Documentation Swagger

L’interface interactive de la documentation REST est disponible à :
```bash
🌐 http://127.0.0.1:8000/swagger/
```
## 💾 Données moissonnées (CanWin)
Les données proviennent du catalogue CKAN CanWin :

```bash
https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search
```

Les modèles enregistrés sont :

* **Dataset** → Métadonnées principales

* **Organization** → Informations sur l’organisation

* **Ressource** → Liens et fichiers associés

* **Tag** → Mots-clés du jeu de données

# 🧮 Technologies utilisées

| Composant                | Outil                             |
| ------------------------ | --------------------------------- |
| Framework Web            | Django 5.x                        |
| API REST                 | Django REST Framework             |
| Documentation            | Swagger (drf-yasg)                |
| Authentification REST    | Token                             |
| Authentification GraphQL | JWT                               |
| Base de données          | MySQL                             |
| Client HTTP              | Requests                          |
| Catalogue de données     | CanWin CKAN                       |
| Interface utilisateur    | Templates Django (register/login) |


# 🚀 Exécution du projet

```bash
python manage.py runserver

```

Points d’accès :

| Service            | URL                                                              |
| ------------------ | ---------------------------------------------------------------- |
| Swagger UI         | [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) |
| GraphQL Playground | [http://127.0.0.1:8000/graphql/](http://127.0.0.1:8000/graphql/) |

# 🧾 Licence

Projet académique – Université du Québec à Rimouski (UQAR)
**Cours INF37407 – Automne 2025**