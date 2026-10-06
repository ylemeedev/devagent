# Programme DevAgent — 12 semaines

## 🟢 SEMAINE 1 — Python fondamentaux

### Jour 1 — Bases Python

* Variables
* Types :

  * `str`
  * `int`
  * `float`
  * `bool`
  * `None`
* `print()`
* `input()`
* conversions de types
* opérateurs
* conditions `if / elif / else`
* opérateurs `and / or / not`
* boucles `for`
* boucles `while`
* `range()`

### Jour 2 — Collections

* listes `list`
* tuples `tuple`
* dictionnaires `dict`
* ensembles `set`
* accès aux éléments
* modification
* ajout/suppression
* parcours des collections
* méthodes courantes
* compréhensions de listes
* compréhensions de dictionnaires
* `enumerate()`
* `zip()`

### Jour 3 — Fonctions

* création d'une fonction
* paramètres
* valeur de retour
* annotations de type
* paramètres optionnels
* valeurs par défaut
* `*args`
* `**kwargs`
* portée des variables
* fonctions comme objets

### Jour 4 — Modules et environnement Python

* `import`
* `from ... import`
* organisation en modules
* `__init__.py`
* environnement virtuel `.venv`
* activation de l'environnement
* `pip`
* installation de packages
* `pyproject.toml`
* installation du projet avec :

```bash
python -m pip install -e .
```

* exécution avec :

```bash
python -m devagent.main
```

### Jour 5 — Python pratique

* exceptions
* `try / except`
* `else`
* `finally`
* `raise`
* lecture de fichiers
* écriture de fichiers
* JSON
* `json.loads()`
* `json.dumps()`
* configuration
* variables d'environnement
* premiers éléments de DevAgent

---

# 🟢 SEMAINE 2 — Python professionnel

## Jour 1 — Typage avancé

Nous avons vu :

* annotations de types
* `list[str]`
* `dict[str, int]`
* `Optional`
* `Union`
* `|`
* `TypeVar`
* `Generic`
* `Protocol`

Et surtout l'idée de :

```python
Tool
```

comme contrat commun pour nos outils.

---

## Jour 2 — `Protocol`, génériques et architecture Tool

Nous avons construit le concept :

```python
class Tool(Protocol[T]):
    ...
```

Puis :

* `TypeVar`
* génériques
* `Protocol`
* contrat d'une Tool
* `ToolResult`
* `Agent`
* registre des Tools
* `tool.name`
* `input_model`
* `execute()`

Architecture :

```text
Agent
  ↓
Tool
  ↓
ToolResult
```

---

## Jour 3 — Dataclasses + Pydantic

### Dataclasses

* `@dataclass`
* attributs
* constructeur automatique
* objets de données
* méthodes de classe
* `classmethod`

Nous avons notamment utilisé :

```python
@dataclass
class ToolResult:
    success: bool
    content: str
```

avec :

```python
ToolResult.ok(...)
ToolResult.error(...)
```

### Pydantic

Nous avons ensuite vu :

* `BaseModel`
* validation
* conversion de types
* `ValidationError`
* `Field`
* valeurs par défaut
* champs optionnels
* `model_validate()`
* `model_dump()`
* `model_dump_json()`
* `model_json_schema()`

Et surtout l'utilisation de Pydantic pour définir le **contrat d'entrée d'une Tool**.

Exemple :

```python
class DivideInput(BaseModel):
    a: int
    b: int
```

Puis validation personnalisée avec :

```python
@field_validator("b")
@classmethod
def b_must_not_be_zero(...):
    ...
```

---

# 🟢 SEMAINE 2 — Jour 4 : HTTP / REST / Async

### HTTP

* client / serveur
* requête / réponse
* GET
* POST
* PUT
* PATCH
* DELETE
* status codes
* `200`
* `201`
* erreurs HTTP
* headers
* body
* paramètres
* JSON

### REST

* ressources
* URL
* paramètres de chemin
* query parameters
* méthodes HTTP

### Python HTTP

* `requests`
* `httpx`
* `response.status_code`
* `response.text`
* `response.json()`
* `params`
* `headers`
* `json`

### Async

