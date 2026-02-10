# Activation de GitHub Pages pour le déploiement des rapports de couverture

## Problème
Le workflow CI/CD inclut un job `deploy-coverage` qui tente de déployer le rapport de couverture HTML sur GitHub Pages. Cependant, GitHub Pages n'est pas encore activé pour ce dépôt, ce qui cause l'erreur :

```
Error: Get Pages site failed. Please verify that the repository has Pages enabled and configured to build using GitHub Actions
```

## Solution

### Option 1 : Activer GitHub Pages manuellement (recommandé)
1. Accédez à la page des paramètres du dépôt :
   - https://github.com/Kisai-DG-SLU/label_image/settings/pages

2. Dans la section "Build and deployment" :
   - Source : Sélectionnez "GitHub Actions"
   - Cliquez sur "Save"

3. Vérifiez que GitHub Pages est activé :
   - La page devrait afficher "Your site is ready to be published at https://kisai-dg-slu.github.io/label_image/"
   - Le workflow `deploy-coverage` pourra alors fonctionner

### Option 2 : Désactiver temporairement le job (solution temporaire)
Si vous ne souhaitez pas activer GitHub Pages immédiatement, vous pouvez désactiver le job en modifiant `.github/workflows/ci.yml` :

```yaml
deploy-coverage:
  name: Deploy Coverage Report to GitHub Pages
  runs-on: ubuntu-22.04
  needs: test
  if: false  # Désactivé jusqu'à activation de GitHub Pages
  # ... reste du job
```

Et mettre à jour le job `ci` pour ne plus dépendre de `deploy-coverage` :
```yaml
ci:
  name: CI Status
  runs-on: ubuntu-22.04
  needs: [test, build, notebook-test]  # Retirer deploy-coverage
  # ... reste du job
```

## Avantages de l'activation
- **Rapports de couverture accessibles** : Les rapports HTML seront publiés sur https://kisai-dg-slu.github.io/label_image/
- **Visibilité** : Les métriques de couverture seront accessibles publiquement
- **Intégration complète** : Le pipeline CI/CD sera entièrement fonctionnel

## Étapes après activation
1. Une fois GitHub Pages activé, le workflow se déclenchera automatiquement au prochain push
2. Le rapport de couverture sera disponible à l'adresse : https://kisai-dg-slu.github.io/label_image/
3. Vous pourrez consulter les rapports détaillés par fichier et par ligne

## Vérification
Pour vérifier que GitHub Pages est activé :
```bash
# Vérifier le statut via l'API GitHub (si vous avez un token)
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/Kisai-DG-SLU/label_image/pages
```

## Notes
- Le job `deploy-coverage` ne s'exécute que sur la branche `main`
- Il dépend du job `test` qui génère l'artefact `coverage-report`
- L'activation de GitHub Pages est gratuite pour les dépôts publics