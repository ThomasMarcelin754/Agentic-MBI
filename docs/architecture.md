# Architecture Technique — Dexter MBI

## Vue d'ensemble

Dexter est un agent autonome multi-modèles orchestrant des tâches complexes de due diligence M&A. Il combine **Sonnet 4.5** (raisonnement complexe) et **Haiku** (extraction rapide) pour analyser des cibles d'acquisition.

## Stack technique

```
┌─────────────────────────────────────────┐
│  User Query (DD complète sur cible X)   │
└──────────────┬──────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Agent orchestrator   │
    │  (agent.py)           │
    │  - Task planning      │
    │  - Tool selection     │
    │  - Multi-step exec    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────────────────────┐
    │         Model Router                  │
    ├───────────────────┬──────────────────┤
    │   Sonnet 4.5      │     Haiku        │
    │   Complex tasks   │   Fast tasks     │
    │   - EBITDA norm   │   - PDF extract  │
    │   - Red flags     │   - IM parsing   │
    │   - Valuation     │   - Quick screen │
    └───────────────────┴──────────────────┘
               │
               ▼
    ┌──────────────────────────────────────┐
    │           Tool Suite                  │
    │  - read_fec (FEC analysis)            │
    │  - extract_im_data (PDF → JSON)       │
    │  - normalize_ebitda (adjustments)     │
    │  - score_four_pillars (thesis fit)    │
    │  - detect_red_flags (deal breakers)   │
    │  - value_target (multiples + DCF)     │
    └───────────────────────────────────────┘
```

## Modèles & stratégie de routage

### Claude Sonnet 4.5
**Usage:** Raisonnement complexe, jugement qualitatif
- EBITDA normalization (identifier retraitements non évidents)
- Red flag analysis (détecter signaux faibles)
- Valuation judgment (ajuster multiples selon qualité)
- Deal structuring (optimiser cash/earn-out)

**Coût:** ~$15 / 1M tokens input, ~$75 / 1M tokens output

### Claude Haiku
**Usage:** Extraction rapide, tâches structurées
- PDF text extraction (IM, comptes annuels)
- Table parsing (bilan, compte de résultat)
- Quick screening (filtrage initial de leads)
- Data validation (checks cohérence)

**Coût:** ~$0.80 / 1M tokens input, ~$4 / 1M tokens output

### Stratégie de routage
```python
# Règle simple dans model.py
if task in ["extract", "parse", "screen"]:
    model = "claude-3-haiku-20240307"
else:
    model = "claude-sonnet-4-20250514"
```

## Architecture des tools

### 1. read_fec (priorité absolue)
```python
read_fec(fec_path, encoding="latin-1", separator="\t") -> Dict
```
**Input:** Fichier FEC (format officiel français)
**Output:**
- Financials: CA, charges, EBITDA proxy
- Concentration: top 5 clients/fournisseurs
- Red flags: concentration >30%, déficit, saisonnalité
- Calculs au jour près (annualization si besoin)

**Plan Comptable Général mapping:**
- Classe 7 (produits): 706 (prestations services)
- Classe 6 (charges): 644 (rémunération exploitant), 681 (amortissements)
- Classe 4: 411XXX (clients), 401XXX (fournisseurs)

### 2. extract_im_data (fallback si pas de FEC)
```python
extract_im_data(im_text: str) -> Dict
```
**Workflow:**
1. PyMuPDF extrait texte brut du PDF
2. Haiku structure en JSON (TargetCompany + FinancialMetrics)
3. Sonnet valide et enrichit

### 3. normalize_ebitda
```python
normalize_ebitda(target, financials, im_text) -> List[EBITDAAdjustment]
```
**Retraitements French GAAP:**
- Compte 644: rémunération exploitant excessive
- Compte 612: crédit-bail (si comparaison IFRS)
- Charges personnelles (véhicule, logement)
- Provisions réglementées
- Éléments non-récurrents (67X)

**Output:** EBITDA normalisé + liste ajustements avec confiance

### 4. score_four_pillars
```python
score_four_pillars(target, business_description) -> FourPillarsScore
```
**Piliers (scoring 0-10):**
1. Repetitive operations (standardisable?)
2. Recurring revenue (contrats, MRR?)
3. Low digitalization (potentiel transformation?)
4. Diversified client base (<30% concentration)

**Seuil GO:** ≥28/40

### 5. detect_red_flags
```python
detect_red_flags(target, financials, im_text) -> List[RedFlag]
```
**Deal breakers:**
- Déclin structurel marché
- Concentration client >30%
- Litiges majeurs
- Actif immobilier complexe
- Management non retainable

### 6. value_target
```python
value_target(target, ebitda_normalized) -> Valuation
```
**Méthodes:**
- Multiples sectoriels (SECTOR_MULTIPLES dict)
- Ajustement géographique (GEOGRAPHY_COST_INDEX)
- DCF optionnel

## Schemas Pydantic

Tous les inputs/outputs sont typés via `schemas.py`:

