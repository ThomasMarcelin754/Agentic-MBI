# Workflows Opérationnels

Templates et processus concrets pour chaque phase du rollup.

---

## 🎯 Phase 1 : Sourcing & Deal Flow

### Workflow Standard

```
1. Définir secteur + géographie cible
   ↓
2. Générer liste 50-100 entreprises (Infogreffe, Pappers)
   ↓
3. Scorer rapidement (EBITDA estimé, fit piliers)
   ↓
4. Sélectionner top 20
   ↓
5. Approche personnalisée (email/LinkedIn/appel)
   ↓
6. Qualifier en 15min (checklist)
   ↓
7. GO → DD complète / NO-GO → Sourcing suivant
```

### Template Email d'Approche

**Objet :** Rencontre autour de [Secteur] à [Ville]

Bonjour [Prénom],

Je suis [Votre Nom], investisseur-entrepreneur spécialisé dans les services techniques aux entreprises et collectivités.

J'ai identifié votre société [Nom Société] comme un acteur de référence en [Secteur] sur [Géographie]. Je suis particulièrement intéressé par votre expertise en [spécificité].

Nous construisons un groupe industriel pérenne dans ce domaine, avec une forte orientation digitalisation et excellence opérationnelle.

Seriez-vous ouvert à une rencontre informelle autour d'un café pour échanger sur nos approches respectives ?

Bien cordialement,
[Signature]

### Checklist Qualification 15min

**Critères Financiers**
- [ ] CA >2M€ ?
- [ ] EBITDA estimé 500k€-2M€ ?
- [ ] Marges >10% ?
- [ ] Croissance stable ou positive ?

**4 Piliers**
- [ ] Opérations répétitives ? (standardisables)
- [ ] Revenus récurrents >60% ?
- [ ] Digitalisation faible ? (Excel/papier)
- [ ] Base clients diversifiée ? (<30% concentration)

**Red Flags**
- [ ] Déclin marché ?
- [ ] Concentration client >30% ?
- [ ] Litiges majeurs ?
- [ ] Management non-retainable ?

**Décision**
- **4/4 piliers OK + 0 red flag** → GO DD
- **3/4 piliers OK + 0 red flag** → MAYBE (creuser)
- **<3/4 piliers OU 1+ red flag** → NO-GO

---

## 🔍 Phase 2 : Due Diligence

### Workflow DD Complète (J0 - J15)

#### J0-J2 : Collecte Documents

**Priorité P0 (bloquant) :**
- [ ] FEC (Fichier Écritures Comptables) 3 derniers exercices
- [ ] Liasse fiscale 3 ans
- [ ] Situation intermédiaire N (si N pas clos)
- [ ] Liste clients + CA par client
- [ ] Organigramme + fiches de poste

**Priorité P1 (important) :**
- [ ] Grand Livre détaillé
- [ ] Balance âgée clients/fournisseurs
- [ ] Top 20 contrats clients
- [ ] Contrats cadres fournisseurs
- [ ] Statuts société + pacte actionnaires

**Priorité P2 (nice-to-have) :**
- [ ] Process opérationnels documentés
- [ ] KPIs opérationnels
- [ ] Historique IRP / climat social
- [ ] Liste actifs (véhicules, matériel)

#### J3-J5 : Analyse Financière

**Checklist :**
- [ ] Lire FEC avec tool read_fec()
- [ ] Extraire : CA, EBITDA, concentration clients, red flags
- [ ] Normaliser EBITDA (retraitements compte 644, 681, 6815, 67X)
- [ ] Analyser marges par année (tendance)
- [ ] Calculer BFR moyen et évolution
- [ ] Vérifier dette nette / EBITDA (<3x)
- [ ] Identifier éléments exceptionnels (one-offs)

**Livrables :**
- Tableau financier 3 ans (CA, EBITDA normalisé, marges)
- Liste retraitements avec justifications
- Red flags financiers

#### J6-J8 : Analyse Commerciale & Opérationnelle

**Commercial :**
- [ ] Analyser concentration clients (top 5, 10, 20)
- [ ] Calculer taux attrition / renouvellement
- [ ] Reviewer contrats majeurs (durée, résiliation)
- [ ] Identifier risques de dépendance
- [ ] Positionner vs. concurrence

**Opérationnel :**
- [ ] Cartographier processus clés (intervention, facturation, support)
- [ ] Scorer 4 piliers (/40)
- [ ] Identifier quick wins digitaux (app mobile, auto-facturation, CRM)
- [ ] Estimer gains productivité (FTE économisés)
- [ ] Lister synergies avec groupe (si plateforme existante)

