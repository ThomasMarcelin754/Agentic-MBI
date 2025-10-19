# Documentation Technique

Guide technique pour comprendre et étendre Dexter.

---

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────┐
│  User Query (via CLI ou Python)         │
└──────────────┬──────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Agent Orchestrator   │
    │  (src/dexter/agent.py)│
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
    │   Raisonnement    │   Extraction     │
    │   - EBITDA norm   │   - PDF parsing  │
    │   - Red flags     │   - Quick screen │
    │   - Scoring       │   - Validation   │
    └───────────────────┴──────────────────┘
               │
               ▼
    ┌──────────────────────────────────────┐
    │           Tool Suite                  │
    │  - read_fec (FEC analysis)            │
    │  - normalize_ebitda                   │
    │  - score_four_pillars                 │
    │  - detect_red_flags                   │
    │  - value_target                       │
    └───────────────────────────────────────┘
```

---

## 🤖 Modèles IA

### Claude Sonnet 4.5
**Model ID:** `claude-sonnet-4-20250514`

**Usage :** Raisonnement complexe, jugement qualitatif
- Normalisation EBITDA (identifier retraitements non évidents)
- Détection red flags (signaux faibles)
- Scoring 4 piliers (analyse qualitative)
- Valorisation (ajustements multiples selon qualité)

**Coût :** ~$15/1M tokens input, ~$75/1M tokens output

### Claude Haiku
**Model ID:** `claude-3-haiku-20240307`

**Usage :** Extraction rapide, tâches structurées
- Extraction texte PDF (comptes, IMs)
- Parsing tableaux
- Quick screening (filtrage leads)
- Validation données

**Coût :** ~$0.80/1M tokens input, ~$4/1M tokens output

### Stratégie de routage
```python
# Dans model.py
if task_type in ["extract", "parse", "screen", "validate"]:
    model = "claude-3-haiku-20240307"  # Rapide, pas cher
else:
    model = "claude-sonnet-4-20250514"  # Raisonnement complexe
```

**Ratio optimal :** 30% Haiku / 70% Sonnet
- Haiku : Extraction/parsing (30% tokens)
- Sonnet : Analyse/décision (70% tokens)

**Coût moyen par cible analysée :** ~1.50€

---

## 🛠️ Tools Disponibles

### 1. read_fec()
**Fichier :** `src/dexter/tools_mbi.py`

**Signature :**
```python
def read_fec(fec_path: str, encoding: str = "latin-1", separator: str = "|") -> Dict
```

**Input :**
- `fec_path` : Chemin vers fichier FEC (.txt)
- `encoding` : Encodage (latin-1, utf-8, cp1252)
- `separator` : Séparateur (| ou ; ou \t)

**Output :**
```python
{
    "success": True,
    "total_entries": 197,
    "date_range": {
        "start": "2023-12-06",
        "end": "2024-12-31",
        "nb_days": 391,
        "is_full_year": False
    },
    "financials": {
        "total_revenue": 14560.69,
        "total_revenue_annualized": 13601.77,  # Si <365j
        "total_expenses": 14986.83,
        "result_before_tax": -426.14,
        "owner_compensation_644": 0.0,
        "depreciation_681": 0.0,
        "provisions_6815": 0.0,
        "ebitda_proxy": -426.14,
        "ebitda_margin_pct": -2.93
    },
    "concentration": {
        "top_client_concentration_pct": 0.0,
        "top_5_clients": {},
        "client_risk": "LOW"
    },
    "seasonality": {
        "coefficient_variation": 0.0,
        "high_seasonality": False
    },
    "red_flags": [
        {
            "type": "Résultat déficitaire",
            "severity": "High",
            "description": "Perte de 426.14 €"
        }
    ]
}
```

**Logique interne :**
- Parse FEC avec pandas
- Calcule nb jours exact (annualisation si <365)
- Map Plan Comptable Général (PCG) :
  - Classe 7 → Produits
  - Classe 6 → Charges
  - 644 → Rémunération exploitant
  - 681 → Amortissements
  - 411XXX → Clients
  - 401XXX → Fournisseurs
- Détecte red flags automatiquement

**Cas d'usage :**
```python
from dexter.tools_mbi import read_fec

result = read_fec(
    fec_path="/path/to/FEC.txt",
    encoding="utf-8",
    separator="\t"
)

if result["concentration"]["client_risk"] == "HIGH":
    print("⚠️ Concentration client >30%")
