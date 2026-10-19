# Banking Risk Analytics — Portfolio Jordan Boucetta

Analyse reproductible d'un portefeuille de **8 000 prêts entièrement synthétiques**.

## Question métier
Quels types de crédits présentent les taux d'incident simulés à 90 jours les plus élevés ?

## Contenu
- `pipeline.py` : génération, contrôles, agrégations et visualisation.
- `tests.py` : quatre tests automatisés.
- `data_dictionary.md` : définition des champs.
- `.github/workflows/tests.yml` : exécution automatique des tests et génération des livrables.
- `requirements.txt` : dépendances.

## Exécution locale
```bash
python -m pip install -r requirements.txt
python pipeline.py --size 8000 --seed 42
python -m unittest tests.py -v
```

Le pipeline produit :
- `data/synthetic_loans.csv`
- `reports/risk_by_loan_type.csv`
- `reports/summary.txt`
- `images/risk_by_loan_type.png`

Les résultats générés par GitHub Actions sont téléchargeables dans l'onglet **Actions**, en tant qu'artifact `synthetic-risk-demo`.

## Indicateurs
Nombre de prêts, encours simulé, DTI, score fictif et taux d'incident par type de prêt.

## Limites
**100 % de données fictives.** Aucun dossier client, modèle interne ou donnée d'employeur. Les événements et corrélations sont simulés ; ce projet n'est ni un score réglementaire, ni une estimation de PD/LGD/EAD, ni un outil de décision de crédit.

**Auteur :** Jordan Boucetta — étude de cas de portfolio.