```python
class TargetCompany(BaseModel):
    name: str
    sector: Sector  # Literal["CVC", "IRVE", ...]
    geography: Geography
    accounting_standard: AccountingStandard  # French GAAP / IFRS / US GAAP

class FinancialMetrics(BaseModel):
    revenue: float
    ebitda_reported: float
    ebitda_normalized: Optional[float]
    total_debt: Optional[float]
    period_end: date
    period_type: Literal["annual", "quarterly", "ttm"]

class EBITDAAdjustment(BaseModel):
    category: Literal["Non-récurrent", "Rémunération dirigeant", ...]
    amount: float
    description: str
    source: str
    confidence: Literal["High", "Medium", "Low"]

class DueDiligenceReport(BaseModel):
    target: TargetCompany
    financials: FinancialMetrics
    adjustments: List[EBITDAAdjustment]
    valuation: Valuation
    four_pillars: FourPillarsScore
    red_flags: List[RedFlag]
    recommendation: Literal["GO", "MAYBE", "NO-GO"]
    requires_human_validation: bool = True
```

## Flow d'exécution type

### Cas d'usage: DD complète sur cible CVC

```
1. User: "Analyse société Alizé Clim (CVC, 92)"
           ↓
2. Agent: plan multi-step
   - Extract FEC si disponible
   - Sinon extract PDF comptes
   - Normalize EBITDA
   - Score pillars
   - Detect red flags
   - Value target
   - Generate recommendation
           ↓
3. read_fec(fec_path) [FEC fourni]
   → Output: CA 8.5M€, EBITDA proxy 1.2M€,
             marge 14%, période 365j
           ↓
4. normalize_ebitda(target, financials)
   Sonnet analyse:
   - Pas de 644 détecté
   - Amortissements 681: +150k€
   - Provisions 6815: +50k€
   → EBITDA normalisé: 1.4M€
           ↓
5. score_four_pillars(target, business_desc)
   Sonnet score:
   - Repetitive: 8/10 (maintenance CVC)
   - Recurring: 9/10 (contrats annuels)
   - Low digital: 7/10 (Excel, papier)
   - Diversified: 6/10 (top 3 = 25%)
   → Total: 30/40 ✅ GO
           ↓
6. detect_red_flags(target, financials)
   → Aucun red flag détecté
           ↓
7. value_target(target, ebitda_normalized=1.4M€)
   Secteur CVC: 6-8-10x
   → EV: 8.4M€ (mid), range 8-14M€
           ↓
8. DueDiligenceReport generated
   Recommendation: GO
   Rationale: Marges saines, recurring fort,
              digitalisation = levier valeur
```

## Performance & coûts

### Analyse type (1 cible)
- FEC: 200 écritures → 5k tokens
- IM PDF: 50 pages → 30k tokens
- Total processing: ~50k tokens input, ~5k tokens output

**Coût estimé par DD:**
- Haiku (extraction): $0.04
- Sonnet (analyse): $1.50
- **Total: ~$1.50/cible**

### Optimisations
- Cache FEC parsé (évite re-parsing)
- Haiku pour screening initial (filtre avant Sonnet)
- Batch processing pour comparables

## Sécurité & validation

### Human-in-the-loop
Tous les rapports DD ont `requires_human_validation: bool = True` par défaut.

### Traçabilité
- Tous les ajustements EBITDA avec `source` et `confidence`
- Red flags avec `severity` et `is_deal_breaker`
- Logs détaillés (utils/logger.py)

### Limites connues
- EBITDA normalization: besoin validation expert-comptable
- Multiples sectoriels: base 2024, à actualiser
- Red flags: détection patterns, pas exhaustif

## Extensibilité

### Ajouter un nouveau secteur
```python
# Dans tools_mbi.py
SECTOR_MULTIPLES["Nouveau Secteur"] = {
    "low": 5.0, "mid": 7.0, "high": 9.0,
    "rationale": "Justification basée sur comps"
}
```

### Ajouter un tool
```python
# 1. Définir input schema
class NewToolInput(BaseModel):
    param: str = Field(..., description="...")

# 2. Créer tool
@tool(args_schema=NewToolInput)
def new_tool(param: str) -> Dict:
    # Logic
    return {"result": "..."}

# 3. Ajouter à MBI_TOOLS
MBI_TOOLS = [read_fec, ..., new_tool]
```

### Brancher API externe
```python
# Example: Infogreffe pour enrichissement
import requests

def enrich_from_infogreffe(siren: str) -> Dict:
    url = f"https://api.infogreffe.fr/v1/entreprise/{siren}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

## Roadmap technique

- [ ] Support US GAAP / IFRS (beyond French GAAP)
- [ ] OCR pour PDFs scannés (Mistral API fallback)
- [ ] Time-series analysis (historique 3-5 ans)
- [ ] Comparable search automatique (Infogreffe, APIs)
- [ ] Export rapport DD en Excel/PDF formaté
- [ ] Dashboard Streamlit pour monitoring portfolio

---

**Dernière mise à jour:** 2025-01-17
