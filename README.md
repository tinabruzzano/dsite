# DSite

### Il framework web XML-powered per Python

DSite è un framework web moderno scritto in Python che permette di creare siti web usando XML dinamico, Views Python e un potente sistema di Pages.

[Installa](https://raw.githubusercontent.com/DeMENIGECO/dsite-project/main/it/1.0.0/downloader/download_dsite_1.0.0.py) - 
[Documentazione](https://demenigeco.github.io/dsite-project/it/1.0.0/docs/) -
[![PyPI version](https://img.shields.io/pypi/v/dsite.svg)](https://pypi.org/project/dsite/) - [![Python versions](https://img.shields.io/pypi/pyversions/dsite)](https://pypi.org/project/dsite/#details)

---

# 🚀 Perché DSite?

DSite è progettato per essere:

* Semplice
* Moderno
* Potente
* Facile da imparare
* Basato su XML dinamico

Con DSite puoi creare:

* Blog
* Dashboard
* Social network
* Gestionali
* CMS
* Applicazioni web complete

---

# ✨ Features

* 🌍 URL Routing
* 🐍 Views Python
* 📄 DSite Pages XML
* 🧩 Expand System
* 🐍 PythonTag XML
* 📝 Forms
* 🗄️ ORM Database
* 🔄 Migrazioni
* 🛠️ AdminSite
* 🔐 Sistema Token Sicuro
* ⚡ Rendering dinamico

---

# 📄 DSite Pages

DSite utilizza file XML speciali chiamati **DSite Pages**.

Esempio:

```xml
<expand file="diario_di_viaggio:base.xml" />

<html-block>
<h1>Benvenuto in DSite!</h1>

<p>
Questo è il mio primo sito web.
</p>
</html-block>
```

---

# 🧩 Expand System

DSite include un sistema chiamato `<expand />`.

Permette di:

* usare layout condivisi
* creare navbar
* creare footer
* creare temi globali

Esempio:

```xml
<expand file="diario_di_viaggio:base.xml" />
```

---

# 🐍 PythonTag XML

Con DSite puoi eseguire Python dentro XML.

Esempio:

```xml
<pyfunct>
<pycontent>
for i in range(3):
    print(f"<p>Elemento {i}</p>")
</pycontent>
</pyfunct>
```

---

# 🌍 URL Routing

DSite include un sistema di routing semplice e moderno.

Esempio:

```python
from dsite.urls import path
from . import views

urlpatterns = [
    path("/", views.home),
    path("/about", views.about),
]
```

---

# 🐍 Views Python

Le Views gestiscono le pagine del sito.

Esempio:

```python
from dsite.shortcuts import render

def home(request):
    return render(
        request,
        "homepage.xml"
    )
```

---

# 📝 Forms

DSite include un sistema Forms integrato.

Esempio:

```python
from dsite.forms import Form
from dsite.forms import TextField

class TravelForm(Form):
    title = TextField()
```

---

# 🗄️ ORM Database

DSite include un ORM semplice e potente.

Esempio:

```python
from dsite.db import Model
from dsite.db import TextColumn

class Travel(Model):
    title = TextColumn()
```

---

# 🛠️ AdminSite

AdminSite è il pannello amministratore integrato di DSite.

Permette di:

* gestire database
* creare utenti
* modificare dati
* controllare il sito

Esempio:

```python
from dsite.admin import register
from .models import Travel

register(Travel)
```

---

# 🔐 Sicurezza

DSite include sistemi di sicurezza integrati:

* Form Token
* Controlli permessi
* Protezione database
* Limitazioni PythonTag

---

# ❤️ Filosofia

DSite vuole rendere lo sviluppo web:

* divertente
* semplice
* creativo
* accessibile a tutti

---

# 🚀 Stato del progetto

DSite è attualmente in sviluppo.

---

# 📚 Documentazione

La documentazione ufficiale include:

* URL Routing
* Views
* XML Pages
* PythonTag
* Forms
* Models
* Database
* AdminSite

---

# ❤️ Community

Contributi, idee e feedback sono benvenuti!

---

# Attenzione!
DSite è attualmente in fase di sviluppo attivo.

⚠️ Versione 1.0.0 = Alpha Release

Questo framework:
- è funzionante
- è utilizzabile per progetti semplici o educativi
- NON è ancora ottimizzato per produzione

Alcune parti (AdminSite, Migrations, sicurezza avanzata) sono ancora in sviluppo.

---

# 🔥 DSite

### Build websites with Python and XML.