* `async def`
* coroutine
* `await`
* `asyncio.run()`
* `asyncio.gather()`
* opérations concurrentes
* opérations séquentielles
* I/O
* timeout

### HTTPX asynchrone

```python
async with httpx.AsyncClient() as client:
```

Puis :

```python
response = await client.get(...)
```

### Gestion des erreurs

* `httpx.TimeoutException`
* `httpx.RequestError`
* validation de la réponse
* `ToolResult.error()`

### API de test

Nous avons utilisé **JSONPlaceholder** pour simuler une API externe.

---

# 🟢 SEMAINE 2 — Jour 4 : intégration dans DevAgent

Nous avons transformé les Tools en outils asynchrones :

```python
async def execute(...)
```

Puis l'Agent :

```python
async def run_tool(...)
```

et :

```python
return await tool.execute(input)
```

Nous avons également utilisé :

```python
asyncio.gather(...)
```

pour exécuter plusieurs Tools indépendants.

Architecture actuelle :

```text
                    Agent
                      │
                      ▼
                Pydantic Input
                      │
                      ▼
                    Tool
                      │
             ┌────────┴────────┐
             ▼                 ▼
          traitement          HTTP
                               │
                               ▼
                          API externe
                               │
                               ▼
                          ToolResult
```

---

# 🟢 SEMAINE 2 — Jour 5

## Logging

Nous avons vu :

* `logging`
* `logger`
* `logging.getLogger(__name__)`
* `DEBUG`
* `INFO`
* `WARNING`
* `ERROR`
* `CRITICAL`
* différence entre `print()` et logging

Exemple :

```python
logger = logging.getLogger(__name__)

logger.info("...")
logger.error("...")
```

---

## Configuration

Nous avons vu :

* `os.getenv()`
* variables d'environnement
* `.env`
* `python-dotenv`
* séparation configuration / code
* `config.py`
* `.gitignore`
* protection des secrets

Architecture :

```text
.env
 ↓
config.py
 ↓
DevAgent
```

### Règle importante

Une clé secrète ne doit jamais être mise en fallback dans `config.py`.

---

# 🟡 Pytest — en cours

Nous avons déjà vu :

### Premier test

```python
def test_tool_result_ok():
    result = ToolResult.ok("Bonjour")

    assert result.success is True
    assert result.content == "Bonjour"
```

### `assert`

* vérifier une valeur
* vérifier un booléen
* vérifier un résultat attendu

### Tests d'erreurs

```python
with pytest.raises(ValidationError):
    ...
```

### Tests async

Installation :

```bash
pip install pytest pytest-asyncio
```

Puis :

```python
@pytest.mark.asyncio
async def test_upper_tool():
    ...
```

### Tests déjà réalisés

* `ToolResult.ok()`
* `ToolResult.error()`
* `UpperTool`
* validation `UpperInput`
* validation `DivideInput`

---

# 🟡 Ce qu'il reste à terminer dans la Semaine 2

## Tests de `Agent`

Tester :

* Tool existante
* Tool inconnue
* données valides
* données invalides
* `ToolResult.error()`

## Organisation professionnelle

```text
devagent/
├── src/
│   └── devagent/
│       ├── __init__.py
│       ├── main.py
│       ├── agent.py
│       ├── tool.py
│       └── config.py
│
├── tests/
│   └── test_tool.py
│
├── .env
├── .gitignore
└── pyproject.toml
```

**Semaine 2 terminée.** ✅

---

# 🔵 SEMAINE 3 — Python avancé

### Jour 1

* classes avancées
* attributs
* méthodes
* `self`
* `cls`
* `__new__`
* `classmethod`
* `staticmethod`

### Jour 2

* composition
* héritage
* `super()`
* polymorphisme

### Jour 3

* exceptions avancées
* exceptions personnalisées
* hiérarchie d'exceptions
* bonnes pratiques

### Jour 4

* décorateurs
* fonctions comme objets
* closures

### Jour 5

* context managers
* `with`
* `__enter__`
* `__exit__`
* générateurs
* itérateurs
* `yield`

---

# 🔵 SEMAINE 4 — Architecture DevAgent

