# Guide Due Diligence Opérationnel

Guide pratique pour analyser une cible MBI/Rollup avec Dexter.

## 🎯 Thèse d'investissement

### Critères financiers
- **EBITDA normalisé:** 500k€ - 2M€
- **Enterprise Value:** 5M€ - 20M€
- **Marge EBITDA:** >10% (idéal >15%)
- **Croissance:** Stable ou croissante (pas de déclin structurel)
- **Dette nette / EBITDA:** <3x

### Les 4 piliers opérationnels (score /40, seuil GO ≥28)

#### 1. Opérations répétitives (0-10)
**Objectif:** Identifier le potentiel de standardisation et automation

**Scoring:**
- **10/10:** Process ultra-répétitifs (maintenance préventive, contrôles réglementaires)
- **7-9/10:** Répétitifs avec adaptations (installation, dépannage)
- **4-6/10:** Mix projet/récurrent
- **0-3/10:** Sur-mesure, projets uniques

**Questions clés:**
- Les interventions suivent-elles des protocoles standardisés?
- Peut-on créer des checklist/playbooks?
- Les techniciens font-ils la même chose ou du sur-mesure?

**Exemples:**
- ✅ Sécurité incendie: vérification annuelle = process identique
- ✅ CVC: contrats maintenance = planning récurrent
- ❌ Conseil stratégique: chaque mission unique

#### 2. Revenus récurrents (0-10)
**Objectif:** Prédictibilité du cash flow

**Scoring:**
- **10/10:** 100% récurrent (contrats annuels, abonnements)
- **7-9/10:** 70-90% récurrent
- **4-6/10:** 40-70% récurrent
- **0-3/10:** <40% récurrent, projets one-shot

**Questions clés:**
- % CA sous contrat pluriannuel?
- Taux de renouvellement?
- MRR (Monthly Recurring Revenue)?
- Contrats avec tacite reconduction?

**Types de récurrence:**
- **Contractuel:** Maintenance obligatoire (ascenseurs, extincteurs)
- **Réglementaire:** Diagnostics, contrôles légaux
- **Consommable:** Pièces, filtres, produits
- **Abonnement:** SaaS, licence

#### 3. Faible digitalisation (0-10)
**Objectif:** Levier de transformation = création de valeur

**Scoring:**
- **10/10:** Excel/papier, zéro logiciel métier → énorme potentiel
- **7-9/10:** Logiciel métier basique, beaucoup de manuel
- **4-6/10:** ERP/CRM mais sous-utilisé
- **0-3/10:** Déjà très digitalisé, peu de marge

**Questions clés:**
- Planning techniciens? (Excel vs. app mobile)
- Facturation? (manuelle vs. auto)
- Suivi chantiers? (papier vs. digital)
- Reporting? (manuel vs. dashboards)

**Quick wins digitaux:**
- App mobile techniciens (géoloc, feuille de route)
- Auto-facturation (contrats → factures auto)
- CRM clients (relances auto, up-sell)
- Tableaux de bord gestion (KPIs temps réel)

#### 4. Base clients diversifiée (0-10)
**Objectif:** Réduire risque de concentration

**Scoring:**
- **10/10:** Top 5 clients <15% CA
- **7-9/10:** Top 5 clients 15-25% CA
- **4-6/10:** Top 5 clients 25-35% CA
- **0-3/10:** Top 5 clients >35% CA (red flag si >50%)

**Red flag:** Concentration >30% = risque majeur

**Questions clés:**
- Qui sont les 5 plus gros clients?
- Depuis combien de temps?
- Contrats résiliables?
- Dépendance mutuelle?

## 🚩 Red Flags (deal breakers)

### 1. Déclin structurel du marché
**Sévérité:** Critical
- Secteur en contraction (ex: chaudières gaz avec transition énergétique)
- Technologie obsolète
- Substitution par nouveaux entrants

**Validation:**
- Analyse de marché (études sectorielles)
- Évolution CA sur 3-5 ans
- Pipeline futur

### 2. Concentration client >30%
**Sévérité:** High (Critical si >50%)
- Top 5 clients = >30% CA
- 1 client = >20% CA

