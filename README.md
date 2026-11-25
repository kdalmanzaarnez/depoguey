# PixelDepot WMS

Warehouse Management System voor PixelDepot, een fictieve verkoper van gamingaccessoires. Gemaakt door team DepoGuey: Daniel, Mahi en Kien.

Het projectplan staat in [docs/projectplan/projectplan.md](docs/projectplan/projectplan.md).

## Stack

| Onderdeel | Keuze |
| --- | --- |
| Backend | Python 3.13, Django 5.2, Django REST Framework |
| Database | MySQL 8.4 via Docker |
| Frontend | React + TypeScript + Vite, Chakra UI (volgt) |

## Vereisten

- Docker Desktop
- Python 3.13
- Op macOS: Homebrew met `mysql-client` (voor `mysqlclient`)

## Opstarten

Alle commando's vanuit de root van de repo.

### 1. `.env` aanmaken

```bash
cp .env.example .env
```

Vul in `.env` eigen waarden in voor `DB_PASSWORD`, `DB_ROOT_PASSWORD` en `DJANGO_SECRET_KEY`. `.env` gaat niet mee naar GitHub.

Een secret key maken (na stap 3):

```bash
backend/.venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Database starten

```bash
docker compose up -d
```

Controleren of de database klaar is (status `healthy`):

```bash
docker compose ps
```

### 3. Python-omgeving en pakketten

```bash
python3 -m venv backend/.venv
```

Op macOS met Homebrew:

```bash
MYSQLCLIENT_CFLAGS="$(mysql_config --cflags)" MYSQLCLIENT_LDFLAGS="$(mysql_config --libs) -L/opt/homebrew/lib -L/opt/homebrew/opt/openssl@3/lib" backend/.venv/bin/pip install -r backend/requirements.txt
```

Op Linux:

```bash
backend/.venv/bin/pip install -r backend/requirements.txt
```

Op Windows gebruik je `backend\.venv\Scripts\` in plaats van `backend/.venv/bin/`, ook bij de commando's hieronder:

```bash
backend\.venv\Scripts\pip install -r backend/requirements.txt
```

### 4. Migraties en server

```bash
backend/.venv/bin/python backend/manage.py migrate
```

```bash
backend/.venv/bin/python backend/manage.py runserver
```

De backend draait op http://127.0.0.1:8000.

### 5. Demogebruikers

Zet `DEMO_PASSWORD` in `.env` en draai:

```bash
backend/.venv/bin/python backend/manage.py seed_demo
```

| Gebruiker | Rol |
| --- | --- |
| `medewerker` | Medewerker |
| `admin` | Admin |

Beide loggen in met het wachtwoord uit `DEMO_PASSWORD`. Het commando mag vaker gedraaid worden; het zet de demogebruikers terug naar hun beginstand.

## Tests

```bash
backend/.venv/bin/python backend/manage.py test
```

Django maakt hiervoor een aparte database `test_pixeldepot_wms`. Het script in `docker/mysql-init/` geeft de databasegebruiker daar rechten op, maar alleen bij een nieuwe, lege database. Bestond je database al voordat dit script er was, draai het dan één keer handmatig:

```bash
docker exec pixeldepot-db bash /docker-entrypoint-initdb.d/01-test-database.sh
```

## Mappen

| Map | Inhoud |
| --- | --- |
| `backend/` | Django-project (`config/`) |
| `frontend/` | React-app |
| `docs/` | Projectplan, design, diagrammen, Scrum-verslagen |
| `docker/` | Init-scripts voor de MySQL-container |

## Werkwijze met Git

- `main` is de stabiele versie. Hier pusht niemand rechtstreeks naartoe.
- `dev` is de branch waar we naartoe mergen.
- Iedereen werkt op een eigen branch vanaf `dev`, bijvoorbeeld `feature/us-01-login`.
- Een branch komt via een pull request in `dev`, na review door een ander teamlid.
