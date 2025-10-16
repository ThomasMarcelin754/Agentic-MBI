"""
MBI/Rollup specific tools for due diligence and analysis.
Includes accounting system mapping and sector-specific adjustments.
"""

from langchain.tools import tool
from typing import List, Dict, Optional, Literal
import os
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

# ========== Tool Input Schemas ==========

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

# ========== MBI Tools List ==========

MBI_TOOLS = [
    extract_im_data,
    normalize_ebitda,
    score_four_pillars,
    detect_red_flags,
    value_target
]