**Risques:**
- Perte d'un client = impact majeur
- Pouvoir de négociation déséquilibré
- Difficultés refinancement

**Mitigation:**
- Contrats long-terme signés
- Barrières à l'entrée élevées
- Croissance pour diluer

### 3. Concentration fournisseur
**Sévérité:** Medium
- Dépendance à 1-2 fournisseurs exclusifs
- Pas d'alternative

**Mitigation:**
- Multi-sourcing possible?
- Contrats cadres sécurisés?

### 4. Litiges majeurs
**Sévérité:** High
- Litiges prudhommaux
- Contentieux clients >100k€
- Litiges fiscaux/URSSAF

**Validation:**
- Revue annexes légales
- Provisions comptabilisées?
- Impact potentiel quantifié

### 5. Actif immobilier complexe
**Sévérité:** Medium
- Locaux en crédit-bail complexe
- Murs propriété du dirigeant
- Bail commercial précaire

**Impact:**
- Complique structuration deal
- Risque loyers excessifs post-deal

### 6. Management non retainable
**Sévérité:** Critical pour MBI
- Dirigeant = homme-clé technique
- Pas d'équipe en place
- Départ immédiat du fondateur

**Mitigation:**
- Management fee post-closing
- Earn-out lié à transition
- Équipe n°2 identifiée

## 📊 Normalisation EBITDA (French GAAP)

### Compte 644: Rémunération exploitant
**Retraitement le plus courant**

**Logique:**
- Dirigeant de PME se verse souvent rémunération excessive
- Post-acquisition: remplacé par manager salarié standard

**Méthode:**
```
Rémunération dirigeant actuelle:     150k€
Salaire manager de marché:            80k€
                                    -------
Retraitement (add-back EBITDA):      +70k€
```

**Validation:**
- Comparer salaire de marché (secteur, géographie, taille)
- Sources: études APEC, cabinets RH

### Compte 681: Dotations amortissements
**Add-back systématique pour EBITDA**

**Principe:**
- EBITDA = Earnings Before Interest, Taxes, Depreciation, Amortization
- On réintègre les amortissements (charges non-cash)

**Attention:**
- Ne pas confondre avec "ajustement" EBITDA
- C'est la définition même de l'EBITDA

### Compte 6815: Provisions
**Add-back si non-cash ou non-récurrent**

**Exemples:**
- Provision litige exceptionnel → add-back
- Provision garantie récurrente → garder

### Compte 612: Crédit-bail
**Retraitement si comparaison IFRS 16**

**Logique:**
- French GAAP: crédit-bail hors bilan (loyer en charge)
- IFRS 16: crédit-bail au bilan (amortissement + intérêt)

**Pour comparaison multiples:**
- Si comparables en IFRS → retraiter cible French GAAP
- Ajouter loyers crédit-bail à EBITDA
- Ajouter dette équivalente au bilan

### Charges personnelles
**Voitures, voyages, logement dirigeant**

**Détection:**
- Compte 6063: Carburant excessif (voiture perso)
- Compte 6257: Voyages/réceptions non-business
- Loyer résidence secondaire

**Retraitement:**
```
Charges véhicules:                    25k€
Usage personnel estimé (50%):        -12.5k€
                                    --------
Add-back EBITDA:                     +12.5k€
```

### Éléments non-récurrents (67X)
**Charges exceptionnelles one-off**

**Exemples:**
- Indemnités licenciement (restructuration)
- Amendes/pénalités exceptionnelles
- Frais acquisition/fusion

**Validation:**
- Vraiment exceptionnel? (pas récurrent masqué)
- Montant matériel? (>5% EBITDA)

## 💰 Valorisation

### Multiples sectoriels (EV/EBITDA)

