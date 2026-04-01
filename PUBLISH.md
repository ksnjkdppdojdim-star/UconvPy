# Publication sur PyPI

Ce guide explique comment publier `mahounou-uconv` sur PyPI.

## Prérequis

1. Compte [PyPI](https://pypi.org/account/register/) créé
2. Token PyPI généré dans les [paramètres du compte](https://pypi.org/manage/account/token/)
3. Outils installés:
   ```bash
   pip install build twine
   ```

## Étapes de publication

### 1. Vérifier la version

Assurez-vous que la version dans `setup.py` est correcte:
```python
version="0.2.0",  # Incrémentez selon [semver](https://semver.org/)
```

### 2. Construire le package

```bash
python -m build
```

Cela crée deux fichiers dans `dist/`:
- `mahounou_uconv-0.2.0-py3-none-any.whl` (wheel)
- `mahounou-uconv-0.2.0.tar.gz` (source)

### 3. Vérifier l'intégrité du package

```bash
twine check dist/*
```

### 4. Tester sur PyPI Test (recommandé)

```bash
twine upload --repository testpypi dist/*
```

Quand demandé, utilisez `__token__` comme username et votre token PyPI comme password.

Puis testez:
```bash
pip install --index-url https://test.pypi.org/simple/ mahounou-uconv
```

### 5. Publier sur PyPI

```bash
twine upload dist/*
```

Utilisez `__token__` comme username et votre token comme password.

### 6. Vérifier la publication

Visitez: https://pypi.org/project/mahounou-uconv/

## Utilisation après publication

Les utilisateurs peuvent installer avec:
```bash
pip install mahounou-uconv
```

## Versioning

Respectez [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (ex: 0.2.0)
- MAJOR: changements incompatibles
- MINOR: nouvelles fonctionnalités (rétro-compatibles)
- PATCH: corrections de bugs

### Historique

- **0.2.0**: Phase 1 complète (13 catégories d'unités, 100+ unités)
- **0.1.0**: Version initiale (4 catégories: distance, weight, time, currency)

## État actuel

- [x] i18n (français/anglais)
- [x] CLI Python (mahounou-uconv, uconv-py)
- [x] Unités composées
- [x] Préfixes SI et binaires

## Dépannage

**Erreur: "Invalid distribution"**
```bash
twine check dist/*
```

**Authentification échouée**
- Vérifier le token PyPI
- Utiliser `__token__` comme username

**Package déjà publié**
- Incrémenter la version dans `setup.py`
- Reconstruire avec `python -m build`
