"""
Full Investment Analyst Tools for Buy & Build / Rollup
Covers all 6 phases: Sourcing → DD → Valuation → Negotiation → Integration → Tech
"""

from langchain.tools import tool
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json

from dexter.schemas import (
    # Phase 1: Sourcing
    TargetLead, SourcingCriteria, OutreachTemplate,
    # Phase 2: DD
    TargetCompany, FinancialMetrics, EBITDAAdjustment,
    FourPillarsScore, RedFlag, DueDiligenceReport,
    # Phase 3: Valuation
    DCFAssumptions, DCFValuation, DealStructure, LBOModel, Valuation,
    # Phase 4: Negotiation
    NegotiationStrategy, LOI,
    # Phase 5: Integration
    Integration100DayPlan, Synergy, IntegrationKPIs,
    # Phase 6: Tech
    TechPlatformModule, AutomationOpportunity, TechRoadmap,
    # Common
    Sector, Geography
)

# ========================================
# PHASE 1: SOURCING TOOLS
# ========================================

class GenerateTargetListInput(BaseModel):
    criteria: SourcingCriteria = Field(..., description="Sourcing criteria for target generation")

@tool(args_schema=GenerateTargetListInput)
def generate_target_list(criteria: SourcingCriteria) -> List[TargetLead]:
    """
    Generates a list of target companies matching the sourcing criteria.
    Uses public databases (Infogreffe, Pappers, Societe.com) to identify potential targets.

    Returns: List of TargetLead with quick scoring.
    Model: Haiku for fast bulk processing.
    """
    return {
        "instruction": "Use Haiku to search public databases and generate target list",
        "databases": ["Infogreffe", "Pappers", "Societe.com"],
        "criteria": criteria.dict(),
        "output": "List[TargetLead] with quick_score 0-100"
    }

class QuickScoreInput(BaseModel):
    lead: TargetLead = Field(..., description="Target lead to score")
    thesis_criteria: str = Field(..., description="Investment thesis criteria to check")

@tool(args_schema=QuickScoreInput)
def quick_score_target(lead: TargetLead, thesis_criteria: str) -> int:
    """
    Quick scores a target lead (0-100) based on thesis fit.

    Checks:
    - EBITDA range (500k-2M€)
    - Sector fit (fragmentation, tech deficit)
    - Geography fit
    - 4 pillars preliminary assessment

    Model: Haiku for speed.
    Returns: Score 0-100.
    """
    return {
        "instruction": "Use Haiku to quick score against thesis",
        "lead": lead.dict(),
        "thesis": thesis_criteria,
        "output": "int 0-100"
    }

class GenerateOutreachInput(BaseModel):
    lead: TargetLead = Field(..., description="Target lead for outreach")
    pitch_style: str = Field("growth_partner", description="Pitch style: 'growth_partner', 'tech_transformation', 'liquidity_event'")

@tool(args_schema=GenerateOutreachInput)
def generate_personalized_outreach(lead: TargetLead, pitch_style: str) -> OutreachTemplate:
    """
    Generates a personalized outreach email for a target.
    Tailors messaging based on sector, geography, and company profile.

    Model: Sonnet 4.5 for high-quality, persuasive copy.
    Returns: OutreachTemplate with email subject, body, follow-up strategy.
    """
    return {
        "instruction": "Use Sonnet 4.5 to craft personalized outreach",
        "lead": lead.dict(),
        "pitch_style": pitch_style,
        "output": "OutreachTemplate"
    }

# ========================================
# PHASE 2: DUE DILIGENCE TOOLS
# (Already created in tools_mbi.py - reuse normalize_ebitda, score_four_pillars, detect_red_flags, etc.)
# ========================================

# Import from tools_mbi.py:
# - extract_im_data
# - normalize_ebitda
# - score_four_pillars
# - detect_red_flags
# - value_target (multiples-based)

# ========================================
# PHASE 3: VALUATION & DEAL STRUCTURING
# ========================================

class BuildDCFInput(BaseModel):
    target: TargetCompany
    financials: FinancialMetrics
    assumptions: DCFAssumptions

@tool(args_schema=BuildDCFInput)
def build_dcf_model(target: TargetCompany, financials: FinancialMetrics, assumptions: DCFAssumptions) -> DCFValuation:
    """
    Builds a DCF (Discounted Cash Flow) valuation model.

    Steps:
    1. Project free cash flows (5 years)
    2. Calculate terminal value
    3. Discount at WACC
    4. Perform sensitivity analysis (WACC ±2%, terminal growth ±1%)

    Model: Sonnet 4.5 for complex financial modeling.
    Returns: DCFValuation with enterprise value, equity value, sensitivity analysis.
    """
    return {
        "instruction": "Use Sonnet 4.5 to build DCF model",
        "target": target.dict(),
        "financials": financials.dict(),
        "assumptions": assumptions.dict(),
        "output": "DCFValuation"
    }

