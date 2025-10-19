"""
MBI/Rollup specific tools for due diligence and analysis.
Includes accounting system mapping and sector-specific adjustments.
"""

from langchain.tools import tool
from typing import List, Dict, Optional, Literal
import os
import pandas as pd
import requests
from pydantic import BaseModel, Field

from dexter.schemas import (
    TargetCompany, FinancialMetrics, EBITDAAdjustment,
    FourPillarsScore, RedFlag, Valuation, Comparable,
    Sector, Geography, AccountingStandard
)

# ========== Accounting System Mapping ==========

ACCOUNTING_MAPPINGS = {
    "French GAAP": {
        "revenue_line": ["Chiffre d'affaires", "Ventes", "Produits d'exploitation"],
        "ebitda_calculation": "excedent_brut_exploitation",  # EBE in French GAAP
        "depreciation": ["Dotations aux amortissements"],
        "provisions": ["Dotations aux provisions"],
        "interest": ["Charges financières", "Produits financiers"],
        "tax": ["Impôt sur les bénéfices"],
        "rental_leases": "off_balance_sheet",  # Crédit-bail hors bilan
        "specific_adjustments": ["Provisions réglementées", "Subventions d'exploitation"]
    },
    "US GAAP": {
        "revenue_line": ["Revenue", "Net Sales", "Operating Revenue"],
        "ebitda_calculation": "operating_income_plus_da",
        "depreciation": ["Depreciation", "Amortization"],
        "provisions": ["Provisions", "Allowances"],
        "interest": ["Interest Expense", "Interest Income"],
        "tax": ["Income Tax Expense"],
        "rental_leases": "on_balance_sheet_if_capital",  # ASC 842
        "specific_adjustments": ["Stock-based compensation", "Restructuring charges"]
    },
    "IFRS": {
        "revenue_line": ["Revenue", "Operating Income"],
        "ebitda_calculation": "operating_income_plus_da",
        "depreciation": ["Depreciation", "Amortisation"],
        "provisions": ["Provisions"],
        "interest": ["Finance Costs", "Finance Income"],
        "tax": ["Income Tax"],
        "rental_leases": "on_balance_sheet",  # IFRS 16 - tous en bilan
        "specific_adjustments": ["Impairment charges", "Fair value adjustments"]
    }
}

# ========== Sector-Specific Multiples ==========

SECTOR_MULTIPLES = {
    "CVC": {"low": 6.0, "mid": 8.0, "high": 10.0, "rationale": "Services récurrents, fragmentation élevée"},
    "Sécurité Incendie": {"low": 7.0, "mid": 9.0, "high": 11.0, "rationale": "Réglementation forte, contrats long-terme"},
    "3D": {"low": 5.5, "mid": 7.5, "high": 9.5, "rationale": "Récurrence moyenne, saisonnalité"},
    "Ventilation": {"low": 6.0, "mid": 8.0, "high": 10.0, "rationale": "Similaire CVC"},
    "IRVE": {"low": 8.0, "mid": 11.0, "high": 14.0, "rationale": "Marché croissance forte"},
    "Chaudières": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Maturité, déclin progressif gaz"},
    "Toiture": {"low": 4.5, "mid": 6.5, "high": 8.5, "rationale": "Cyclique, dépendance météo"},
    "Portes": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Mix installation/maintenance"},
    "Légionelles": {"low": 7.0, "mid": 9.0, "high": 11.0, "rationale": "Réglementation stricte, récurrence"},
    "Diagnostics": {"low": 6.0, "mid": 8.0, "high": 10.0, "rationale": "Obligatoire, fragmentation"},
    "Entretien Bâtiment": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Multi-services, standardisable"},
    "Véhicules Lourds": {"low": 5.5, "mid": 7.5, "high": 9.5, "rationale": "B2B stable, spécialisé"},
    "Cuisine Pro": {"low": 6.0, "mid": 8.0, "high": 10.0, "rationale": "Normes strictes, récurrence"},
    "GTA": {"low": 7.0, "mid": 9.5, "high": 12.0, "rationale": "Tech, contrats long-terme"},
    "Installations Sportives": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Public/privé mix"},
    "Balayeuse": {"low": 4.5, "mid": 6.5, "high": 8.5, "rationale": "Capex élevé, municipal"},
    "Marquage": {"low": 4.0, "mid": 6.0, "high": 8.0, "rationale": "Saisonnalité forte"},
    "Élagage": {"low": 4.5, "mid": 6.5, "high": 8.5, "rationale": "Saisonnalité, risques"},
    "Paysage": {"low": 4.0, "mid": 6.0, "high": 8.0, "rationale": "Fragmentation extrême"},
    "Piscines": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Saisonnalité forte"},
    "Photovoltaïque": {"low": 6.0, "mid": 8.5, "high": 11.0, "rationale": "Croissance, contrats O&M"},
    "Gestion Locative": {"low": 8.0, "mid": 10.0, "high": 12.0, "rationale": "Revenus très récurrents"},
    "Courtage Assurance": {"low": 7.0, "mid": 9.5, "high": 12.0, "rationale": "Commissions récurrentes"},
    "Infogérance RH": {"low": 7.0, "mid": 9.0, "high": 11.0, "rationale": "SaaS-like, récurrence"},
    "Clinique Esthétique": {"low": 6.0, "mid": 8.0, "high": 10.0, "rationale": "B2C premium, fidélité"},
    "Autre": {"low": 5.0, "mid": 7.0, "high": 9.0, "rationale": "Multiple générique PME services"}
}