```

---

### 2. normalize_ebitda()
**Fichier :** `src/dexter/tools_mbi.py`

**Signature :**
```python
def normalize_ebitda(
    target: TargetCompany,
    financials: FinancialMetrics,
    im_text: Optional[str] = None
) -> List[EBITDAAdjustment]
```

**Input :**
- `target` : TargetCompany (nom, secteur, accounting_standard)
- `financials` : FinancialMetrics (revenue, ebitda_reported...)
- `im_text` : Texte IM (optionnel, pour contexte)

**Output :**
```python
[
    {
        "category": "Rémunération dirigeant",
        "amount": 70000.0,  # Positif = add-back EBITDA
        "description": "Dirigeant 150k€ vs. manager marché 80k€",
        "source": "Compte 644",
        "confidence": "High"
    },
    {
        "category": "Amortissements",
        "amount": 80000.0,
        "description": "Add-back standard (définition EBITDA)",
        "source": "Compte 681",
        "confidence": "High"
    }
]
```

**Retraitements French GAAP :**
- Compte 644 : Rémunération exploitant excessive
- Compte 681 : Amortissements (add-back systématique)
- Compte 6815 : Provisions exploitation
- Compte 612 : Crédit-bail (si comparaison IFRS)
- Compte 67X : Charges exceptionnelles
- Charges personnelles (véhicule, logement)

**Modèle utilisé :** Sonnet 4.5 (jugement qualitatif)

---

### 3. score_four_pillars()
**Fichier :** `src/dexter/tools_mbi.py`

**Signature :**
```python
def score_four_pillars(
    target: TargetCompany,
    business_description: str
) -> FourPillarsScore
```

**Input :**
- `target` : TargetCompany
- `business_description` : Description détaillée business model

**Output :**
```python
{
    "repetitive_operations": 8,      # /10
    "recurring_revenue": 9,          # /10
    "low_digitalization": 7,         # /10
    "diversified_client_base": 6,    # /10
    "total_score": 30,               # /40
    "comments": "Détails par pilier..."
}
```

**Seuils de décision :**
- ≥32/40 : STRONG GO
- 28-31/40 : GO
- 24-27/40 : MAYBE
- <24/40 : NO-GO

**Modèle utilisé :** Sonnet 4.5

---

### 4. detect_red_flags()
**Fichier :** `src/dexter/tools_mbi.py`

**Signature :**
```python
def detect_red_flags(
    target: TargetCompany,
    financials: FinancialMetrics,
    im_text: Optional[str] = None
) -> List[RedFlag]
```

**Output :**
```python
[
    {
        "category": "Concentration client",
        "severity": "High",
        "description": "Top 5 = 45% CA",
        "is_deal_breaker": True
    }
]
```

**Red flags détectés :**
- Concentration client >30%
- Concentration fournisseur
- Déclin structurel (analyse CA tendance)
- Résultat déficitaire
- Litiges majeurs (si mentionnés dans IM)

**Modèle utilisé :** Sonnet 4.5

---

### 5. value_target()
**Fichier :** `src/dexter/tools_mbi.py`

**Signature :**
```python
def value_target(
    target: TargetCompany,
    ebitda_normalized: float
) -> Valuation
```

**Input :**
- `target` : TargetCompany (secteur, géographie)
- `ebitda_normalized` : EBITDA normalisé (€)

**Output :**
```python
{
    "target_name": "Société X",
    "ebitda_normalized": 1000000.0,
    "ev_ebitda_low": 6.0,
    "ev_ebitda_mid": 8.0,
    "ev_ebitda_high": 10.0,
    "enterprise_value_low": 6000000.0,
    "enterprise_value_mid": 8000000.0,
    "enterprise_value_high": 10000000.0,
    "comparables": []
}
```

**Logique :**
- Lookup secteur dans `SECTOR_MULTIPLES` dict
- Ajustement géographique (optionnel)
- Calcul EV = EBITDA × Multiple

**Note :** Multiples sectoriels à définir (actuellement placeholders, voir `tools_mbi.py:SECTOR_MULTIPLES`)

---

## 📊 Schemas Pydantic

**Fichier :** `src/dexter/schemas.py`

### TargetCompany
```python
class TargetCompany(BaseModel):
    name: str
    sector: Sector  # Literal["CVC", "IRVE", ...]
    geography: Geography  # Literal["Paris", "Lyon", ...]
    accounting_standard: AccountingStandard  # "French GAAP" / "IFRS" / "US GAAP"
    founded_year: Optional[int]
```

### FinancialMetrics
```python
class FinancialMetrics(BaseModel):
    revenue: float
    ebitda_reported: float
    ebitda_normalized: Optional[float]
    net_income: Optional[float]
    total_assets: Optional[float]
    total_debt: Optional[float]
    cash: Optional[float]
    period_end: date
    period_type: Literal["annual", "quarterly", "ttm"]
