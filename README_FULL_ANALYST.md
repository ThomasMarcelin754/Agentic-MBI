# Dexter - Investment Analyst for Buy & Build / Rollup 🚀

Agent autonome spécialisé dans l'analyse complète d'investissement pour stratégies de Buy & Build et rollup de PME françaises.

## Vue d'Ensemble

**Dexter** est votre **directeur général adjoint** sur le projet de rollup. Il couvre **6 phases** du cycle d'investissement :

1. **🎯 Sourcing** : Génération listes cibles, scoring, outreach personnalisé
2. **🔍 Due Diligence** : Analyse financière, scoring 4 piliers, red flags
3. **💰 Valorisation** : DCF, deal structuring, LBO modeling
4. **🤝 Négociation** : Stratégie, LOI, gestion objections
5. **🔧 Intégration** : Plan 100 jours, synergies, KPIs
6. **💻 Tech Platform** : Architecture back-office, automatisation

## Positionnement : Investisseur-Opérateur

Dexter est calibré pour des **investisseurs-entrepreneurs** qui :
- Investissent **ET** opèrent
- Visent excellence opérationnelle (pas seulement financière)
- Construisent un groupe industriel pérenne
- Se concentrent sur transformation réelle (digitalisation, processus, synergies)

## Thèse d'Investissement Codée

### Critères Financiers
- **EBITDA** : 500k€ - 2M€
- **Valeur d'entreprise** : 5M€ - 20M€
- **Marges saines** : EBITDA% > 10%

### 4 Piliers Opérationnels (Score /40, seuil 28)
✅ **Opérations répétitives** (0-10) : Automatisables, standardisables
✅ **Revenus récurrents** (0-10) : Contrats, abonnements, missions répétées
✅ **Faible digitalisation** (0-10) : Levier de transformation
✅ **Base clients diversifiée** (0-10) : <30% concentration

### Red Flags (Deal-Breakers)
❌ Déclin structurel
❌ Concentration client/fournisseur >30%
❌ Litiges majeurs
❌ Actif immobilier complexe
❌ Management non-retainable

## Architecture Multi-Modèles Claude

**Claude Sonnet 4.5** (raisonnement complexe) :
- DD financière, retraitements EBITDA
- Valorisation (DCF, LBO)
- Négociation stratégique
- Design tech platform

**Claude Haiku** (vitesse) :
- Extraction IMs (PDFs)
- Génération listes cibles
- Pre-filtering

## Installation

```bash
git clone https://github.com/virattt/dexter.git
cd dexter

uv sync

cp env.example .env
# Ajouter ANTHROPIC_API_KEY=sk-ant-...
```

## Utilisation par Phase

### 🎯 Phase 1 : Sourcing

```python
from dexter.agent import Agent
from dexter.schemas import SourcingCriteria, Sector, Geography

agent = Agent()

query = """
Génère une liste de cibles CVC sur Lyon et Paris
- EBITDA 500k-2M€
- Score ≥70/100
- Outreach personnalisé pour top 10
"""

result = agent.run(query)
```

**Output** : Liste de `TargetLead` avec scoring + templates d'outreach

### 🔍 Phase 2 : Due Diligence

```python
query = """
DD complète pour Entreprise CVC Lyon :
- Revenue : 5M€
- EBE : 800k€ (French GAAP)
- Normaliser EBITDA
- Scorer 4 piliers
- Red flags
- Valorisation
- Recommandation GO/MAYBE/NO-GO
"""

result = agent.run(query)
```

**Output** : `DueDiligenceReport` avec ajustements, score, valuation, recommandation

### 💰 Phase 3 : Valorisation & Deal Structuring

#### DCF Modeling

```python
query = """
DCF pour Entreprise CVC Lyon :
- EBITDA normalisé : 1.2M€
- Croissance : Années 1-5 : [5%, 5%, 4%, 4%, 3%]
- Marge EBITDA cible : 18%
- WACC : 10%
- Terminal growth : 2%
"""

result = agent.run(query)
```

**Output** : `DCFValuation` avec EV, sensitivity analysis

#### Deal Structuring

```python
query = """
Structure deal pour Entreprise CVC Lyon :
- EV cible : 10M€
- Vendeur : Retraite (full exit souhaité)
- Cash disponible : 3M€
- Propose structure optimale
"""

result = agent.run(query)
```

**Output** : `DealStructure` avec cash/earn-out/vendor loan/equity rollover

#### LBO Modeling

```python
query = """
LBO pour Entreprise CVC Lyon :
- EV : 10M€
- EBITDA : 1.2M€
- Equity : 3M€
- Leverage cible : 3x
- Projections IRR & MOIC
"""

result = agent.run(query)
```

**Output** : `LBOModel` avec structure dette, IRR, MOIC projetés

### 🤝 Phase 4 : Négociation

#### Stratégie de Négociation

```python
query = """
Stratégie négociation Entreprise CVC Lyon :
- Valuation range : 9M€ - 11M€
- Vendeur : Entrepreneur familial, 30 ans métier, attachement émotionnel
- Prépare walk-away/target/stretch + contre-arguments
"""

result = agent.run(query)
```