**Livrables :**
- Scoring 4 piliers avec commentaires détaillés
- Liste quick wins avec ROI estimé
- Plan synergies quantifiées

#### J9-J12 : Analyse RH & Juridique

**RH :**
- [ ] Analyser organigramme (homme-clé ?)
- [ ] Évaluer management (retainable ?)
- [ ] Vérifier turnover (<20% OK)
- [ ] Identifier compétences critiques
- [ ] Estimer salaire manager de marché (si remplacement dirigeant)

**Juridique (high-level) :**
- [ ] Vérifier statuts, capital, actionnariat
- [ ] Identifier litiges en cours (annexe comptes)
- [ ] Checker dettes fiscales/URSSAF
- [ ] Lister garanties/cautions dirigeant

**Livrables :**
- Évaluation management (GO/NO-GO rétention)
- Liste litiges avec impact estimé

#### J13-J15 : Synthèse & Recommandation

**Rapport DD Final :**
1. **Executive Summary** (2 pages)
   - GO / MAYBE / NO-GO
   - Rationale en 5 bullets
   - Prix cible et structure deal

2. **Analyse Financière** (5 pages)
   - Historique 3 ans
   - EBITDA normalisé
   - Marges, croissance, BFR

3. **Scoring 4 Piliers** (3 pages)
   - Score détaillé /40
   - Fit thèse

4. **Red Flags** (2 pages)
   - Liste priorisée (Critical / High / Medium)
   - Impact / mitigation

5. **Valorisation** (3 pages)
   - Fourchette EV
   - Prix cible
   - Structure deal proposée

6. **Next Steps** (1 page)
   - Actions J+15 à J+30
   - DD approfondie (legal, tech)
   - Timeline closing

---

## 💰 Phase 3 : Valorisation & Deal Structuring

### Workflow Valorisation

#### Étape 1 : EBITDA Normalisé (référence)
Base de calcul = EBITDA après tous retraitements.

#### Étape 2 : Valorisation par Multiples
**Approche :**
- Identifier secteur cible (CVC, 3D, diagnostics...)
- Benchmarker multiples du secteur (sources : transactions comparables, bases M&A)
- Ajuster multiple selon :
  - Récurrence (>80% → +0.5x à +1x)
  - Marges (>15% → +0.5x)
  - Digitalisation (faible = potentiel → +0.5x)
  - Croissance (>10%/an → +1x)
  - Concentration clients (>30% → -1x)

**Formule :**
```
EV = EBITDA normalisé × Multiple ajusté
```

#### Étape 3 : DCF (optionnel)
**Quand l'utiliser :**
- Cible à forte croissance prévisible
- Capex et BFR structurés
- Visibilité >3 ans

**Paramètres :**
- WACC : 10-12% (PME non cotée)
- Taux perpétuel : 2%
- Projection 5 ans

**Limite :** Forte sensibilité hypothèses. Préférer multiples pour PME.

#### Étape 4 : Fourchette de Prix
- **EV Low** : Multiple bas × EBITDA normalisé
- **EV Mid** : Multiple mid × EBITDA normalisé
- **EV High** : Multiple haut × EBITDA normalisé

#### Étape 5 : Prix Cible
Définir 3 niveaux :
- **Walk-away** : Prix max absolu (on passe si au-dessus)
- **Target** : Prix cible (offre initiale)
- **Stretch** : Prix limite acceptable (si fort rationale)

### Structure de Deal Types

#### Structure 1 : Full Cash
**Quand :** Vendeur veut liquider rapidement, pas de risque EBITDA futur.

```
EV Total : 8M€
Cash at closing : 8M€
Earn-out : 0€
```

**Avantages :** Simple, rapide.
**Inconvénients :** Pas d'alignement post-closing, risque si EBITDA non maintenu.

#### Structure 2 : Cash + Earn-Out
**Quand :** Incertitude sur maintien EBITDA, vendeur reste impliqué 1-2 ans.

```
EV Total : 8M€
Cash at closing : 6M€ (75%)
Earn-out 2 ans : 2M€ (si EBITDA ≥ seuil)
```

**Conditions Earn-Out :**
- EBITDA moyen 2 ans ≥ 1M€ → 100% earn-out
- EBITDA moyen 2 ans 900k€-1M€ → 50% earn-out
- EBITDA moyen 2 ans <900k€ → 0 earn-out

**Avantages :** Alignement intérêts, réduction risque.
**Inconvénients :** Complexité suivi, potentiel conflit.

#### Structure 3 : Cash + Vendor Loan
**Quand :** Optimiser financement, vendeur accepte paiement différé.