| Secteur                   | Low  | Mid  | High | Rationale                          |
|---------------------------|------|------|------|------------------------------------|
| CVC                       | 6x   | 8x   | 10x  | Services récurrents, fragmentation |
| Sécurité Incendie         | 7x   | 9x   | 11x  | Réglementation forte, LT           |
| 3D (Désinfection)         | 5.5x | 7.5x | 9.5x | Récurrence moyenne, saisonnalité   |
| IRVE (bornes recharge)    | 8x   | 11x  | 14x  | Croissance forte, tech             |
| Chaudières                | 5x   | 7x   | 9x   | Maturité, déclin progressif        |
| Toiture                   | 4.5x | 6.5x | 8.5x | Cyclique, météo                    |
| Légionelles               | 7x   | 9x   | 11x  | Réglementation stricte             |
| Diagnostics               | 6x   | 8x   | 10x  | Obligatoire, fragmentation         |
| Entretien Bâtiment        | 5x   | 7x   | 9x   | Multi-services, standardisable     |
| Gestion Locative B2B      | 8x   | 10x  | 12x  | Revenus très récurrents            |
| Courtage Assurance        | 7x   | 9.5x | 12x  | Commissions récurrentes            |

**Facteurs d'ajustement:**
- **+1-2x:** Digitalisation avancée, marges >20%, croissance >10%/an
- **-1-2x:** Concentration client, marges <10%, déclin

### Géographie (coût et attractivité)

| Zone           | Index coût | Impact multiple     |
|----------------|------------|---------------------|
| Paris          | 1.30       | Coûts +30%, neutre  |
| Lyon           | 1.10       | Attractif           |
| Marseille      | 1.05       | Neutre              |
| Toulouse       | 1.05       | Croissance          |
| Nice           | 1.15       | Coûts élevés        |
| Autres régions | 1.00       | Baseline            |

### Méthode DCF (optionnelle)

**Quand l'utiliser:**
- Cible avec croissance forte et prévisible
- Capex et BFR structurés
- Visibilité >3 ans

**Paramètres clés:**
- WACC: 10-12% (PME non cotée)
- Taux perpétuel: 2%
- EBITDA margin: tendance 5 ans

**Limite:**
- Sensibilité forte aux hypothèses
- Préférer multiples pour PME

## 🔄 Workflow DD complet

### Phase 1: Collecte données (J0 - J2)

**Documents prioritaires:**
1. **FEC (Fichier Écritures Comptables)** ← priorité absolue
2. Comptes annuels 3 derniers exercices (liasse fiscale)
3. Grand Livre / Balance
4. Information Memorandum (si M&A structuré)
5. Contrats clients top 10
6. Liste personnel (organigramme)

**Si FEC disponible:**
```python
from dexter.tools_mbi import read_fec

result = read_fec(
    fec_path="/path/to/FEC.txt",
    encoding="latin-1",
    separator="\t"
)
# → Extraction automatique: CA, EBITDA, concentration, red flags
```

**Si que PDF:**
```python
# PyMuPDF extraction + Haiku parsing
from dexter.tools_mbi import extract_im_data
import fitz

doc = fitz.open("comptes_annuels.pdf")
text = "\n".join([page.get_text() for page in doc])

data = extract_im_data(text)
# → TargetCompany + FinancialMetrics structurés
```

### Phase 2: Analyse financière (J3 - J5)

**Normalisation EBITDA:**
```python
from dexter.tools_mbi import normalize_ebitda

adjustments = normalize_ebitda(
    target=target_company,
    financials=financial_metrics,
    im_text=full_im_text
)
# → Liste des retraitements avec montants et justifications
```

**Résultat attendu:**
```
EBITDA reporté:              800k€
+ Rémunération dirigeant:    +70k€
+ Amortissements:           +120k€
+ Charges exceptionnelles:   +30k€
+ Provisions non-récurrentes:+15k€
                           --------
EBITDA normalisé:          1,035k€
Marge EBITDA:                12.9%
```

### Phase 3: Scoring piliers (J6 - J7)

```python
from dexter.tools_mbi import score_four_pillars

score = score_four_pillars(
    target=target_company,
    business_description=business_model_text
)
# → Score /40 + commentaires détaillés
```

**Exemple output:**
```
Pilier 1 (Repetitive):      8/10
  Maintenance CVC = process standardisés

Pilier 2 (Recurring):       9/10
  90% CA sous contrats annuels, taux renouvellement 95%

Pilier 3 (Low digital):     7/10
  Planning Excel, facturation manuelle
  Potentiel: app mobile techniciens, auto-facturation

Pilier 4 (Diversified):     6/10
  Top 5 clients = 28% CA (acceptable)

TOTAL: 30/40 ✅ GO
```