**Output** : `NegotiationStrategy` avec prix, forces, objections, contre-args

#### Rédaction LOI

```python
query = """
Rédige LOI pour Entreprise CVC Lyon :
- EV proposé : 10M€
- Structure : 70% cash, 30% earn-out sur 2 ans
"""

result = agent.run(query)
```

**Output** : `LOI` complet

### 🔧 Phase 5 : Intégration

#### Plan 100 Jours

```python
query = """
Plan 100 jours post-acquisition Entreprise CVC Lyon :
- DD insights : [résumé DD]
- Priorités mois 1, 2, 3
- Quick wins
- Risques intégration
"""

result = agent.run(query)
```

**Output** : `Integration100DayPlan` avec jalons mensuels

#### Identification Synergies

```python
query = """
Identifie synergies Entreprise CVC Lyon :
- Portfolio existant : [Entreprise 3D Paris, Entreprise Sécurité Lyon]
- Quantifie revenus, coûts, opérationnelles, financières
"""

result = agent.run(query)
```

**Output** : `List[Synergy]` avec valeur annuelle EUR, timeline, confiance

### 💻 Phase 6 : Tech Platform

#### Design Architecture

```python
query = """
Design tech platform Entreprise CVC Lyon :
- Tech actuelle : Excel, Outlook, QuickBooks desktop
- Modules : Finance, HR, CRM, Ops, Procurement, Analytics
- Roadmap 18 mois
"""

result = agent.run(query)
```

**Output** : `TechRoadmap` avec modules, build/buy, coûts, ROI

#### Automatisation

```python
query = """
Identifie opportunités automatisation Entreprise CVC Lyon :
- Processus actuels : Facturation manuelle, planning Excel, paie papier
- Quantifie gains
"""

result = agent.run(query)
```

**Output** : `List[AutomationOpportunity]` ranked par ROI

## Mode Semi-Autonome

**Par défaut** :
- Agent analyse de bout en bout
- Flag **validation humaine requise** sur décisions critiques :
  - Retraitements EBITDA
  - Scoring final
  - Valorisation
  - Structure de deal
  - Recommandation GO/NO-GO

`requires_human_validation=True` dans tous les outputs structurés.

## Mapping Systématique (3 Dimensions)

Chaque analyse est mappée sur :

### 1. Système Comptable
- **French GAAP** : EBE, provisions réglementées, crédit-bail hors bilan
- **US GAAP** : Operating Income + D&A
- **IFRS** : IFRS 16 leases

### 2. Secteur (avec multiples EV/EBITDA)
Exemples :
- CVC : 6-8-10x
- Sécurité Incendie : 7-9-11x
- IRVE : 8-11-14x
- Gestion Locative : 8-10-12x
- 3D : 5.5-7.5-9.5x

Voir `tools_mbi.py:48-78` pour la liste complète.

### 3. Géographie (impact coûts)
Index vs baseline :
- Paris : +30%
- Lyon : +10%
- Nice : +15%

## Exemples de Requêtes Transversales

### "Analyse complète de A à Z"

```python
query = """
Pipeline complet pour secteur CVC sur Lyon :

1. SOURCING
   - Génère liste 50 cibles
   - Score et filtre ≥70
   - Outreach top 10

2. DD (pour 3 meilleures réponses)
   - Analyse financials
   - Score 4 piliers
   - Red flags
   - Valo

3. NÉGOCIATION (pour 1 finaliste)
   - Stratégie
   - LOI

4. INTÉGRATION (si acquisition validée)
   - Plan 100j
   - Synergies
   - Tech roadmap
"""
```

Dexter orchestrera automatiquement toutes les phases.

### "Deep Dive sur un sujet"

```python
# Focus valorisation uniquement
query = """
Valorisation complète Entreprise X :
- DCF (assumptions : [détail])
- Multiples sectoriels
- Deal structuring (3 scénarios)
- LBO model
- Sensibilités
"""
```

## Structure du Projet

```
dexter/
├── src/dexter/
│   ├── agent.py                      # Orchestration principale
│   ├── model.py                      # Interface Claude multi-modèles
│   │
│   ├── schemas.py                    # Structures Pydantic (TOUTES phases)
│   │   ├── Phase 1: TargetLead, SourcingCriteria, OutreachTemplate
│   │   ├── Phase 2: TargetCompany, FinancialMetrics, DueDiligenceReport
│   │   ├── Phase 3: DCFValuation, DealStructure, LBOModel
│   │   ├── Phase 4: NegotiationStrategy, LOI
│   │   ├── Phase 5: Integration100DayPlan, Synergy, IntegrationKPIs
│   │   └── Phase 6: TechRoadmap, AutomationOpportunity
│   │
│   ├── tools_mbi.py                  # Tools DD (Phase 2)
│   ├── tools_full_analyst.py         # Tools phases 1, 3, 4, 5, 6
│   │
│   ├── prompts_mbi.py                # Prompts DD (Phase 2)
│   ├── prompts_full_analyst.py       # Prompts toutes phases
│   │
│   └── cli.py                        # Interface CLI
│
├── pyproject.toml                    # Dépendances (Anthropic)
└── README_FULL_ANALYST.md            # Ce fichier
```

