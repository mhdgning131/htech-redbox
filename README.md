# Htech RedBox (Prototype)

Plateforme CTF crypto modulaire (prototype). Contenu en français — conçu pour l'apprentissage.

Installation rapide (PowerShell) :

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
$env:FLASK_APP = 'app.py'; flask run --host=0.0.0.0
```

Structure des challenges (modulaire) :
- Créez un dossier sous `challenges/` (par exemple `challenges/mon_challenge`).
- Ajoutez un fichier `meta.json` avec ce format minimal :

```json
{
  "id": "mon_challenge",
  "title": "Titre du challenge",
  "difficulty": "Facile",
  "points": 50,
  "description": "Description en français (HTML autorisé).",
  "flag": "HTECH{exemple_flag}"
}
```

Placez ensuite les fichiers du challenge dans le même dossier (énoncés, binaires, images...). La plateforme listera automatiquement les challenges.

Sécurité / production : ceci est un prototype pédagogique. Ne mettez pas de flags en clair en production ; utilisez un stockage sécurisé et vérifiez les soumissions côté serveur avec hachages/ACL.

Prochaines améliorations possibles :
- Authentification / comptes utilisateurs
- Base de données pour garder score et validations
- Console d'administration pour ajouter/modifier challenges
- Téléchargements et quotas