```

### EBITDAAdjustment
```python
class EBITDAAdjustment(BaseModel):
    category: Literal[
        "Non-récurrent", "Rémunération dirigeant", "Loyers",
        "Provisions", "Amortissements", "Charges personnelles",
        "Syndic", "Autres"
    ]
    amount: float  # Positif = add-back EBITDA
    description: str
    source: str  # "Compte 644", "Annexe IM", etc.
    confidence: Literal["High", "Medium", "Low"]
```

### FourPillarsScore
```python
class FourPillarsScore(BaseModel):
    repetitive_operations: int  # 0-10
    recurring_revenue: int      # 0-10
    low_digitalization: int     # 0-10
    diversified_client_base: int # 0-10
    total_score: int            # 0-40
    comments: str
```

### RedFlag
```python
class RedFlag(BaseModel):
    category: Literal[
        "Déclin structurel", "Concentration client",
        "Concentration fournisseur", "Litiges",
        "Actif immobilier", "Réglementation",
        "Management", "Autre"
    ]
    severity: Literal["Critical", "High", "Medium", "Low"]
    description: str
    is_deal_breaker: bool
```

### Valuation
```python
class Valuation(BaseModel):
    target_name: str
    ebitda_normalized: float
    ev_ebitda_low: float
    ev_ebitda_mid: float
    ev_ebitda_high: float
    enterprise_value_low: float
    enterprise_value_mid: float
    enterprise_value_high: float
    comparables: List[Comparable]
    dcf_value: Optional[float]
```

---

## 🗂️ Plan Comptable Général (PCG)

**Fichier :** `src/dexter/tools_mbi.py:PCG_ACCOUNTS`

### Classes Principales

**Classe 6 : Charges**
- 601-607 : Achats
- 611 : Sous-traitance
- 612 : Crédit-bail (key pour normalization)
- 621-628 : Personnel
- 641 : Salaires
- 644 : Rémunération exploitant (KEY pour EBITDA)
- 681 : Amortissements (add-back EBITDA)
- 6815 : Provisions exploitation (add-back EBITDA)

**Classe 7 : Produits**
- 701 : Ventes produits finis
- 703 : Ventes marchandises
- 706 : Prestations de services

**Classe 4 : Tiers**
- 411XXX : Clients individuels (concentration)
- 401XXX : Fournisseurs individuels

**Classe 67/77 : Exceptionnel**
- 671 : Charges exceptionnelles (normalisation)
- 771 : Produits exceptionnels

---

## 🔧 Comment Étendre

### Ajouter un Nouveau Secteur

**Fichier :** `src/dexter/schemas.py`

1. Ajouter secteur à l'enum :
```python
Sector = Literal[
    "CVC", "IRVE", "Diagnostics",
    "Nouveau Secteur",  # ← Ajouter ici
    "Autre"
]
```

2. (Optionnel) Ajouter multiples dans `tools_mbi.py` :
```python
SECTOR_MULTIPLES = {
    # ...
    "Nouveau Secteur": {
        "low": 5.0,
        "mid": 7.0,
        "high": 9.0,
        "rationale": "Justification"
    }
}
```

### Ajouter un Nouveau Tool

**Fichier :** `src/dexter/tools_mbi.py`

1. Définir input schema :
```python
class NewToolInput(BaseModel):
    param1: str = Field(..., description="Description param1")
    param2: int = Field(..., description="Description param2")
```

2. Créer tool :
```python
@tool(args_schema=NewToolInput)
def new_tool(param1: str, param2: int) -> Dict:
    """
    Description du tool.

    Args:
        param1: ...
        param2: ...

    Returns:
        Dict avec résultats
    """
    # Logique
    result = {"output": "..."}
    return result
```

3. Ajouter à la liste :
```python
MBI_TOOLS = [
    read_fec,
    normalize_ebitda,
    # ...
    new_tool  # ← Ajouter ici
]
```

### Ajouter un Nouveau Retraitement EBITDA

**Fichier :** `src/dexter/tools_mbi.py:normalize_ebitda()`

Ajouter dans la logique :
```python
# Nouveau retraitement
if target.accounting_standard == "French GAAP":
    adjustments_to_check.append(
        "Nouveau type de charge à retraiter"
    )
```

Ajouter catégorie dans schema :
```python
# src/dexter/schemas.py
class EBITDAAdjustment(BaseModel):
    category: Literal[
        "Non-récurrent", "Rémunération dirigeant",
        "Nouvelle Catégorie",  # ← Ajouter
        "Autres"
    ]
```

---

## 🧪 Tests & Validation

### Tester read_fec()

```python
from dexter.tools_mbi import read_fec

# Test avec FEC réel
result = read_fec(
    fec_path="/path/to/test_fec.txt",
    encoding="utf-8",
    separator="\t"
)