# ========== Geography-Specific Cost Adjustments ==========

GEOGRAPHY_COST_INDEX = {
    "Paris": 1.30,  # +30% vs baseline
    "Lyon": 1.10,
    "Marseille": 1.05,
    "Toulouse": 1.05,
    "Bordeaux": 1.08,
    "Lille": 1.00,  # Baseline
    "Nantes": 1.05,
    "Strasbourg": 1.05,
    "Nice": 1.15,
    "Montpellier": 1.00,
    "Rennes": 1.03,
    "Grenoble": 1.05,
    "Autre": 1.00
}

# ========== French Plan Comptable Général (PCG) ==========
# Key account ranges for EBITDA normalization and red flag detection

PCG_ACCOUNTS = {
    # Revenue accounts (Class 7)
    "revenue": {
        "701": "Ventes de produits finis",
        "703": "Ventes de marchandises",
        "706": "Prestations de services",
        "708": "Produits des activités annexes",
    },

    # Operating expenses (Class 6) - for EBITDA adjustments
    "operating_expenses": {
        "601-607": "Achats",
        "611": "Sous-traitance générale",
        "612": "Redevances de crédit-bail",  # Key for lease normalization
        "613-614": "Locations et charges locatives",
        "615-616": "Entretien, réparations",
        "621-628": "Personnel",
        "631-637": "Impôts et taxes",
        "641": "Rémunérations du personnel",
        "644": "Rémunération du travail de l'exploitant",  # KEY: Owner compensation
        "645": "Charges de sécurité sociale et de prévoyance",
        "681": "Dotations aux amortissements",  # Add back for EBITDA
        "6815": "Dotations aux provisions d'exploitation",  # Add back for EBITDA
    },

    # Financial accounts
    "financial": {
        "661": "Charges d'intérêts",
        "761": "Produits financiers",
    },

    # Exceptional items (Class 67/77) - for normalization
    "exceptional": {
        "671": "Charges exceptionnelles sur opérations de gestion",
        "771": "Produits exceptionnels sur opérations de gestion",
    },

    # Balance sheet - Assets (Class 2)
    "fixed_assets": {
        "20": "Immobilisations incorporelles",
        "21": "Immobilisations corporelles",
        "23": "Immobilisations en cours",
    },

    # Balance sheet - Liabilities (Class 1, 4)
    "equity_debt": {
        "101": "Capital",
        "106": "Réserves",
        "12": "Résultat de l'exercice",
        "16": "Emprunts et dettes",
        "164": "Emprunts auprès des établissements de crédit",
    },

    # Client accounts (Class 411) - for concentration analysis
    "clients": {
        "411": "Clients",
        "4110-4119999": "Comptes clients individuels",
    },

    # Supplier accounts (Class 401) - for concentration analysis
    "suppliers": {
        "401": "Fournisseurs",
        "4010-4019999": "Comptes fournisseurs individuels",
    },
}