## Outputs Structurés

### Phase 1 : Sourcing
```python
TargetLead(
    company_name="CVC Services Lyon",
    sector="CVC",
    geography="Lyon",
    estimated_ebitda=1_200_000,
    quick_score=85,
    ...
)

OutreachTemplate(
    email_subject="Partnership pour moderniser CVC Services Lyon",
    email_body="...",
    follow_up_strategy="..."
)
```

### Phase 2 : DD
```python
DueDiligenceReport(
    target=TargetCompany(...),
    financials=FinancialMetrics(ebitda_normalized=1_100_000, ...),
    adjustments=[
        EBITDAAdjustment(category="Rémunération dirigeant", amount=80_000, ...)
    ],
    four_pillars=FourPillarsScore(total_score=32, ...),
    red_flags=[...],
    valuation=Valuation(enterprise_value_mid=9_000_000, ...),
    recommendation="GO",
    requires_human_validation=True
)
```

### Phase 3 : Valorisation
```python
DCFValuation(
    enterprise_value=10_200_000,
    equity_value=9_500_000,
    sensitivity_analysis={...}
)

DealStructure(
    cash_at_closing=7_000_000,
    earn_out=3_000_000,
    earn_out_conditions="EBITDA ≥1.3M€ en Année 2",
    ...
)

LBOModel(
    equity=3_000_000,
    senior_debt=6_500_000,
    leverage_ratio=2.8,
    projected_irr=25.3,
    projected_moic=3.2
)
```

### Phase 4 : Négociation
```python
NegotiationStrategy(
    walk_away_price=11_500_000,
    target_price=9_500_000,
    stretch_price=10_200_000,
    strengths=["Certainty of close", "Tech value-add", ...],
    counter_arguments={
        "Price too low": "Multiple de 8x vs 7.5x marché, justifié par..."
    }
)
```

### Phase 5 : Intégration
```python
Integration100DayPlan(
    month_1_priorities=["All-hands meeting", "Retention packages", ...],
    quick_wins=["Renégocier contrat fournisseur Y → -50k€/an"],
    ...
)

Synergy(
    category="Cost",
    description="Centralisation achats véhicules",
    annual_value_eur=120_000,
    timeline_to_realize="6 months",
    confidence="High"
)
```

### Phase 6 : Tech
```python
TechRoadmap(
    modules=[
        TechPlatformModule(
            name="Finance",
            current_state="QuickBooks desktop",
            target_state="Pennylane cloud",
            build_vs_buy="Buy",
            estimated_cost_eur=15_000,
            estimated_roi_months=8
        ),
        ...
    ],
    total_investment_eur=80_000,
    expected_annual_savings_eur=150_000
)

AutomationOpportunity(
    process_name="Facturation",
    current_manual_hours_per_month=20,
    automation_potential_percent=80,
    annual_cost_savings_eur=18_000,
    priority="Critical"
)
```

## Secteurs Couverts

**Services Techniques Bâtiment :**
CVC, Sécurité Incendie, Ventilation, IRVE, Chaudières, Toiture, Portes, Légionelles, Diagnostics, Entretien

**Services Techniques Spécialisés :**
Véhicules Lourds, Cuisine Pro, GTA

**Services Extérieurs :**
Installations Sportives, Balayeuse, Marquage, Élagage, Paysage, Piscines, Photovoltaïque

**Services B2B :**
Gestion Locative, Courtage Assurance, Infogérance RH, Clinique Esthétique

## Retraitements EBITDA Standards

### French GAAP
- Rémunération dirigeant excessive (vs benchmark)
- Charges personnelles (véhicule, logement)
- Provisions réglementées (neutralisation non-cash)
- Crédit-bail (retraitement IFRS si besoin)
- Éléments non-récurrents

### US GAAP / IFRS
- Stock-based compensation
- Restructuring charges
- Impairment charges
- Non-recurring items

## Limitations & Développements Futurs

### Limitations Actuelles
- **Comparables** : Multiples pré-définis (pas de recherche dynamique comparables FR)
- **APIs FR** : Pas d'intégration Pappers/Infogreffe (données simulées)
- **Extraction PDF** : Nécessite texte pré-extrait (parsing natif à venir)
- **DCF** : Implémentation simplifiée (pas de model Excel exportable)

### Roadmap
- [ ] Intégration Pappers/Infogreffe API
- [ ] Recherche dynamique comparables (base Diane/Orbis)
- [ ] Export Excel pour DCF/LBO models
- [ ] Parsing PDF natif pour IMs
- [ ] Dashboard pipeline tracking
- [ ] Intégration CRM pour suivi deal flow

## Support

Questions/bugs : [GitHub Issues](https://github.com/virattt/dexter/issues)

## Licence

MIT

---

**Dexter : Votre DG adjoint pour le rollup** 🚀
