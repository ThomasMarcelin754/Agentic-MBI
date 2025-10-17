# Dexter — Agent MBI/Rollup Analyst 🤖

Agent autonome d'analyse financière pour **Management Buy-In** et stratégies **Buy & Build** sur PME françaises.

Dexter automatise la due diligence d'acquisition : extraction FEC, normalisation EBITDA (French GAAP), scoring des 4 piliers opérationnels, détection de red flags, et valorisation par multiples sectoriels.

**Mission :** Analyser 100+ cibles/an avec la rigueur d'un analyste M&A, en 10x moins de temps.

## 🚀 Quick Start

```bash
git clone https://github.com/ThomasMarcelin754/Agentic-MBI.git
cd Agentic-MBI
uv sync

cp env.example .env
# Renseigner : ANTHROPIC_API_KEY=sk-ant-...
```

**Test rapide :**
```bash
uv run dexter-agent
```

```python
# Analyse programmatique
from dexter.tools_mbi import read_fec

result = read_fec(
    fec_path="/path/to/FEC.txt",
    encoding="latin-1",
    separator="|"
)
# → CA, EBITDA, concentration clients, red flags
```

## 🎯 Capacités clés

### 1. Extraction multi-format
- **FEC (priorité)** : Analyse granulaire compte par compte, calculs au jour près
- **PDF comptable** : PyMuPDF + Haiku → données structurées
- **Excel** : Balance, Grand Livre via pandas

### 2. Normalisation EBITDA (French GAAP)
- Rémunération dirigeant excessive (644)
- Amortissements (681), provisions (6815)
- Crédit-bail (612), charges exceptionnelles
- Ajustements avec confiance (High/Medium/Low)

### 3. Scoring thèse MBI (4 piliers /40)
1. Opérations répétitives (automatisables)
2. Revenus récurrents (contrats, MRR)
3. Faible digitalisation (levier transformation)
4. Base clients diversifiée (<30% concentration)

**Seuil GO : ≥28/40**

### 4. Red flags automatiques
- Concentration client/fournisseur >30%
- Déclin structurel marché
- Litiges majeurs, actif immobilier complexe
- Management non retainable

### 5. Valorisation
- **Multiples sectoriels** : 25 secteurs couverts (CVC, IRVE, sécurité...)
- **Ajustement géographique** : coûts Paris vs. régions
- **DCF optionnel** : pour cibles à forte croissance

## 📊 Architecture

**Multi-modèles optimisé :**
- **Claude Sonnet 4.5** : Raisonnement complexe (EBITDA normalization, red flags)
- **Claude Haiku** : Extraction rapide (PDF parsing, screening)

**Coût moyen :** ~1,50 € / cible analysée

```
User Query → Agent → [Haiku: extraction] → [Sonnet: analyse] → Report DD
```

## 📖 Documentation

**Pour approfondir :**

- **[Architecture technique](docs/architecture.md)** : Multi-modèles, tools, schemas Pydantic, extensibilité
- **[Guide due diligence](docs/due_diligence.md)** : 4 piliers, red flags, normalisation EBITDA, workflow J0-J15
- **[Exemples concrets](docs/examples.md)** : Tests FEC réels, extraction PDF, cas d'usage complets

## 🎯 Secteurs couverts

| Secteur | Multiples EV/EBITDA | Rationale |
|---------|---------------------|-----------|
| CVC / maintenance | 6x - 8x - 10x | Services récurrents, fragmentation |
| Sécurité incendie | 7x - 9x - 11x | Réglementation forte, contrats LT |
| IRVE (bornes) | 8x - 11x - 14x | Croissance forte, tech |
| Gestion locative B2B | 8x - 10x - 12x | Revenus très récurrents |
| Diagnostics | 6x - 8x - 10x | Obligatoire, fragmentation |
| Élagage / espaces verts | 4.5x - 6.5x - 8.5x | Saisonnalité forte |

**Total : 25 secteurs** (voir `tools_mbi.py:SECTOR_MULTIPLES`)

## 🛠️ Structure projet

```
Agentic-MBI/
├── src/dexter/
│   ├── agent.py           # Orchestrateur multi-agent
│   ├── tools_mbi.py       # Tools DD (read_fec, normalize_ebitda...)
│   ├── schemas.py         # Pydantic models (TargetCompany, RedFlag...)
│   ├── prompts_mbi.py     # System prompts
│   └── utils/             # CLI, logger
├── docs/
│   ├── architecture.md    # Doc technique
│   ├── due_diligence.md   # Guide métier
│   └── examples.md        # Cas d'usage
└── README.md              # Ce fichier
```

## 🚦 Tests validés

✅ **FEC holding TM Capital** : Extraction 391 jours, calculs au jour près, concordance 100% vs PDF
✅ **PDF Alizé Clim** : PyMuPDF extraction, CA 8.5M€, ROA 22.56%
✅ **Workflow DD complet** : SecurFire (fictif), scoring 33/40, valorisation 10.2M€

## 🗺️ Roadmap

- [ ] Support US GAAP / IFRS complet
- [ ] OCR pour PDFs scannés (Mistral API)
- [ ] Time-series analysis (3-5 ans)
- [ ] API Infogreffe pour enrichissement auto
- [ ] Dashboard Streamlit (monitoring portfolio)
- [ ] Export rapport DD (Excel/PDF formaté)

## 📄 Licence

MIT

---

**Contributeurs :** Thomas Marcelin, Brice (avec Claude Code ⚡)