C'est là que le projet va vraiment commencer à prendre une forme professionnelle.

* Domain
* Application
* Infrastructure
* séparation des responsabilités
* `Tool`
* `ToolResult`
* `Protocol`
* génériques
* registry
* découverte dynamique des Tools
* métadonnées
* schemas
* exécution dynamique
* gestion des erreurs
* refactoring
* tests

Architecture visée :

```text
src/devagent/
│
├── domain/
├── application/
└── infrastructure/
```

---

# 🔵 SEMAINE 5 — LLM

* fonctionnement d'un LLM
* tokens
* contexte
* messages
* system / user / assistant
* API LLM
* première requête LLM
* structured output
* réponses structurées
* intégration du LLM dans DevAgent

---

# 🔵 SEMAINE 6 — Tool Calling

C'est une étape **très importante pour ton objectif AI Agent**.

On passera de :

```text
Agent → Tool
```

à :

```text
LLM
 ↓
choisit une Tool
 ↓
génère les arguments
 ↓
Pydantic valide
 ↓
Tool exécutée
 ↓
résultat
 ↓
LLM
```

On verra :

* function calling
* JSON Schema
* arguments générés par le LLM
* validation Pydantic
* exécution
* retour du résultat au LLM
* boucle LLM ↔ Tools

---

# 🔵 SEMAINE 7 — Developer Tools

On donnera de vraies capacités de développeur à DevAgent :

* `read_file`
* `write_file`
* `list_files`
* `search_code`
* `run_command`
* `run_tests`

Et :

* filesystem
* subprocess
* stdout
* stderr
* sécurité
* permissions
* commandes dangereuses

---

# 🔵 SEMAINE 8 — Boucle Agent

On construira le véritable mécanisme d'Agent :

```text
Plan
 ↓
Action
 ↓
Observation
 ↓
Plan
 ↓
Action
 ↓
Observation
...
```

Avec :

* état
* contexte
* historique
* nombre maximal d'itérations
* conditions d'arrêt
* erreurs
* prévention des boucles infinies

---

# 🔵 SEMAINE 9 — Developer Agent

DevAgent commencera réellement à agir comme un assistant développeur :

* analyser un projet
* comprendre le code
* rechercher du code
* modifier des fichiers
* lancer les tests
* analyser les erreurs
* corriger le code
* vérifier les corrections

---

# 🔵 SEMAINE 10 — Agent avancé

* mémoire court terme
* historique
* contexte
* planning
* sous-tâches
* plusieurs Tools
* parallélisme
* async dans l'Agent
* orchestration

---

# 🔵 SEMAINE 11 — Architecture professionnelle

* Domain
* Application
* Infrastructure
* interfaces
* Dependency Injection
* configuration
* logging
* tests unitaires
* tests d'intégration
* sécurité
* gestion des erreurs

---

# 🔵 SEMAINE 12 — DevAgent final

On consolide tout :

```text
LLM
 ↓
Agent
 ↓
Planning
 ↓
Tool Calling
 ↓
Tools
 ↓
Filesystem / Terminal / Tests
 ↓
Observation
 ↓
LLM
```

Puis :

* documentation
* configuration
* logs
* tests
* sécurité
* packaging
* Git
* démonstration finale

---

# 🎯 Redémarrage — DevAgent depuis zéro

Ne pas simplement relire cette liste.

Refaire réellement le projet depuis zéro, dans un nouveau dossier par exemple :

```text
devagent-practice/
```

Et avancer dans cet ordre :

```text
Python bases
     ↓
typing
     ↓
Protocol
     ↓
ToolResult
     ↓
Pydantic
     ↓
Agent
     ↓
Tools
     ↓
HTTP
     ↓
async
     ↓
logging
     ↓
config
     ↓
pytest
```

## Méthode de travail

Quand un concept est rencontré :

1. Comprendre le concept.
2. Faire un petit exercice isolé.
3. L'intégrer dans `devagent-practice`.
4. Tester.
5. Revenir dessus plus tard pour vérifier qu'il est maîtrisé.

**L'objectif n'est pas de recopier le projet actuel, mais de reconstruire DevAgent progressivement en comprenant chaque élément.**
