# Rapport des Tests de Sécurité Locaux

Ce document contient les preuves de l'exécution réussie de nos outils de sécurité "Shift-Left" sur le code source du projet.

---

## Test 1 : Semgrep (Analyse Statique - SAST)

**Date du test :** [Mettez la date d'aujourd'hui]

**Commande exécutée :**
```powershell
$env:PYTHONUTF8=1; semgrep scan --config auto