```
EV Total : 8M€
Cash at closing : 5M€
Vendor loan : 3M€ (remboursement 3-5 ans, taux 3-5%)
```

**Avantages :** Réduit equity / dette bancaire nécessaire.
**Inconvénients :** Vendeur reste créancier.

#### Structure 4 : Equity Rollover
**Quand :** Vendeur garde une participation minoritaire (co-investissement).

```
EV Total : 8M€
Cash : 6M€
Equity rollover : 2M€ (vendeur garde 20%)
```

**Avantages :** Alignement fort, vendeur impliqué croissance.
**Inconvénients :** Vendeur reste actionnaire (gouvernance).

---

## 🤝 Phase 4 : Négociation & Closing

### Workflow Négociation

#### Étape 1 : Préparer Stratégie
**Définir :**
- Walk-away price : [X]M€
- Target price : [Y]M€
- Stretch price : [Z]M€

**Identifier leviers :**
- Structure (cash vs. earn-out)
- Conditions suspensives
- Garanties & warranties
- Management retention
- Timeline closing

#### Étape 2 : Première Offre (LOI)
**Contenu LOI :**
- Prix proposé (fourchette ou ferme)
- Structure (cash, earn-out, vendor loan)
- Conditions suspensives (DD approfondie, financement)
- Exclusivité (60-90 jours)
- Timeline closing (3-6 mois)

**Ton :** Ferme mais respectueux. Montrer sérieux et capacité à closer.

#### Étape 3 : Négociation
**Objections Vendeur Types :**

**"Prix trop bas"**
→ Argumentaire :
- Basé sur EBITDA normalisé (retraitements justifiés)
- Multiples de marché (comps sectoriels)
- Risques identifiés (concentration, digitalisation à faire)
- Earn-out pour partager upside

**"Je veux tout cash"**
→ Argumentaire :
- Earn-out = alignement intérêts (vous voulez que ça marche)
- Réduit risque pour nous (EBITDA à maintenir)
- Partage upside si surperformance

**"Timeline trop longue"**
→ Solutions :
- Accélérer DD (mobiliser ressources)
- Simplifier conditions suspensives
- Pre-financement validé

#### Étape 4 : Closing
**Checklist Closing :**
- [ ] LOI signée
- [ ] DD approfondie terminée (legal, fiscal, environnemental)
- [ ] Financement sécurisé (equity + dette)
- [ ] SPA négocié et signé
- [ ] Garanties / Warranties définies
- [ ] Conditions suspensives levées
- [ ] Closing call organisé
- [ ] Virement effectué
- [ ] Registre commerce mis à jour

**Timeline Type :**
- LOI signée : J0
- DD approfondie : J0 → J60
- Négociation SPA : J30 → J75
- Levée conditions suspensives : J75 → J90
- Closing : J90

---

## 🔧 Phase 5 : Intégration (Plan 100 Jours)

### J0 - J30 : Stabilisation

**Priorités :**
- [ ] Rencontre équipe (management + techniciens)
- [ ] Communication clients (continuité, pas de rupture)
- [ ] Sécuriser process critiques (facturation, paie, achats)
- [ ] Identifier quick wins (gains rapides <3 mois)
- [ ] Confirmer organigramme et responsabilités

**Quick Wins Types :**
- Renégocier contrats fournisseurs (pouvoir achat groupe)
- Automatiser relances clients (cash immédiat)
- Optimiser stocks (réduction BFR)
- Digitaliser planning (productivité techniciens)

### J31 - J60 : Intégration Supports

**Fonctions à Intégrer :**
- [ ] **Finance** : Reporting groupe, consolidation, trésorerie centralisée
- [ ] **RH** : Paie, contrats, SIRH commun
- [ ] **IT** : Messagerie, Wi-Fi, licences logiciels
- [ ] **Juridique** : Contrats, assurances groupe
- [ ] **Achats** : Contrats cadres, centrales d'achat

**Livrables :**
- Reporting mensuel consolidé (KPIs groupe)
- Dashboard financier temps réel
- Process standardisés documentés

### J61 - J100 : Transformation

**Chantiers Digitaux :**
- [ ] Déployer app mobile techniciens
- [ ] Automatiser facturation (contrats → factures auto)
- [ ] Intégrer CRM clients (relances, up-sell, NPS)
- [ ] Mettre en place dashboards opérationnels

**Synergies :**
- [ ] Cross-sell clients (si multi-secteurs)
- [ ] Mutualisation véhicules / matériel
- [ ] Formation croisée équipes
- [ ] Harmonisation tarifs

**Tracking :**
- Synergies réalisées vs. plan
- KPIs opérationnels (productivité, NPS, attrition)
- EBITDA post-intégration vs. baseline

