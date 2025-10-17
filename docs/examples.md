# Exemples & Cas d'Usage

Exemples concrets d'utilisation de Dexter pour analyser des cibles MBI.

## 📊 Test 1 : Analyse FEC réel (Holding TM Capital)

### Contexte
- Société : TM CAPITAL (SIREN 982442899)
- Type : Holding patrimoniale
- Exercice : 2024 (du 06/12/2023 au 31/12/2024)
- Format : FEC au format tabulation

### Données extraites

```python
from dexter.tools_mbi import read_fec

result = read_fec(
    fec_path="/path/to/982442899FEC20241231.TXT",
    encoding="utf-8",
    separator="\t"
)
```

### Résultats

**📅 Période analysée :**
- Début : 06/12/2023
- Fin : 31/12/2024
- **Durée : 391 jours** (pas une année complète)
- Facteur d'annualisation : 0.934

**💰 Données financières :**
| Métrique | Montant | Annualisé |
|----------|---------|-----------|
| Total produits | 14 560,69 € | 13 601,77 € |
| Total charges | 14 986,83 € | - |
| Résultat | -426,14 € | - |
| EBITDA proxy | -426,14 € | - |
| Trésorerie | 21 840,64 € | - |

**📊 Détail charges (top 3) :**
1. Intérêts compte courant (66150000) : 11 685,54 € (78% des charges)
2. Honoraires comptables (62262500) : 720,00 €
3. Honoraires avocats (62262100) : 500,00 €

**📊 Détail produits :**
1. Revenus créances immobilisées (76270000) : 14 549,18 €
   - Lié à obligation de 150 000 € (compte 27210000)
   - Rendement : **9,7% annuel** (355 jours de détention)
2. Gains de change (76600000) : 11,51 €

**🔍 Concentration :**
- Client risk : LOW
- Pas de comptes clients (holding pure)

**🚩 Red flags :**
- [High] Résultat déficitaire : -426,14 €
- Cause : intérêts compte courant > produits financiers

**✅ Validation :**
Comparaison FEC vs PDF des comptes annuels :
- Produits : 14 560,69 € ✅ Match parfait
- Charges : 14 986,83 € ✅ Match parfait
- Résultat : -426,14 € ✅ Match parfait
- Trésorerie : 21 840,64 € ✅ Match parfait

### Enseignements

1. **Calcul au jour près** : FEC détecte 391 jours (pas 365)
2. **Granularité** : Analyse compte par compte (PCG)
3. **Cohérence** : 100% de concordance FEC/PDF
4. **Red flags auto** : Déficit détecté, intérêts élevés alertés

---

## 🏢 Test 2 : Extraction PDF bien formaté (Alizé Clim)

### Contexte
- Société : ALIZÉ CLIM (SARL)
- Secteur : CVC (Climatisation)
- Localisation : Gennevilliers (92)
- Exercice : 2024
- Format : PDF comptable bien structuré

### Extraction PyMuPDF

```python
import fitz

pdf_path = "/path/to/Plaquette2024alize.pdf"
doc = fitz.open(pdf_path)

# Page 4 = attestation expert-comptable avec synthèse
page_4 = doc[3]
text = page_4.get_text()

# Parsing simple
import re
ca_match = re.search(r"chiffre d'affaires\s*\n?\s*([0-9\s,.]+)\s*Euros", text)
resultat_match = re.search(r"résultat\s*net\s*comptable\s*\n?\s*([0-9\s,.]+)\s*Euros", text)
bilan_match = re.search(r"total\s*du\s*bilan\s*\n?\s*([0-9\s,.]+)\s*Euros", text)
```

### Résultats

**💰 Données extraites :**
- Chiffre d'affaires : **8 474 718,38 €**
- Résultat net : **1 040 659,77 €**
- Total bilan : **4 613 406,53 €**

**📊 Ratios calculés :**
- Marge nette : **12,28%** (excellente pour CVC)
- Rotation actif : **1,84x**
- ROA : **22,56%** (très rentable)

### Analyse métier

**Secteur CVC :**
- Multiples indicatifs : 6x - 8x - 10x (EV/EBITDA)
- Récurrence forte (contrats maintenance)
- Fragmentation élevée (consolidation)

**Estimation EBITDA :**
```
Résultat net :              1 040k€
+ IS estimé (25%) :          +347k€
+ Charges financières :       +50k€  (estimé)
+ Amortissements :           +150k€  (estimé)
                           --------
EBITDA proxy :             ~1 600k€
Marge EBITDA :               ~19%
```