# ========== Tool Input Schemas ==========

class ReadFECInput(BaseModel):
    """Input for reading FEC (Fichier des Écritures Comptables)."""
    fec_path: str = Field(..., description="Path to FEC file (.txt or .csv)")
    encoding: str = Field("latin-1", description="File encoding (latin-1, utf-8, cp1252)")
    separator: str = Field("|", description="Field separator (| or ; or tab)")

class ExtractIMDataInput(BaseModel):
    """Input for extracting data from Information Memorandum."""
    im_text: str = Field(..., description="Full text content of the IM document (extracted by Haiku from PDF)")

class NormalizeEBITDAInput(BaseModel):
    """Input for EBITDA normalization analysis."""
    target: TargetCompany = Field(..., description="Target company information")
    financials: FinancialMetrics = Field(..., description="Raw financial metrics")
    im_text: Optional[str] = Field(None, description="Full IM text for additional context")

class ScoreFourPillarsInput(BaseModel):
    """Input for scoring the 4 operational pillars."""
    target: TargetCompany = Field(..., description="Target company information")
    business_description: str = Field(..., description="Detailed business model description")

class DetectRedFlagsInput(BaseModel):
    """Input for red flag detection."""
    target: TargetCompany = Field(..., description="Target company information")
    financials: FinancialMetrics = Field(..., description="Financial metrics")
    im_text: Optional[str] = Field(None, description="Full IM text for additional context")

class ValueTargetInput(BaseModel):
    """Input for target valuation."""
    target: TargetCompany = Field(..., description="Target company information")
    ebitda_normalized: float = Field(..., description="Normalized EBITDA in EUR")

# ========== Tools ==========

