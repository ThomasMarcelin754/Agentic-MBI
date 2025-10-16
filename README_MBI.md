# Dexter MBI - Agent de Due Diligence pour Rollup 🤖

Agent autonome spécialisé dans l'analyse financière et la due diligence de PME françaises pour stratégie de rollup/MBI.

## Vue d'Ensemble

Dexter MBI analyse automatiquement des cibles d'acquisition en :
- **Normalisant l'EBITDA** avec retraitements adaptés au système comptable
- **Scorant les 4 piliers opérationnels** (répétitivité, récurrence, digitalisation, diversification)
- **Détectant les red flags** et deal-breakers
- **Valorisant** avec multiples sectoriels
- **Recommandant** GO/MAYBE/NO-GO avec validation humaine

## Architecture Multi-Modèles

**Claude Sonnet 4.5** (tâches complexes) :
- Analyse financière & retraitements EBITDA
- Scoring des 4 piliers
- Détection de red flags
- Valorisation

**Claude Haiku** (tâches rapides) :
- Extraction de données depuis IMs (PDF)
- Pre-filtering de listes de cibles

## Mapping Systématique

L'agent mappe chaque analyse sur 3 dimensions :

### 1. Système Comptable
- **French GAAP** : EBE, provisions réglementées, crédit-bail hors bilan
- **US GAAP** : Operating Income + D&A, stock-based comp
- **IFRS** : Operating Income + D&A, IFRS 16 leases

### 2. Secteur (avec multiples spécifiques)
Exemples de multiples EV/EBITDA :
- CVC : 6-8-10x (services récurrents)
- Sécurité Incendie : 7-9-11x (réglementation forte)
- IRVE : 8-11-14x (croissance forte)
- Gestion Locative : 8-10-12x (revenus très récurrents)
- Élagage : 4.5-6.5-8.5x (saisonnalité)

### 3. Géographie (impact coûts)
Index de coûts vs baseline :
- Paris : +30%
- Lyon : +10%
- Nice : +15%
- Lille : baseline

## Installation

```bash
# Clone du repo
git clone https://github.com/virattt/dexter.git
cd dexter

# Installation avec uv
uv sync

# Variables d'environnement
cp env.example .env
# Ajouter : ANTHROPIC_API_KEY=your-key
```

## Configuration `.env`

```bash
ANTHROPIC_API_KEY=sk-ant-...
FINANCIAL_DATASETS_API_KEY=your-key  # Optionnel pour comparables US
```

## Utilisation

### Mode CLI Interactif

```bash
uv run dexter-agent
```

### Mode Programmatique

```python
from dexter.agent import Agent
from dexter.schemas import TargetCompany, FinancialMetrics, Sector, Geography
from datetime import date

# Initialiser l'agent
agent = Agent(max_steps=20, max_steps_per_task=5)

# Définir la cible
target = TargetCompany(
    name="Entreprise CVC Lyon",
    sector="CVC",
    geography="Lyon",
    accounting_standard="French GAAP",
    founded_year=2010
)

# Données financières brutes
financials = FinancialMetrics(
    revenue=5_000_000,  # 5M€
    ebitda_reported=800_000,  # 800k€
    net_income=300_000,
    total_debt=1_200_000,
    cash=200_000,
    period_end=date(2024, 12, 31),
    period_type="annual"
)

# Analyser
query = f"""
Analyse complète DD pour {target.name} :
- Normaliser l'EBITDA (French GAAP)
- Scorer les 4 piliers
- Détecter red flags
- Valoriser (secteur {target.sector})
- Recommandation GO/MAYBE/NO-GO
"""

result = agent.run(query)
print(result)
```

## Thèse d'Investissement Codée

### Critères Financiers
- **EBITDA** : 500k-2M€ ✅
- **Marges saines** : EBITDA% > 10% ✅
- **Rentabilité démontrée** : Historique >3 ans ✅

### 4 Piliers Opérationnels (Score /40, seuil 28)
1. **Opérations répétitives** (0-10)
2. **Revenus récurrents** (0-10)
3. **Faible digitalisation** (0-10)
4. **Base clients diversifiée** (0-10)

### Red Flags (Deal-Breakers)
❌ Déclin structurel
❌ Concentration >30%
❌ Litiges majeurs
❌ Management non-retainable

## Exemples de Requêtes