**Valorisation rapide :**
```
EBITDA normalisé : 1 600k€
Multiple CVC (mid) : 8x
                   -------
EV estimé : 12,8M€
```

**Score 4 piliers (estimation) :**
1. Repetitive : 8/10 (maintenance CVC standardisée)
2. Recurring : 9/10 (contrats annuels)
3. Low digital : 7/10 (PME traditionnelle → potentiel)
4. Diversified : 7/10 (diversifié géographiquement)
**Total : 31/40** ✅ GO

### Enseignements

1. **PDF bien formaté** → extraction texte facile
2. **Haiku** peut structurer ces données en JSON
3. **Fallback valide** si pas de FEC disponible
4. **Limite** : pas de granularité compte par compte

---

## 🔄 Test 3 : Workflow DD complet (Simulation)

### Contexte
Cible fictive pour illustrer workflow end-to-end

**Société :** SecurFire SAS
**Secteur :** Sécurité incendie (vérification extincteurs, alarmes)
**Localisation :** Lyon
**EBITDA reporté :** 750k€
**CA :** 5,2M€

### Step 1 : Collecte données

```python
from dexter.tools_mbi import read_fec

# FEC fourni par comptable
fec_data = read_fec(
    fec_path="/path/to/securfire_fec_2024.txt",
    encoding="latin-1",
    separator="|"
)
```

**Output :**
```json
{
  "financials": {
    "total_revenue": 5200000,
    "total_expenses": 4450000,
    "ebitda_proxy": 920000,
    "owner_compensation_644": 180000,
    "depreciation_681": 80000,
    "provisions_6815": 90000
  },
  "concentration": {
    "top_client_concentration_pct": 18.5,
    "client_risk": "LOW"
  },
  "red_flags": [
    {
      "type": "Rémunération dirigeant excessive",
      "severity": "Medium",
      "description": "Compte 644 = 3.5% du CA (normalisable)",
      "adjustable_amount": 180000
    }
  ]
}
```

### Step 2 : Normalisation EBITDA

```python
from dexter.tools_mbi import normalize_ebitda

adjustments = normalize_ebitda(
    target=target_company,
    financials=financials,
    im_text=im_full_text
)
```

**Adjustments identifiés :**

| Catégorie | Montant | Description | Confiance |
|-----------|---------|-------------|-----------|
| Rémunération dirigeant | +80k€ | Dirigeant 180k€ vs manager marché 100k€ | High |
| Amortissements | +80k€ | Add-back standard (définition EBITDA) | High |
| Provisions | +90k€ | Provisions exploitation (6815) | High |
| Charges exceptionnelles | +20k€ | Litige client one-off | Medium |

**EBITDA normalisé :**
```
EBITDA reporté :              750k€
+ Rémunération dirigeant :    +80k€
+ Amortissements :            +80k€
+ Provisions :                +90k€
+ Charges exceptionnelles :   +20k€
                            --------
EBITDA normalisé :          1 020k€
Marge EBITDA :               19.6%
```

### Step 3 : Scoring 4 piliers

```python
from dexter.tools_mbi import score_four_pillars

score = score_four_pillars(
    target=target_company,
    business_description=business_model
)
```

**Résultat :**
```
Pilier 1 (Repetitive) : 9/10
  Vérifications réglementaires = process ultra-standardisé
  Checklist identiques pour chaque site

Pilier 2 (Recurring) : 10/10
  100% contrats annuels obligatoires
  Taux renouvellement : 98%
  Réglementation = barrière à l'entrée

Pilier 3 (Low digital) : 8/10
  Planning Excel, rapports papier
  Potentiel : app mobile techniciens, QR codes, dashboards

Pilier 4 (Diversified) : 6/10
  Top 5 clients = 18.5% CA (acceptable)
  Mix copropriétés + PME + grands comptes

TOTAL : 33/40 ✅✅ STRONG GO
```

### Step 4 : Red flags

```python
from dexter.tools_mbi import detect_red_flags

flags = detect_red_flags(
    target=target_company,
    financials=financials,
    im_text=im_text
)
```

**Red flags détectés :**
- [Medium] Rémunération dirigeant excessive : 180k€ (normalisable)
- ✅ Pas de concentration client critique
- ✅ Pas de déclin marché
- ✅ Pas de litiges majeurs

**Conclusion :** Aucun deal breaker

### Step 5 : Valorisation