@tool(args_schema=ReadFECInput)
def read_fec(fec_path: str, encoding: str = "latin-1", separator: str = "|") -> Dict:
    """
    Reads and analyzes a French FEC (Fichier des Écritures Comptables) file for MBI due diligence.

    MISSION: Provide precise, day-accurate financial analysis for acquisition targets.

    Key capabilities:
    - Day-accurate interest/revenue calculations (no approximations)
    - EBITDA normalization with French GAAP account mapping
    - Client/supplier concentration (red flag if >30%)
    - Owner compensation analysis (account 644)
    - Seasonality detection
    - Balance sheet quality checks

    The FEC is the official French accounting export format containing all journal entries.
    Standard columns (per Article A47 A-1):
    - JournalCode, JournalLib, EcritureNum, EcritureDate
    - CompteNum, CompteLib, CompAuxNum, CompAuxLib
    - PieceRef, PieceDate, EcritureLib
    - Debit, Credit, EcritureLet, DateLet, ValidDate, Montantdevise, Idevise

    Returns:
    - Exact financial metrics (revenue, expenses, EBITDA proxy)
    - Time-weighted calculations for partial periods
    - Concentration risks
    - Red flags for due diligence
    - Account-level detail for deep-dive analysis
    """
    try:
        # Read FEC file
        # Try different separators if | doesn't work
        separators_to_try = [separator, "|", ";", "\t"]
        df = None

        for sep in separators_to_try:
            try:
                df = pd.read_csv(
                    fec_path,
                    sep=sep,
                    encoding=encoding,
                    dtype=str,  # Read all as string first
                    low_memory=False
                )
                if len(df.columns) >= 10:  # FEC should have at least 10 columns
                    break
            except:
                continue

        if df is None or len(df.columns) < 10:
            return {
                "error": "Could not parse FEC file. Try different encoding or separator.",
                "tried_separators": separators_to_try,
                "encoding": encoding
            }

        # Standardize column names (some FEC files have different casing)
        df.columns = [col.strip() for col in df.columns]

        # Convert amounts to float
        if 'Debit' in df.columns:
            df['Debit'] = pd.to_numeric(df['Debit'].str.replace(',', '.'), errors='coerce').fillna(0)
        if 'Credit' in df.columns:
            df['Credit'] = pd.to_numeric(df['Credit'].str.replace(',', '.'), errors='coerce').fillna(0)

        # Convert dates
        if 'EcritureDate' in df.columns:
            df['EcritureDate'] = pd.to_datetime(df['EcritureDate'], format='%Y%m%d', errors='coerce')

        # Basic statistics
        total_entries = len(df)
        date_range = (df['EcritureDate'].min(), df['EcritureDate'].max()) if 'EcritureDate' in df.columns else None
        unique_accounts = df['CompteNum'].nunique() if 'CompteNum' in df.columns else 0

        # Calculate exact number of days in period (for annualization)
        nb_days_in_period = (date_range[1] - date_range[0]).days if date_range else 365
        period_factor = 365.25 / nb_days_in_period if nb_days_in_period > 0 else 1

        # Revenue analysis (Class 7)
        revenue_accounts = df[df['CompteNum'].str.startswith('7', na=False)]
        total_revenue = revenue_accounts['Credit'].sum() - revenue_accounts['Debit'].sum()

        # Expense analysis (Class 6)
        expense_accounts = df[df['CompteNum'].str.startswith('6', na=False)]
        total_expenses = expense_accounts['Debit'].sum() - expense_accounts['Credit'].sum()

        # Account 644 - Owner compensation (key for EBITDA normalization)
        owner_comp = df[df['CompteNum'].str.startswith('644', na=False)]
        owner_comp_total = owner_comp['Debit'].sum() - owner_comp['Credit'].sum()

        # Account 681 - Depreciation (add back for EBITDA)
        depreciation = df[df['CompteNum'].str.startswith('681', na=False)]
        depreciation_total = depreciation['Debit'].sum() - depreciation['Credit'].sum()

        # Account 6815 - Provisions (add back for EBITDA)
        provisions = df[df['CompteNum'].str.startswith('6815', na=False)]
        provisions_total = provisions['Debit'].sum() - provisions['Credit'].sum()

        # Client concentration (411XXX accounts)
        clients = df[df['CompteNum'].str.match(r'^411\d+', na=False)].copy()
        if len(clients) > 0:
            client_balances = clients.groupby('CompteNum').apply(
                lambda x: (x['Debit'].sum() - x['Credit'].sum())
            ).sort_values(ascending=False)
            top_5_clients = client_balances.head(5)
            top_client_concentration = top_5_clients.sum() / client_balances.sum() if client_balances.sum() != 0 else 0
        else:
            top_5_clients = pd.Series()
            top_client_concentration = 0

        # Supplier concentration (401XXX accounts)
        suppliers = df[df['CompteNum'].str.match(r'^401\d+', na=False)].copy()
        if len(suppliers) > 0:
            supplier_balances = suppliers.groupby('CompteNum').apply(
                lambda x: (x['Credit'].sum() - x['Debit'].sum())
            ).sort_values(ascending=False)
            top_5_suppliers = supplier_balances.head(5)
            top_supplier_concentration = top_5_suppliers.sum() / supplier_balances.sum() if supplier_balances.sum() != 0 else 0
        else:
            top_5_suppliers = pd.Series()
            top_supplier_concentration = 0

        # Red flags detection
        red_flags = []

        # Red flag: Client concentration >30%
        if top_client_concentration > 0.30:
            red_flags.append({
                "type": "Concentration client",
                "severity": "High" if top_client_concentration > 0.50 else "Medium",
                "description": f"Top 5 clients = {top_client_concentration*100:.1f}% du CA (>30% = risque)"
            })

        # Red flag: Owner compensation excessive (>10% revenue for small business)
        if owner_comp_total > 0 and total_revenue > 0:
            owner_comp_pct = owner_comp_total / total_revenue
            if owner_comp_pct > 0.10:
                red_flags.append({
                    "type": "Rémunération dirigeant excessive",
                    "severity": "Medium",
                    "description": f"Compte 644 = {owner_comp_pct*100:.1f}% du CA (normalisable pour EBITDA)",
                    "adjustable_amount": round(owner_comp_total, 2)
                })

        # Red flag: Loss-making
        if (total_revenue - total_expenses) < 0:
            red_flags.append({
                "type": "Résultat déficitaire",
                "severity": "High",
                "description": f"Perte de {abs(total_revenue - total_expenses):,.2f} €"
            })

        # Monthly seasonality analysis
        monthly_revenue = revenue_accounts.groupby(revenue_accounts['EcritureDate'].dt.to_period('M')).apply(
            lambda x: (x['Credit'].sum() - x['Debit'].sum())
        )
        if len(monthly_revenue) >= 3:
            revenue_std = monthly_revenue.std()
            revenue_mean = monthly_revenue.mean()
            coef_variation = (revenue_std / revenue_mean) if revenue_mean > 0 else 0
            high_seasonality = coef_variation > 0.3
        else:
            coef_variation = 0
            high_seasonality = False

        return {
            "success": True,
            "file_path": fec_path,
            "total_entries": total_entries,
            "date_range": {
                "start": date_range[0].strftime('%Y-%m-%d') if date_range else None,
                "end": date_range[1].strftime('%Y-%m-%d') if date_range else None,
                "nb_days": nb_days_in_period,
                "is_full_year": abs(nb_days_in_period - 365) < 10
            },
            "unique_accounts": unique_accounts,
            "financials": {
                "total_revenue": round(total_revenue, 2),
                "total_revenue_annualized": round(total_revenue * period_factor, 2),
                "total_expenses": round(total_expenses, 2),
                "result_before_tax": round(total_revenue - total_expenses, 2),
                "owner_compensation_644": round(owner_comp_total, 2),
                "depreciation_681": round(depreciation_total, 2),
                "provisions_6815": round(provisions_total, 2),
                "ebitda_proxy": round(total_revenue - total_expenses + depreciation_total + provisions_total, 2),
                "ebitda_margin_pct": round(((total_revenue - total_expenses + depreciation_total + provisions_total) / total_revenue * 100), 2) if total_revenue > 0 else 0
            },
            "concentration": {
                "top_client_concentration_pct": round(top_client_concentration * 100, 2),
                "top_5_clients": top_5_clients.head(5).to_dict(),
                "top_supplier_concentration_pct": round(top_supplier_concentration * 100, 2),
                "top_5_suppliers": top_5_suppliers.head(5).to_dict(),
                "client_risk": "HIGH" if top_client_concentration > 0.30 else "LOW"
            },
            "seasonality": {
                "coefficient_variation": round(coef_variation, 3),
                "high_seasonality": high_seasonality,
                "note": "Coef > 0.3 = forte saisonnalité (risque cash flow)"
            },
            "red_flags": red_flags,
            "dd_notes": {
                "period_accuracy": f"Période de {nb_days_in_period} jours (facteur annualisation: {period_factor:.3f})",
                "ebitda_adjustments_needed": owner_comp_total > 0 or depreciation_total > 0 or provisions_total > 0,
                "key_accounts_to_review": [
                    "644 (Rémunération exploitant)" if owner_comp_total > 0 else None,
                    "411XXX (Détail clients)" if top_client_concentration > 0.30 else None,
                    "67X (Charges exceptionnelles à normaliser)"
                ]
            },
            "next_steps": [
                "Use normalize_ebitda tool with FEC insights",
                f"Analyze owner_compensation_644: {owner_comp_total:,.2f} EUR" if owner_comp_total > 0 else "No owner compensation detected",
                f"⚠️ Client concentration = {top_client_concentration*100:.1f}% - red flag if >30%" if top_client_concentration > 0.30 else "Client diversification OK",
                "Review monthly revenue trend for seasonality",
                f"⚠️ Period = {nb_days_in_period} days - annualize metrics" if not abs(nb_days_in_period - 365) < 10 else "Full year data"
            ]
        }

    except Exception as e:
        return {
            "error": f"Failed to read FEC: {str(e)}",
            "file_path": fec_path,
            "encoding": encoding,
            "separator": separator
        }