class ProposeDealStructureInput(BaseModel):
    target_name: str
    enterprise_value: float = Field(..., description="Target enterprise value in EUR")
    seller_motivation: str = Field(..., description="Seller motivation (e.g., 'full exit', 'partial liquidity', 'growth capital')")
    available_cash: float = Field(..., description="Cash available for deal in EUR")

@tool(args_schema=ProposeDealStructureInput)
def propose_deal_structure(
    target_name: str,
    enterprise_value: float,
    seller_motivation: str,
    available_cash: float
) -> DealStructure:
    """
    Proposes an optimal deal structure based on:
    - Enterprise value target
    - Seller motivation
    - Available financing

    Considers: cash, earn-out, vendor loan, equity rollover.

    Model: Sonnet 4.5 for structuring expertise.
    Returns: DealStructure with recommended split.
    """
    return {
        "instruction": "Use Sonnet 4.5 to propose optimal deal structure",
        "inputs": {
            "target_name": target_name,
            "enterprise_value": enterprise_value,
            "seller_motivation": seller_motivation,
            "available_cash": available_cash
        },
        "output": "DealStructure"
    }

class BuildLBOModelInput(BaseModel):
    target_name: str
    enterprise_value: float
    ebitda_normalized: float
    equity_investment: float = Field(..., description="Equity investment in EUR")
    target_leverage: float = Field(3.0, description="Target leverage (Debt/EBITDA)")

@tool(args_schema=BuildLBOModelInput)
def build_lbo_model(
    target_name: str,
    enterprise_value: float,
    ebitda_normalized: float,
    equity_investment: float,
    target_leverage: float
) -> LBOModel:
    """
    Builds an LBO (Leveraged Buyout) financing model.

    Calculates:
    - Debt capacity (based on leverage ratio)
    - Senior vs mezzanine debt split
    - Interest coverage
    - Projected IRR and MOIC (5-year hold assumption)

    Model: Sonnet 4.5 for financial modeling.
    Returns: LBOModel with financing structure and returns.
    """
    return {
        "instruction": "Use Sonnet 4.5 to build LBO model",
        "inputs": {
            "target_name": target_name,
            "enterprise_value": enterprise_value,
            "ebitda_normalized": ebitda_normalized,
            "equity_investment": equity_investment,
            "target_leverage": target_leverage
        },
        "output": "LBOModel"
    }

# ========================================
# PHASE 4: NEGOTIATION TOOLS
# ========================================

class PrepareNegotiationInput(BaseModel):
    target_name: str
    valuation_range_low: float
    valuation_range_high: float
    seller_profile: str = Field(..., description="Seller profile (e.g., 'family business, emotional attachment', 'PE exit, price-focused')")

@tool(args_schema=PrepareNegotiationInput)
def prepare_negotiation_strategy(
    target_name: str,
    valuation_range_low: float,
    valuation_range_high: float,
    seller_profile: str
) -> NegotiationStrategy:
    """
    Prepares a negotiation strategy with walk-away/target/stretch prices.

    Identifies:
    - Your strengths (e.g., certainty of close, operational value-add)
    - Potential objections from seller
    - Counter-arguments

    Model: Sonnet 4.5 for strategic thinking.
    Returns: NegotiationStrategy.
    """
    return {
        "instruction": "Use Sonnet 4.5 to prepare negotiation strategy",
        "inputs": {
            "target_name": target_name,
            "valuation_range": [valuation_range_low, valuation_range_high],
            "seller_profile": seller_profile
        },
        "output": "NegotiationStrategy"
    }

class DraftLOIInput(BaseModel):
    target_name: str
    proposed_ev: float
    deal_structure: DealStructure

@tool(args_schema=DraftLOIInput)
def draft_loi(target_name: str, proposed_ev: float, deal_structure: DealStructure) -> LOI:
    """
    Drafts a Letter of Intent (LOI) with key terms.

    Includes:
    - Proposed enterprise value
    - Structure summary
    - Exclusivity period
    - Conditions precedent
    - DD scope
    - Timeline

    Model: Sonnet 4.5 for professional drafting.
    Returns: LOI.
    """
    return {
        "instruction": "Use Sonnet 4.5 to draft LOI",
        "inputs": {
            "target_name": target_name,
            "proposed_ev": proposed_ev,
            "deal_structure": deal_structure.dict()
        },
        "output": "LOI"
    }

# ========================================
# PHASE 5: INTEGRATION TOOLS
# ========================================

class Create100DayPlanInput(BaseModel):
    target: TargetCompany
    dd_report: DueDiligenceReport