```python
from dexter.tools_mbi import value_target

valuation = value_target(
    target=target_company,
    ebitda_normalized=1_020_000
)
```

**Multiples sectoriels (Sécurité Incendie) :**
- Low : 7x → 7,14M€
- Mid : 9x → 9,18M€
- High : 11x → 11,22M€

**Ajustements qualité :**
- ✅ Récurrence 100% : +0.5x
- ✅ Marges >15% : +0.5x
- ✅ Digitalisation faible (levier) : +0.5x
- ⚠️ Géographie Lyon (compétitif) : -0.5x

**Multiple ajusté : 10x**

**Valorisation recommandée :**
```
EBITDA normalisé : 1 020k€
Multiple cible : 10x
                 -------
EV : 10,2M€

Structure deal proposée :
  Cash at closing : 8,0M€
  Earn-out (2 ans) : 2,2M€ (si EBITDA maintenu >1M€)
```

### Step 6 : Recommandation finale

```
🎯 RECOMMANDATION : STRONG GO

RATIONALE :
✅ Scoring piliers 33/40 (excellent fit thèse MBI)
✅ Récurrence 100% (contrats obligatoires)
✅ Marges saines 19.6% post-normalisation
✅ Aucun red flag critique
✅ Potentiel digitalisation = création valeur
✅ Secteur défensif (réglementation)

RISQUES IDENTIFIÉS :
⚠️ Concentration client 18.5% (acceptable mais à monitorer)
⚠️ Dirigeant = homme-clé technique (plan transition nécessaire)

NEXT STEPS :
1. Legal DD approfondie (contrats, litiges)
2. RH DD (équipe n°2, plan recrutement manager)
3. Visites sites (Lyon + agences)
4. Draft LOI avec earn-out structure
5. Timeline closing : 3 mois
```

---

## 🎓 Leçons apprises

### FEC > PDF > IM

**Hiérarchie des sources :**
1. **FEC** : Granularité maximale, calculs précis
2. **Excel comptable** : Balance, Grand Livre
3. **PDF bien formaté** : Extraction texte facile
4. **PDF scanné** : OCR nécessaire (Mistral API)
5. **IM banque** : Synthèse mais biais sell-side

### Calculs au jour près

**Exemple TM Capital :**
- FEC indique 391 jours (pas 365)
- Facteur annualisation : 365.25 / 391 = 0.934
- Obligation : 355 jours détention
- Taux annualisé : 9,98% (pas 9,7%)

**Leçon :** Toujours vérifier dates exactes, pas d'approximation

### Red flags hiérarchisés

**Critical (deal breaker) :**
- Déclin structurel marché
- Concentration client >50%
- Dirigeant non remplaçable + départ immédiat

**High (négocier ou passer) :**
- Concentration 30-50%
- Litiges >100k€
- Marges en baisse continue

**Medium (mitigation possible) :**
- Rémunération dirigeant excessive (normalisable)
- Digitalisation faible (opportunité!)
- Fournisseur unique (multi-sourcing possible)

### Multi-modèles efficace

**Haiku pour :**
- Extraction PDF (rapide, pas cher)
- Quick screening (filtrer 100 leads)
- Data validation (checks cohérence)

**Sonnet pour :**
- EBITDA normalization (jugement)
- Red flags (détection signaux faibles)
- Scoring piliers (analyse qualitative)
- Recommendation (synthèse)

**Ratio Haiku/Sonnet optimal : 30/70**
- 30% tokens = extraction/parsing (Haiku)
- 70% tokens = analyse/décision (Sonnet)

---

## 📚 Ressources supplémentaires

### Templates utilisables

**Checklist DD (Google Sheet) :**
- Documents à collecter
- Red flags à vérifier
- Timeline J0-J15

**Template rapport DD (Notion) :**
- Executive summary
- Financial analysis
- 4 pillars scoring
- Red flags
- Valuation
- Recommendation

### Données sectorielles

**Sources multiples :**
- Xerfi : études sectorielles France
- Bpifrance : observatoire TPE/PME
- France Invest : transactions PE
- Epsilon Research : comps M&A

**Mise à jour :**
- Multiples sectoriels : Q1 chaque année
- Géographie cost index : annuel

### API externes (roadmap)

**Enrichissement automatique :**
- Infogreffe API : SIREN, dirigeants, statuts
- Pappers API : scoring financier, liens
- Sirene API : données entreprises

**Comparables :**
- Financial Datasets API : transactions M&A
- Argos Mid-Market : private deals database

---

**Dernière mise à jour :** 2025-01-17