@tool(args_schema=ExtractIMDataInput)
def extract_im_data(im_text: str) -> Dict:
    """
    Extracts structured financial data from an Information Memorandum (IM) text.
    Uses Haiku for fast extraction from large documents.
    Returns: TargetCompany + FinancialMetrics + key business info.
    """
    # This would call Haiku via call_llm with model_type="haiku"
    # For now, placeholder structure
    return {
        "instruction": "Call this tool with IM text to extract structured data",
        "model_to_use": "haiku",
        "output": "TargetCompany + FinancialMetrics + business_description"
    }

@tool(args_schema=NormalizeEBITDAInput)
def normalize_ebitda(
    target: TargetCompany,
    financials: FinancialMetrics,
    im_text: Optional[str] = None
) -> Dict:
    """
    Normalizes EBITDA by applying adjustments appropriate for the company's
    accounting standard, sector, and geography.

    Uses Sonnet 4.5 for complex analysis and judgment calls.

    Returns: List of EBITDAAdjustment + normalized EBITDA value.
    """
    accounting_map = ACCOUNTING_MAPPINGS.get(target.accounting_standard)

    # Standard adjustments to consider based on accounting system
    adjustments_to_check = []

    if target.accounting_standard == "French GAAP":
        adjustments_to_check = [
            "Rémunération dirigeant excessive",
            "Charges personnelles (véhicule, logement)",
            "Provisions réglementées à neutraliser",
            "Crédit-bail à retraiter (si comparaison IFRS)",
            "Subventions d'exploitation",
            "Éléments non-récurrents"
        ]
    elif target.accounting_standard == "US GAAP":
        adjustments_to_check = [
            "Stock-based compensation",
            "Non-recurring items",
            "Restructuring charges",
            "Management compensation excess"
        ]
    else:  # IFRS
        adjustments_to_check = [
            "Impairment charges (non-cash)",
            "Fair value adjustments",
            "Non-recurring items",
            "Management compensation excess"
        ]

    return {
        "instruction": "Call Sonnet 4.5 to analyze and propose adjustments",
        "model_to_use": "sonnet",
        "accounting_standard": target.accounting_standard,
        "adjustments_to_consider": adjustments_to_check,
        "output": "List[EBITDAAdjustment] + ebitda_normalized"
    }