# Validations
assert result["success"] == True
assert result["financials"]["total_revenue"] > 0
assert "red_flags" in result
```

### Tester avec FEC holding TM Capital (validé)

**Données attendues :**
- Total produits : 14 560,69 €
- Total charges : 14 986,83 €
- Résultat : -426,14 €
- Période : 391 jours (pas 365)
- Concentration client : 0% (holding)

**Test de cohérence FEC vs PDF :**
- ✅ 100% de concordance validée

---

## 📦 Dépendances Techniques

**Fichier :** `pyproject.toml`

### Core
- `anthropic` : API Claude (Sonnet, Haiku)
- `langchain` : Orchestration agent + tools
- `pydantic` : Validation schémas

### Data Processing
- `pandas` : Analyse FEC, données tabulaires
- `openpyxl` : Lecture Excel
- `pymupdf` (fitz) : Extraction PDF
- `pdfplumber` : Alternative extraction PDF

### Utils
- `python-dotenv` : Variables d'environnement
- `rich` : CLI formatting

---

## 🚀 Performance & Optimisation

### Coûts par Analyse

**Analyse DD complète (1 cible) :**
- FEC : 200 écritures → ~5k tokens
- IM PDF : 50 pages → ~30k tokens
- Total : ~50k tokens input, ~5k tokens output

**Breakdown :**
- Haiku (extraction) : ~$0.04
- Sonnet (analyse) : ~$1.50
- **Total : ~$1.54 / cible**

### Optimisations Possibles

1. **Cache FEC parsé**
```python
# Éviter re-parsing si même fichier
import functools

@functools.lru_cache(maxsize=10)
def read_fec_cached(fec_path: str):
    return read_fec(fec_path)
```

2. **Batch processing comparables**
```python
# Analyser 10 cibles en parallèle
targets = [target1, target2, ...]
results = asyncio.gather(*[analyze(t) for t in targets])
```

3. **Haiku pour screening initial**
```python
# Filtrer 100 leads → garder top 20 pour Sonnet
quick_scores = [haiku_screen(lead) for lead in leads]
top_20 = sorted(quick_scores)[:20]
detailed_dd = [sonnet_analyze(t) for t in top_20]
```

---

## 🔐 Sécurité & Validation

### Human-in-the-Loop

Tous les rapports DD ont `requires_human_validation: bool = True` par défaut.

**Pas d'automatisation complète :** L'humain valide toujours avant action.

### Traçabilité

- Tous ajustements EBITDA avec `source` + `confidence`
- Red flags avec `severity` + `is_deal_breaker`
- Logs détaillés (utils/logger.py)

### Limites Connues

**EBITDA normalization :**
- ⚠️ Nécessite validation expert-comptable
- ⚠️ Jugement qualitatif (Sonnet peut se tromper)

**Multiples sectoriels :**
- ⚠️ À définir avec vraies sources (pas d'inventions)
- ⚠️ Mise à jour annuelle nécessaire

**Red flags :**
- ⚠️ Détection par patterns (pas exhaustif)
- ⚠️ Faux positifs possibles

---

## 📁 Structure Code

```
src/dexter/
├── agent.py              # Orchestrateur agent
├── model.py              # Routage Sonnet/Haiku
├── tools.py              # Tools génériques (base Dexter)
├── tools_mbi.py          # Tools spécifiques MBI ⭐
├── schemas.py            # Pydantic models ⭐
├── prompts_mbi.py        # System prompts
├── cli.py                # Interface CLI
└── utils/
    ├── logger.py         # Logging
    └── ui.py             # UI CLI
```

**Fichiers clés pour MBI :**
- `tools_mbi.py` : Tous les tools (read_fec, normalize_ebitda...)
- `schemas.py` : Structures de données
- `prompts_mbi.py` : Prompts système

---

## 🛣️ Roadmap Technique

### Court terme (Q1 2025)
- [ ] Finaliser multiples sectoriels (sources réelles)
- [ ] Ajouter tests unitaires (pytest)
- [ ] Améliorer parsing PDF (tableaux complexes)

### Moyen terme (Q2-Q3 2025)
- [ ] Support US GAAP / IFRS complet
- [ ] OCR pour PDFs scannés (Mistral API)
- [ ] Time-series analysis (3-5 ans historique)
- [ ] Export rapport DD (Excel/PDF formaté)

### Long terme (2026)
- [ ] API Infogreffe pour enrichissement auto
- [ ] Comparable search automatique
- [ ] Dashboard Streamlit (monitoring portfolio)
- [ ] ML pour prédiction scoring piliers

---

**Dernière mise à jour :** 2025-01-17