@tool(args_schema=Create100DayPlanInput)
def create_100_day_plan(target: TargetCompany, dd_report: DueDiligenceReport) -> Integration100DayPlan:
    """
    Creates a 100-day integration plan post-acquisition.

    Phases:
    - Month 1 (Days 1-30): Stabilization (communication, retention, quick wins)
    - Month 2 (Days 31-60): Foundation (systems, processes, team alignment)
    - Month 3+ (Days 61-100): Transformation (digitalization, synergies, scaling)

    Model: Sonnet 4.5 for structured planning.
    Returns: Integration100DayPlan.
    """
    return {
        "instruction": "Use Sonnet 4.5 to create 100-day integration plan",
        "target": target.dict(),
        "dd_insights": dd_report.dict(),
        "output": "Integration100DayPlan"
    }

class IdentifySynergiesInput(BaseModel):
    target: TargetCompany
    existing_portfolio: Optional[List[str]] = Field(None, description="Existing portfolio companies if any")

@tool(args_schema=IdentifySynergiesInput)
def identify_synergies(target: TargetCompany, existing_portfolio: Optional[List[str]]) -> List[Synergy]:
    """
    Identifies synergy opportunities:
    - Revenue synergies (cross-sell, geo expansion)
    - Cost synergies (procurement, back-office)
    - Operational synergies (process improvements)
    - Financial synergies (better financing terms)

    Model: Sonnet 4.5 for strategic analysis.
    Returns: List[Synergy] with value quantification.
    """
    return {
        "instruction": "Use Sonnet 4.5 to identify and quantify synergies",
        "target": target.dict(),
        "existing_portfolio": existing_portfolio,
        "output": "List[Synergy]"
    }

class DefineIntegrationKPIsInput(BaseModel):
    target_name: str
    integration_plan: Integration100DayPlan

@tool(args_schema=DefineIntegrationKPIsInput)
def define_integration_kpis(target_name: str, integration_plan: Integration100DayPlan) -> IntegrationKPIs:
    """
    Defines KPIs to track integration success:
    - Revenue retention
    - Employee retention
    - Customer retention
    - Synergies realized
    - EBITDA improvement
    - NPS score

    Model: Sonnet 4.5 for KPI framework.
    Returns: IntegrationKPIs.
    """
    return {
        "instruction": "Use Sonnet 4.5 to define integration KPIs",
        "target_name": target_name,
        "integration_plan": integration_plan.dict(),
        "output": "IntegrationKPIs"
    }

# ========================================
# PHASE 6: TECH PLATFORM TOOLS
# ========================================

class DesignTechPlatformInput(BaseModel):
    target: TargetCompany
    current_tech_stack: str = Field(..., description="Description of current tech/systems")

@tool(args_schema=DesignTechPlatformInput)
def design_tech_platform(target: TargetCompany, current_tech_stack: str) -> TechRoadmap:
    """
    Designs the target back-office tech platform architecture.

    Modules: Finance, HR, CRM, Operations, Procurement, Analytics.
    For each: Current state → Target state → Build/Buy → Vendor recommendation.

    Model: Sonnet 4.5 for tech architecture.
    Returns: TechRoadmap with phased deployment plan.
    """
    return {
        "instruction": "Use Sonnet 4.5 to design tech platform roadmap",
        "target": target.dict(),
        "current_tech": current_tech_stack,
        "output": "TechRoadmap"
    }

class IdentifyAutomationInput(BaseModel):
    target: TargetCompany
    process_description: str = Field(..., description="Description of current manual processes")

@tool(args_schema=IdentifyAutomationInput)
def identify_automation_opportunities(
    target: TargetCompany,
    process_description: str
) -> List[AutomationOpportunity]:
    """
    Identifies automation opportunities in current manual processes.

    For each process:
    - Current manual hours/month
    - Automation potential %
    - Annual cost savings
    - Implementation effort
    - Priority

    Model: Sonnet 4.5 for process analysis.
    Returns: List[AutomationOpportunity] ranked by ROI.
    """
    return {
        "instruction": "Use Sonnet 4.5 to identify automation opportunities",
        "target": target.dict(),
        "processes": process_description,
        "output": "List[AutomationOpportunity]"
    }

# ========================================
# CONSOLIDATED TOOLS LIST
# ========================================

FULL_ANALYST_TOOLS = [
    # Phase 1: Sourcing
    generate_target_list,
    quick_score_target,
    generate_personalized_outreach,

    # Phase 2: DD
    # (import from tools_mbi.py)

    # Phase 3: Valuation
    build_dcf_model,
    propose_deal_structure,
    build_lbo_model,

    # Phase 4: Negotiation
    prepare_negotiation_strategy,
    draft_loi,

    # Phase 5: Integration
    create_100_day_plan,
    identify_synergies,
    define_integration_kpis,

    # Phase 6: Tech
    design_tech_platform,
    identify_automation_opportunities
]