```python
# Analyse d'un IM complet
"Extrait et analyse cet IM (secteur 3D, Paris) : [texte IM]"

# Normalisation EBITDA uniquement
"Normalise l'EBITDA de cette cible CVC (French GAAP) : Revenue 3M€, EBE 450k€, rémunération gérant 180k€"

# Scoring rapide
"Score les 4 piliers : entreprise maintenance ascenseurs, 200 clients PME/copro, contrats annuels, gestion Excel"

# Valorisation
"Valorise cette cible : secteur Sécurité Incendie, Lyon, EBITDA normalisé 1.2M€"

# DD complète
"DD complète : [résumé cible avec financials]"
```

## Structure du Projet

```
dexter/
├── src/dexter/
│   ├── agent.py              # Orchestration principale
│   ├── model.py              # Interface Claude multi-modèles
│   ├── schemas.py            # Structures Pydantic (Target, Financials, etc.)
│   ├── tools_mbi.py          # Tools MBI (normalize, score, detect, value)
│   ├── prompts_mbi.py        # Prompts spécialisés DD
│   ├── tools.py              # Tools financialdatasets (comparables)
│   └── cli.py                # Interface CLI
```

## Outputs Structurés

L'agent retourne un `DueDiligenceReport` avec :

```python
DueDiligenceReport(
    target=TargetCompany(...),
    financials=FinancialMetrics(...),
    adjustments=[
        EBITDAAdjustment(
            category="Rémunération dirigeant",
            amount=80000,  # +80k€ à l'EBITDA
            description="Salaire gérant 180k€ vs 100k€ marché Lyon secteur CVC",
            source="Compte de résultat ligne 641",
            confidence="High"
        ),
        ...
    ],
    valuation=Valuation(
        ebitda_normalized=880000,  # 800k + 80k
        ev_ebitda_mid=8.0,
        enterprise_value_mid=7040000,  # 7.04M€
        ...
    ),
    four_pillars=FourPillarsScore(
        repetitive_operations=8,
        recurring_revenue=9,
        low_digitalization=7,
        diversified_client_base=8,
        total_score=32,  # > 28 → PASS
        comments="..."
    ),
    red_flags=[...],
    recommendation="GO",
    recommendation_rationale="...",
    requires_human_validation=True
)
```

## Mode Semi-Autonome

Par défaut, l'agent fonctionne en **mode semi-autonome** :

✅ **Analyse automatique complète**
⚠️ **Validation humaine requise** sur :
- Retraitements EBITDA proposés
- Scoring final des 4 piliers
- Valorisation et multiples
- Recommandation GO/NO-GO

Flag `requires_human_validation=True` dans tous les rapports.

## Retraitements EBITDA Standards

### French GAAP
- Rémunération dirigeant excessive (vs benchmark marché)
- Charges personnelles (véhicule, logement, frais)
- Provisions réglementées (neutralisation si non-cash)
- Crédit-bail (retraitement si comparaison IFRS)
- Éléments non-récurrents

### US GAAP / IFRS
- Stock-based compensation
- Restructuring charges
- Impairment charges (non-cash)
- Non-recurring items

## Secteurs Couverts

**Services Techniques Bâtiment :**
CVC, Sécurité Incendie, Ventilation, IRVE, Chaudières, Toiture, Portes, Légionelles, Diagnostics, Entretien

**Services Techniques Spécialisés :**
Véhicules Lourds, Cuisine Pro, GTA

**Services Extérieurs :**
Installations Sportives, Balayeuse, Marquage, Élagage, Paysage, Piscines, Photovoltaïque

**Services B2B :**
Gestion Locative, Courtage Assurance, Infogérance RH, Clinique Esthétique

## Limitations Actuelles

1. **Comparables** : Multiples sectoriels pré-définis (pas de recherche dynamique de comparables FR)
2. **DCF** : Non implémenté (focus multiples)
3. **Extraction IM** : Nécessite texte pré-extrait (pas de parsing PDF natif intégré)
4. **APIs FR** : Pas d'intégration Pappers/Infogreffe (à venir)

## Prochaines Étapes

- [ ] Intégrer APIs Pappers/Infogreffe pour données publiques
- [ ] Recherche dynamique de comparables FR (base Diane/Orbis)
- [ ] Module DCF avec projections
- [ ] Parsing PDF natif pour IMs
- [ ] Dashboard de suivi du pipeline

## Support

Pour questions/bugs : [GitHub Issues](https://github.com/virattt/dexter/issues)

## Licence

MIT