@tool(args_schema=ScoreFourPillarsInput)
def score_four_pillars(
    target: TargetCompany,
    business_description: str
) -> FourPillarsScore:
    """
    Scores a target against the 4 operational pillars:
    1. Repetitive operations (0-10)
    2. Recurring revenue (0-10)
    3. Low digitalization / automation opportunity (0-10)
    4. Diversified client base (0-10)

    Uses Sonnet 4.5 for qualitative assessment.
    """
    return FourPillarsScore(
        repetitive_operations=0,
        recurring_revenue=0,
        low_digitalization=0,
        diversified_client_base=0,
        total_score=0,
        comments="Call Sonnet 4.5 to score based on business description"
    )

@tool(args_schema=DetectRedFlagsInput)
def detect_red_flags(
    target: TargetCompany,
    financials: FinancialMetrics,
    im_text: Optional[str] = None
) -> List[RedFlag]:
    """
    Detects potential red flags and deal-breakers:
    - Structural decline
    - Client/supplier concentration >30%
    - Major litigation
    - Complex real estate assets
    - Heavy regulation
    - Management issues

    Uses Sonnet 4.5 for analysis.
    """
    return [
        {
            "instruction": "Call Sonnet 4.5 to analyze for red flags",
            "model_to_use": "sonnet",
            "checks": [
                "Client concentration analysis",
                "Debt level vs EBITDA",
                "Market trend (growth/decline)",
                "Regulatory compliance mentions",
                "Litigation mentions"
            ]
        }
    ]

@tool(args_schema=ValueTargetInput)
def value_target(
    target: TargetCompany,
    ebitda_normalized: float
) -> Valuation:
    """
    Values a target company using sector-specific EV/EBITDA multiples.
    Adjusts for geography and specific characteristics.

    Uses Sonnet 4.5 for valuation analysis.
    """
    # Get sector-specific multiples
    multiples = SECTOR_MULTIPLES.get(target.sector, SECTOR_MULTIPLES["Autre"])

    # Apply geography adjustment (optional, conservative approach)
    geo_index = GEOGRAPHY_COST_INDEX.get(target.geography, 1.0)
    # Higher costs might justify slightly lower multiples (debatable)

    ev_low = ebitda_normalized * multiples["low"]
    ev_mid = ebitda_normalized * multiples["mid"]
    ev_high = ebitda_normalized * multiples["high"]

    return Valuation(
        target_name=target.name,
        ebitda_normalized=ebitda_normalized,
        ev_ebitda_low=multiples["low"],
        ev_ebitda_mid=multiples["mid"],
        ev_ebitda_high=multiples["high"],
        enterprise_value_low=ev_low,
        enterprise_value_mid=ev_mid,
        enterprise_value_high=ev_high,
        comparables=[]  # Would be populated by comparable search
    )

