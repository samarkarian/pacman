# 🟡 Pac-Man 42 — Avancement (Sacha)

> **Config loader** — ✅ Fait · `make lint` (flake8 + mypy) : **0 erreur**

## Ce qui est fait

- **`pac-man.py`** — lit l'argument `config.json`, ouvre le fichier, gère les erreurs proprement (pas de crash, pas de traceback).
- **`json_loader.py`** — enlève les commentaires `#`, parse le JSON, valide avec **pydantic**.
- Modèles **`Config`** + **`Level`** avec valeurs par défaut.
- **Robustesse** — toute valeur invalide (mauvais type *ou* hors plage) est **clampée** vers son défaut → jamais de rejet, jamais de crash. Conforme **V.2 + V.3**.

## Ce que ça te donne

```python
json_load(content) -> Config
```

Une **`Config`** prête à l'emploi : `lives`, `pacgum`, `points_per_*`, `seed`, `level_max_time`, et `level` (liste de tailles `width`/`height`).

## Ma prochaine étape

Le **maze** (package `mazegenerator`), avec les `width` / `height` / `seed` de la `Config`.
