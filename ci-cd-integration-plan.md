# Plan d'Intégration CI/CD pour la Sécurité

---

### Semgrep (Static Application Security Testing - SAST)

**Objectif :** Analyser le code source à chaque `push` et bloquer le pipeline si des failles de sécurité sont trouvées.

**Action GitHub à utiliser :** `semgrep/semgrep-action@v1`

**Snippet de Code YAML à insérer dans le workflow :**
```yaml
- name: 'SECURITY: Scan source code with Semgrep'
  uses: semgrep/semgrep-action@v1
  with:
    # "auto" détecte le langage (Python) et applique les règles de sécurité recommandées.
    config: "auto"