# ========== Financial Datasets API Integration ==========

class GetCompanyFinancialsInput(BaseModel):
    """Input for getting company financials via Financial Datasets API."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'CARR')")
    period: Optional[str] = Field("annual", description="Period type: 'annual', 'quarterly', or 'ttm'")
    limit: int = Field(5, description="Number of periods to retrieve (default 5 years)")

@tool(args_schema=GetCompanyFinancialsInput)
def get_company_financials(
    ticker: str,
    period: str = "annual",
    limit: int = 5
) -> Dict:
    """
    Get financial statements for a public company using Financial Datasets API.

    Useful for:
    - Benchmarking private target against public comps
    - Understanding sector margins/multiples
    - Validating target financials

    Returns:
    - Income statements (revenue, operating income, net income)
    - Balance sheets (assets, liabilities, equity)
    - Cash flow statements
    - Key ratios and metrics

    Requires FINANCIAL_DATASETS_API_KEY in environment.

    Example tickers:
    - CARR: Carrier Global (HVAC)
    - JCI: Johnson Controls (Building tech)
    - GNRC: Generac (Power systems)
    - TTEK: Tetra Tech (Infrastructure)
    """
    api_key = os.getenv("FINANCIAL_DATASETS_API_KEY")

    if not api_key:
        return {
            "error": "FINANCIAL_DATASETS_API_KEY not set",
            "message": "Add API key to .env file"
        }

    try:
        # Financial Datasets API endpoint (all financial statements)
        url = "https://api.financialdatasets.ai/financials/"

        params = {
            "ticker": ticker.upper(),
            "period": period,
            "limit": limit
        }

        response = requests.get(
            url,
            headers={"X-API-KEY": api_key},
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()

            if not data.get("financials"):
                return {
                    "error": "No data found",
                    "message": f"No financial data for ticker {ticker}"
                }

            # Extract key metrics from latest period
            latest = data["financials"][0] if data["financials"] else {}

            # Calculate metrics
            revenue = latest.get("revenue", 0)
            operating_income = latest.get("operating_income", 0)
            net_income = latest.get("net_income", 0)
            total_assets = latest.get("total_assets", 0)
            total_liabilities = latest.get("total_liabilities", 0)
            ebitda = latest.get("ebitda", 0)

            # Calculate margins
            operating_margin = (operating_income / revenue * 100) if revenue > 0 else 0
            net_margin = (net_income / revenue * 100) if revenue > 0 else 0
            ebitda_margin = (ebitda / revenue * 100) if revenue > 0 else 0

            return {
                "success": True,
                "ticker": ticker.upper(),
                "period": period,
                "latest_period": latest.get("period_end_date"),
                "key_metrics": {
                    "revenue": revenue,
                    "ebitda": ebitda,
                    "operating_income": operating_income,
                    "net_income": net_income,
                    "total_assets": total_assets,
                    "total_liabilities": total_liabilities,
                    "equity": total_assets - total_liabilities
                },
                "margins": {
                    "ebitda_margin_pct": round(ebitda_margin, 2),
                    "operating_margin_pct": round(operating_margin, 2),
                    "net_margin_pct": round(net_margin, 2)
                },
                "historical_data": data["financials"],
                "source": "Financial Datasets API"
            }
        else:
            return {
                "error": f"API returned status {response.status_code}",
                "message": response.text[:200]
            }

    except Exception as e:
        return {
            "error": "Failed to fetch financials",
            "message": str(e)
        }

# ========== MBI Tools List ==========

MBI_TOOLS = [
    read_fec,
    extract_im_data,
    normalize_ebitda,
    score_four_pillars,
    detect_red_flags,
    value_target,
    get_company_financials  # Financial Datasets API integration
]