### Phase 4: Red flags (J8 - J9)

```python
from dexter.tools_mbi import detect_red_flags

flags = detect_red_flags(
    target=target_company,
    financials=financial_metrics,
    im_text=full_im_text
)
# → Liste red flags avec sévérité
```

**Triage:**
- **Critical:** Deal breaker → NO-GO immédiat
- **High:** Blocker majeur → négocie ou passe
- **Medium:** A surveiller → plan mitigation
- **Low:** Note dans rapport

### Phase 5: Valorisation (J10 - J12)

```python
from dexter.tools_mbi import value_target

valuation = value_target(
    target=target_company,
    ebitda_normalized=1_035_000
)
# → Range EV avec multiples sectoriels
```

**Exemple output:**
```
Secteur: CVC
EBITDA normalisé: 1,035k€

Multiples sectoriels:
  Low (6x):   6.2M€
  Mid (8x):   8.3M€
  High (10x): 10.4M€

Recommandation: Offrir 7.5M€ (7.2x)
  Rationale: Marges solides, digitalisation = levier
  Walk-away price: 9M€
```

### Phase 6: Rapport final (J13 - J15)

**Structure rapport DD:**

1. **Executive Summary**
   - GO / MAYBE / NO-GO
   - Rationale en 3-5 bullets

2. **Business Overview**
   - Secteur, géographie, business model
   - Position concurrentielle

3. **Financial Analysis**
   - Historique 3 ans
   - EBITDA normalisé
   - Marges, croissance

4. **Scoring 4 Piliers**
   - Score détaillé /40
   - Fit avec thèse MBI

5. **Red Flags**
   - Liste priorisée
   - Impact/mitigation

6. **Valuation**
   - Range EV
   - Prix cible
   - Structuration deal

7. **Next Steps**
   - Due diligence approfondie (legal, RH)
   - Termes LOI
   - Timeline closing

## 📋 Checklist DD

### Documents à obtenir

**Financier (P0):**
- [ ] FEC 3 derniers exercices
- [ ] Liasse fiscale 3 ans
- [ ] Situation intermédiaire N
- [ ] Grand Livre détaillé
- [ ] Balance âgée clients/fournisseurs

**Commercial (P0):**
- [ ] Liste clients + CA par client
- [ ] Top 20 contrats
- [ ] Taux attrition/renouvellement
- [ ] Pipeline commercial

**Opérationnel (P1):**
- [ ] Organigramme + fiches de poste
- [ ] Grille salaires
- [ ] Process clés (maintenance, intervention)
- [ ] KPIs opérationnels

**Juridique (P1):**
- [ ] Statuts société
- [ ] Pacte actionnaires
- [ ] Contrats cadres fournisseurs
- [ ] Litiges en cours
- [ ] Propriété intellectuelle

**RH (P2):**
- [ ] Contrats de travail
- [ ] Accords entreprise
- [ ] Historique IRP
- [ ] Turnover

### Red flags à vérifier

**Financier:**
- [ ] Concentration client >30%
- [ ] Croissance CA négative
- [ ] Marges en baisse
- [ ] BFR qui dérive
- [ ] Dette / EBITDA >3x

**Opérationnel:**
- [ ] Dirigeant = homme clé
- [ ] Pas d'équipe n°2
- [ ] Process non documentés
- [ ] Qualité variable

**Commercial:**
- [ ] Dépendance 1-2 clients
- [ ] Contrats résiliables court-terme
- [ ] Marché en déclin
- [ ] Nouveaux entrants agressifs

**Juridique:**
- [ ] Litiges >100k€
- [ ] Contentieux prudhommal
- [ ] Dettes fiscales/URSSAF
- [ ] IP non protégée

**RH:**
- [ ] Turnover >20%
- [ ] Grève/conflits sociaux
- [ ] Masse salariale non alignée
- [ ] Compétences clés non remplaçables

---

**Dernière mise à jour:** 2025-01-17
