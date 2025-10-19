# Dexter — Votre DG Adjoint pour le Rollup 🤖

**Agent IA autonome pour piloter votre stratégie de rollup multi-sectoriel.**

Nous sommes des **investisseurs-opérateurs** qui construisons un groupe industriel pérenne. Dexter nous assiste sur toutes les phases : sourcing, due diligence, valorisation, négociation, intégration, et déploiement tech.

**Statut actuel :** Recherche de la plateforme initiale.

---

## 🎯 Notre Positionnement

**Investisseurs-entrepreneurs, pas fonds d'investissement :**
- Nous investissons ET nous opérons directement
- Vision long terme : excellence opérationnelle durable
- Création de valeur par la transformation, pas le multiple financier
- Implication dans l'intégration et la digitalisation

**Notre conviction :** Les PME françaises vieillissantes à forte récurrence + faible digitalisation = énorme levier de création de valeur par l'excellence opérationnelle.

---

## 💡 Notre Thèse d'Investissement

### Critères Financiers (Qualification)
- **EBITDA/EBE** : 500k€ - 2M€ (critère principal)
- **Valeur d'entreprise** : 5M€ - 20M€
- **Marges** : Saines et démontrées (>10%)
- **CA** : Pas de critère strict (focus profitabilité)

### 4 Piliers Opérationnels (Essentiels)
1. ✅ **Opérations répétitives** → Standardisables, automatisables
2. ✅ **Revenus récurrents** → Contrats, abonnements, missions répétées
3. ✅ **Faible digitalisation** → Fort levier de transformation
4. ✅ **Base clients diversifiée** → Pas de concentration (<30% du CA/client)

### Critères de Marché
- **Marchés fragmentés** : Nombreux acteurs locaux, absence de leader
- **Business vieillissant** : Gestion artisanale, peu de tech
- **Géographie** : Grandes métropoles françaises + agglomérations

### Red Flags (Exclusions)
❌ Déclin structurel du marché
❌ Concentration client/fournisseur >30%
❌ Litiges majeurs (prudhommaux, fiscaux)
❌ Actif immobilier complexe
❌ Management non-retainable

---

## 🏭 Secteurs Explorés

**Services Techniques Bâtiment :** CVC, Sécurité incendie, Ventilation, IRVE, Chaudières, Toiture, Portes, Légionelles, Diagnostics, Entretien

**Services Techniques Spécialisés :** Véhicules lourds, Cuisine pro, GTA, Certifications énergétiques

**Services Extérieurs :** Installations sportives, Balayeuse, Marquage, Élagage, Paysage, Piscines, Photovoltaïque O&M

**Hygiène & Conformité :** 3D (Dératisation-Désinsectisation-Désinfection)

**Services B2B :** Gestion locative, Courtage assurance, Infogérance RH, Clinique esthétique

---

## 🚀 Installation

```bash
git clone https://github.com/ThomasMarcelin754/Agentic-MBI.git
cd Agentic-MBI
uv sync

cp env.example .env
# Renseigner : ANTHROPIC_API_KEY=sk-ant-...
```

**Lancer Dexter :**
```bash
uv run dexter-agent
```

---

## 🤝 Rôle de Dexter

Dexter agit comme votre **directeur général adjoint** :

### Vision d'ensemble
- Maintient la cohérence avec la thèse d'investissement
- Challenge chaque opportunité vs. les 4 piliers
- Identifie les interdépendances entre phases
- Propose des approches structurées

### Deep dive sur demande
- Devient ultra-spécifique et actionnable
- Fournit templates, checklists, exemples concrets
- Quantifie et structure les analyses
- Propose des next steps clairs

**Exemples d'interactions :**
- *"Aide-moi à sourcer des cibles en maintenance CVC sur Lyon"*
- *"Analyse ce bilan et dis-moi si l'EBITDA est normalisé"*
- *"Quelle structure de deal proposer pour cette cible à 8M€ ?"*
- *"Comment automatiser la facturation dans ce secteur ?"*

---

## 📚 Documentation

**Pour approfondir :**

- **[Mission & Capacités](docs/mission.md)** : Rôle de Dexter par phase (sourcing, DD, valo, négo, intégration, tech)
- **[Thèse d'Investissement](docs/thesis.md)** : Critères détaillés, secteurs, scoring, red flags
- **[Workflows Opérationnels](docs/workflow.md)** : Templates et processus concrets par phase

---

## 🛠️ Structure Projet

```
Agentic-MBI/
├── src/dexter/
│   ├── agent.py           # Orchestrateur agent
│   ├── tools_mbi.py       # Tools spécifiques MBI (FEC, extraction, scoring)
│   ├── schemas.py         # Modèles de données
│   ├── prompts_mbi.py     # Prompts système
│   └── utils/             # CLI, logger
├── docs/
│   ├── mission.md         # Rôle et capacités de Dexter
│   ├── thesis.md          # Thèse d'investissement détaillée
│   └── workflow.md        # Workflows opérationnels
└── README.md              # Ce fichier
```

---

## 🎯 Stratégie de Création de Valeur

### 1. Digitalisation & Automatisation (Cœur)
- Back-office centralisé
- Automatisation tâches répétitives
- Gains de productivité mesurables

### 2. Excellence Opérationnelle
- Standardisation des processus
- Mutualisation des supports (finance, RH, IT, juridique, achats)
- Pilotage par la data

### 3. Synergies
- **Commerciales** : Cross-sell, extension géographique
- **Achats** : Pouvoir de négociation fournisseurs
- **Financières** : Accès financement, réinvestissement cash

---

## 📄 Licence

MIT

---

**Fondateurs :** Thomas Marcelin, Brice
**Powered by :** Claude Sonnet 4.5 (raisonnement complexe) + Claude Haiku (extraction rapide)