---

## 💻 Phase 6 : Back-Office Tech Platform

### Workflow Déploiement Tech

#### Étape 1 : Définir Architecture Cible

**Modules Essentiels :**

| Module | Fonction | Build vs Buy |
|--------|----------|--------------|
| **Finance** | Compta, reporting, conso | Buy (ERP cloud) |
| **RH** | Paie, contrats, temps | Buy (SIRH SaaS) |
| **CRM** | Clients, pipeline, support | Buy (CRM cloud) |
| **Ops** | Planning, intervention, mobile | Buy + Custom |
| **Achats** | Fournisseurs, contrats, appro | Buy (module ERP) |
| **Analytics** | Dashboards, KPIs, BI | Buy (Tableau, Power BI) |

#### Étape 2 : Sélection Vendors

**Critères :**
- Cloud SaaS (pas on-premise)
- Scalable (croissance groupe)
- Intégrations API (connectivité)
- Prix raisonnable (coût/utilisateur)
- Support français

**Benchmarks :**
- **ERP** : Odoo, Sage, Cegid, QuickBooks
- **SIRH** : PayFit, Lucca, Factorial
- **CRM** : HubSpot, Pipedrive, Salesforce (si budget)
- **Planning Techniciens** : Praxedo, Synchroteam, FieldWire
- **BI** : Metabase (open-source), Power BI, Tableau

#### Étape 3 : Automatisations Prioritaires

**Top 5 Automatisations (ROI rapide) :**

1. **Auto-facturation**
   - Contrats → Factures générées automatiquement
   - Gain : 1-2 FTE admin

2. **Relances Clients**
   - Emails automatiques J+15, J+30, J+45
   - Gain : Réduction DSO de 10-15 jours

3. **Planning Techniciens**
   - App mobile : géoloc, feuilles de route, signatures
   - Gain : +10% productivité terrain

4. **Dashboards Temps Réel**
   - KPIs : CA, marge, DSO, productivité, NPS
   - Gain : Pilotage réactif

5. **CRM Automatisé**
   - Relances renouvellement auto
   - Up-sell triggers
   - Gain : +5-10% CA récurrent

#### Étape 4 : Roadmap 12-24 Mois

**Phase 1 (0-6 mois) : Fondations**
- Déployer ERP cloud (finance, achats)
- Déployer SIRH (paie, temps)
- Migrer emails / messagerie groupe

**Phase 2 (6-12 mois) : Digitalisation Ops**
- App mobile techniciens
- CRM clients
- Auto-facturation
- Dashboards KPIs

**Phase 3 (12-24 mois) : Optimisation**
- BI avancée (prédictions, alertes)
- Automatisations avancées (workflows)
- Intégrations poussées (API, ETL)

---

## 📊 Templates & Checklists

### Template Rapport DD (Structure)

```markdown
# Due Diligence - [Nom Cible]

## Executive Summary
- **Recommandation** : GO / MAYBE / NO-GO
- **Prix cible** : [X]M€
- **Structure** : [Cash / Earn-out / Vendor loan]
- **Rationale** : [5 bullets]

## 1. Présentation Cible
- Secteur, géographie, historique
- Business model
- Positionnement concurrentiel

## 2. Analyse Financière
- Historique 3 ans (CA, EBITDA, marges)
- EBITDA normalisé (retraitements)
- BFR, dette, cash

## 3. Scoring 4 Piliers
- Pilier 1 : [X/10]
- Pilier 2 : [X/10]
- Pilier 3 : [X/10]
- Pilier 4 : [X/10]
- **Total : [X/40]**

## 4. Red Flags
- Liste priorisée (Critical / High / Medium)
- Impact / Mitigation

## 5. Valorisation
- Fourchette EV
- Prix cible
- Structure deal

## 6. Plan Intégration (high-level)
- Quick wins
- Synergies
- Timeline

## 7. Next Steps
- Actions J+15 → J+30
- Timeline closing
```

### Checklist 100 Jours (Condensée)

**J0-J30 : Stabilisation**
- [ ] Rencontre équipe complète
- [ ] Communication clients
- [ ] Sécuriser process critiques
- [ ] 3 quick wins identifiés et lancés

**J31-J60 : Intégration Supports**
- [ ] Finance intégrée (reporting groupe)
- [ ] RH intégrée (paie groupe)
- [ ] IT intégrée (outils communs)

**J61-J100 : Transformation**
- [ ] App mobile techniciens déployée
- [ ] Auto-facturation activée
- [ ] CRM clients opérationnel
- [ ] Dashboards KPIs en place

---

**Dernière mise à jour :** 2025-01-17
