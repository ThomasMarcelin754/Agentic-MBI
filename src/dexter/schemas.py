from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict
from datetime import date

# ========== Original Dexter Schemas ==========
class Task(BaseModel):
    """Represents a single task in a task list."""
    id: int = Field(..., description="Unique identifier for the task.")
    description: str = Field(..., description="The description of the task.")
    done: bool = Field(False, description="Whether the task is completed.")

class TaskList(BaseModel):
    """Represents a list of tasks."""
    tasks: List[Task] = Field(..., description="The list of tasks.")

class IsDone(BaseModel):
    """Represents the boolean status of a task."""
    done: bool = Field(..., description="Whether the task is done or not.")

class Answer(BaseModel):
    """Represents an answer to the user's query."""
    answer: str = Field(..., description="A comprehensive answer to the user's query, including relevant numbers, data, reasoning, and insights.")

# ========== MBI/Rollup Specific Schemas ==========
# Covers all 6 phases: Sourcing → DD → Valuation → Negotiation → Integration → Tech

# ========== PHASE 1: SOURCING ==========

# Accounting systems
AccountingStandard = Literal["French GAAP", "US GAAP", "IFRS"]

# Sectors
Sector = Literal[
    "CVC", "Sécurité Incendie", "3D", "Ventilation", "IRVE",
    "Chaudières", "Toiture", "Portes", "Légionelles", "Diagnostics",
    "Entretien Bâtiment", "Véhicules Lourds", "Cuisine Pro", "GTA",
    "Installations Sportives", "Balayeuse", "Marquage", "Élagage",
    "Paysage", "Piscines", "Photovoltaïque", "Gestion Locative",
    "Courtage Assurance", "Infogérance RH", "Clinique Esthétique", "Autre"
]

# Geography
Geography = Literal[
    "Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux",
    "Lille", "Nantes", "Strasbourg", "Nice", "Montpellier",
    "Rennes", "Grenoble", "Autre"
]

class TargetLead(BaseModel):
    """Represents a sourced lead (Phase 1: Sourcing)."""
    company_name: str
    sector: Sector
    geography: Geography
    estimated_revenue: Optional[float] = Field(None, description="Estimated revenue in EUR")
    estimated_ebitda: Optional[float] = Field(None, description="Estimated EBITDA in EUR")
    source: str = Field(..., description="Source of lead (Infogreffe, Pappers, referral, etc.)")
    contact_info: Optional[str] = Field(None, description="Contact information if available")
    quick_score: Optional[int] = Field(None, description="Quick score 0-100 based on thesis fit", ge=0, le=100)
    notes: Optional[str] = Field(None, description="Additional notes")

class SourcingCriteria(BaseModel):
    """Criteria for generating sourcing lists."""
    sectors: List[Sector]
    geographies: List[Geography]
    min_ebitda: float = Field(500_000, description="Minimum EBITDA in EUR")
    max_ebitda: float = Field(2_000_000, description="Maximum EBITDA in EUR")
    min_history_years: int = Field(5, description="Minimum years in business")
    require_recurring_revenue: bool = Field(True, description="Filter for recurring revenue model")

class OutreachTemplate(BaseModel):
    """Template for personalized outreach to target company."""
    target_name: str
    sector: Sector
    geography: Geography
    pitch_angle: str = Field(..., description="Customized pitch angle (e.g., 'tech transformation partner', 'growth capital')")
    email_subject: str
    email_body: str
    follow_up_strategy: str = Field(..., description="Recommended follow-up approach")

# ========== PHASE 2: DUE DILIGENCE ==========

class TargetCompany(BaseModel):
    """Represents a target company for acquisition."""
    name: str = Field(..., description="Company name")
    sector: Sector = Field(..., description="Business sector")
    geography: Geography = Field(..., description="Primary geographic location")
    accounting_standard: AccountingStandard = Field(..., description="Accounting standard used")
    founded_year: Optional[int] = Field(None, description="Year company was founded")

class FinancialMetrics(BaseModel):
    """Core financial metrics for a target company."""
    # Raw metrics
    revenue: float = Field(..., description="Revenue in EUR", gt=0)
    ebitda_reported: float = Field(..., description="Reported EBITDA in EUR")
    net_income: Optional[float] = Field(None, description="Net income in EUR")
    total_assets: Optional[float] = Field(None, description="Total assets in EUR")
    total_debt: Optional[float] = Field(None, description="Total debt in EUR")
    cash: Optional[float] = Field(None, description="Cash in EUR")

    # Period
    period_end: date = Field(..., description="Financial period end date")
    period_type: Literal["annual", "quarterly", "ttm"] = Field(..., description="Type of period")

    # Normalized metrics (post-retraitement)
    ebitda_normalized: Optional[float] = Field(None, description="Normalized EBITDA in EUR after adjustments")
    adjustments: Optional[List[str]] = Field(default_factory=list, description="List of adjustments made")

class EBITDAAdjustment(BaseModel):
    """Represents a single EBITDA normalization adjustment."""
    category: Literal[
        "Non-récurrent", "Rémunération dirigeant", "Loyers", "Provisions",
        "Amortissements", "Charges personnelles", "Syndic", "Autres"
    ]
    amount: float = Field(..., description="Adjustment amount in EUR (positive = adds to EBITDA)")
    description: str = Field(..., description="Detailed explanation of the adjustment")
    source: str = Field(..., description="Source document or line item")
    confidence: Literal["High", "Medium", "Low"] = Field(..., description="Confidence level in this adjustment")

class Comparable(BaseModel):
    """Comparable company for valuation multiples."""
    name: str
    sector: Sector
    geography: Geography
    revenue: float
    ebitda: float
    ev: Optional[float] = Field(None, description="Enterprise Value in EUR")
    ev_ebitda_multiple: Optional[float] = Field(None, description="EV/EBITDA multiple")
    transaction_date: Optional[date] = Field(None, description="Transaction date if applicable")

class Valuation(BaseModel):
    """Valuation analysis for a target."""
    target_name: str
    ebitda_normalized: float = Field(..., description="Normalized EBITDA used for valuation in EUR")

    # Multiples approach
    ev_ebitda_low: float = Field(..., description="Low-end EV/EBITDA multiple", gt=0)
    ev_ebitda_mid: float = Field(..., description="Mid-point EV/EBITDA multiple", gt=0)
    ev_ebitda_high: float = Field(..., description="High-end EV/EBITDA multiple", gt=0)

    # Resulting valuations
    enterprise_value_low: float = Field(..., description="Low-end enterprise value in EUR")
    enterprise_value_mid: float = Field(..., description="Mid-point enterprise value in EUR")
    enterprise_value_high: float = Field(..., description="High-end enterprise value in EUR")

    # Comparable companies used
    comparables: List[Comparable] = Field(default_factory=list, description="Comparable companies")

    # DCF (optional)
    dcf_value: Optional[float] = Field(None, description="DCF valuation in EUR if performed")

class FourPillarsScore(BaseModel):
    """Scoring based on the 4 operational pillars."""
    repetitive_operations: int = Field(..., description="Score 0-10: Degree of repetitiveness/standardization", ge=0, le=10)
    recurring_revenue: int = Field(..., description="Score 0-10: Degree of revenue recurrence", ge=0, le=10)
    low_digitalization: int = Field(..., description="Score 0-10: Opportunity for digitalization (10 = huge opportunity)", ge=0, le=10)
    diversified_client_base: int = Field(..., description="Score 0-10: Client diversification (10 = fully diversified)", ge=0, le=10)

    total_score: int = Field(..., description="Total score out of 40", ge=0, le=40)
    comments: str = Field(..., description="Detailed commentary on scoring")

class RedFlag(BaseModel):
    """Represents a deal-breaker or significant concern."""
    category: Literal[
        "Déclin structurel", "Concentration client", "Concentration fournisseur",
        "Litiges", "Actif immobilier", "Réglementation", "Management", "Autre"
    ]
    severity: Literal["Critical", "High", "Medium", "Low"]
    description: str = Field(..., description="Detailed description of the red flag")
    is_deal_breaker: bool = Field(..., description="Is this a deal-breaker?")

class DueDiligenceReport(BaseModel):
    """Complete due diligence report for a target."""
    target: TargetCompany
    financials: FinancialMetrics
    adjustments: List[EBITDAAdjustment]
    valuation: Valuation
    four_pillars: FourPillarsScore
    red_flags: List[RedFlag]

    # Final recommendation
    recommendation: Literal["GO", "MAYBE", "NO-GO"]
    recommendation_rationale: str = Field(..., description="Detailed rationale for the recommendation")

    # Validation flag (for semi-autonomous mode)
    requires_human_validation: bool = Field(True, description="Whether this report requires human review before action")

# ========== PHASE 3: VALUATION & DEAL STRUCTURING ==========

class DCFAssumptions(BaseModel):
    """Assumptions for DCF valuation model."""
    revenue_growth_rates: List[float] = Field(..., description="Revenue growth % for years 1-5")
    ebitda_margin: float = Field(..., description="Target EBITDA margin %", ge=0, le=100)
    capex_percent_revenue: float = Field(..., description="Capex as % of revenue")
    nwc_percent_revenue: float = Field(..., description="Net working capital as % of revenue")
    tax_rate: float = Field(25.0, description="Tax rate %", ge=0, le=100)
    wacc: float = Field(..., description="Weighted average cost of capital %", gt=0)
    terminal_growth_rate: float = Field(2.0, description="Perpetual growth rate %", ge=0, le=5)

class DCFValuation(BaseModel):
    """DCF valuation output."""
    enterprise_value: float = Field(..., description="DCF enterprise value in EUR")
    equity_value: float = Field(..., description="Equity value (EV - Net Debt) in EUR")
    assumptions: DCFAssumptions
    sensitivity_analysis: Optional[Dict] = Field(None, description="Sensitivity to WACC and terminal growth")

class DealStructure(BaseModel):
    """Proposed deal structure."""
    total_enterprise_value: float = Field(..., description="Total EV in EUR")
    cash_at_closing: float = Field(..., description="Cash payment at closing in EUR")
    earn_out: Optional[float] = Field(None, description="Earn-out amount in EUR")
    earn_out_conditions: Optional[str] = Field(None, description="Earn-out conditions and timeline")
    vendor_loan: Optional[float] = Field(None, description="Vendor loan amount in EUR")
    vendor_loan_terms: Optional[str] = Field(None, description="Vendor loan terms (rate, duration)")
    equity_rollover: Optional[float] = Field(None, description="Seller equity rollover %")
    management_retention: Optional[str] = Field(None, description="Management retention package")

class LBOModel(BaseModel):
    """LBO financing structure."""
    total_uses: float = Field(..., description="Total uses of funds in EUR")
    equity: float = Field(..., description="Equity investment in EUR")
    senior_debt: float = Field(..., description="Senior debt in EUR")
    senior_debt_rate: float = Field(..., description="Senior debt interest rate %")
    mezzanine_debt: Optional[float] = Field(None, description="Mezzanine debt in EUR")
    mezzanine_rate: Optional[float] = Field(None, description="Mezzanine interest rate %")
    leverage_ratio: float = Field(..., description="Total Debt / EBITDA")
    projected_irr: Optional[float] = Field(None, description="Projected IRR %")
    projected_moic: Optional[float] = Field(None, description="Projected MOIC (multiple on invested capital)")

# ========== PHASE 4: NEGOTIATION ==========

class NegotiationStrategy(BaseModel):
    """Negotiation positioning."""
    walk_away_price: float = Field(..., description="Maximum price in EUR - walk away above this")
    target_price: float = Field(..., description="Target price in EUR - ideal outcome")
    stretch_price: float = Field(..., description="Stretch price in EUR - acceptable if strong rationale")
    key_deal_terms: List[str] = Field(..., description="Non-price terms to negotiate (e.g., earn-out, warranties)")
    strengths: List[str] = Field(..., description="Your negotiation strengths")
    weaknesses: List[str] = Field(..., description="Potential weaknesses/objections from seller")
    counter_arguments: Dict[str, str] = Field(..., description="Responses to expected seller objections")

class LOI(BaseModel):
    """Letter of Intent terms."""
    target_name: str
    proposed_ev: float = Field(..., description="Proposed enterprise value in EUR")
    structure_summary: str = Field(..., description="Deal structure summary")
    exclusivity_period: int = Field(..., description="Exclusivity period in days")
    key_conditions: List[str] = Field(..., description="Key conditions precedent")
    due_diligence_scope: str = Field(..., description="Scope of DD")
    proposed_closing_timeline: str = Field(..., description="Target closing date")

# ========== PHASE 5: INTEGRATION ==========

class Integration100DayPlan(BaseModel):
    """100-day integration plan post-acquisition."""
    target_name: str

    # Day 1-30: Stabilization
    month_1_priorities: List[str] = Field(..., description="Critical actions for month 1")

    # Day 31-60: Foundation
    month_2_priorities: List[str] = Field(..., description="Actions for month 2")

    # Day 61-100: Transformation
    month_3_priorities: List[str] = Field(..., description="Actions for month 3+")

    # Quick wins (0-30 days)
    quick_wins: List[str] = Field(..., description="High-impact quick wins")

    # Key stakeholders
    key_stakeholders: Dict[str, str] = Field(..., description="Key people and roles")

    # Risks
    integration_risks: List[str] = Field(..., description="Top integration risks to monitor")

class Synergy(BaseModel):
    """Identified synergy opportunity."""
    category: Literal["Revenue", "Cost", "Operational", "Financial"]
    description: str
    annual_value_eur: float = Field(..., description="Estimated annual value in EUR")
    timeline_to_realize: str = Field(..., description="Timeline to realize (e.g., '6 months', '1 year')")
    confidence: Literal["High", "Medium", "Low"]
    implementation_complexity: Literal["Low", "Medium", "High"]
    responsible_function: str = Field(..., description="Function responsible (e.g., 'Finance', 'IT', 'Sales')")

class IntegrationKPIs(BaseModel):
    """KPIs for tracking integration progress."""
    target_name: str
    revenue_retention: Optional[float] = Field(None, description="% of revenue retained post-acquisition")
    employee_retention: Optional[float] = Field(None, description="% of key employees retained")
    customer_retention: Optional[float] = Field(None, description="% of customers retained")
    synergies_realized_eur: Optional[float] = Field(None, description="Synergies realized to date in EUR")
    ebitda_improvement: Optional[float] = Field(None, description="EBITDA improvement % vs baseline")
    nps_score: Optional[int] = Field(None, description="Net Promoter Score", ge=-100, le=100)

# ========== PHASE 6: TECH PLATFORM ==========

class TechPlatformModule(BaseModel):
    """Module in the back-office tech platform."""
    name: Literal["Finance", "HR", "CRM", "Operations", "Procurement", "Analytics"]
    current_state: str = Field(..., description="Current state (e.g., 'Excel-based', 'Legacy ERP')")
    target_state: str = Field(..., description="Target state (e.g., 'Cloud ERP', 'Automated workflows')")
    build_vs_buy: Literal["Build", "Buy", "Hybrid"]
    recommended_solution: Optional[str] = Field(None, description="Specific tool/vendor recommendation")
    estimated_cost_eur: Optional[float] = Field(None, description="Implementation cost in EUR")
    estimated_roi_months: Optional[int] = Field(None, description="Payback period in months")

class AutomationOpportunity(BaseModel):
    """Automation opportunity identified."""
    process_name: str
    current_manual_hours_per_month: float = Field(..., description="Current manual hours/month")
    automation_potential_percent: float = Field(..., description="% of work automatable", ge=0, le=100)
    annual_cost_savings_eur: float = Field(..., description="Annual cost savings in EUR")
    implementation_effort: Literal["Low", "Medium", "High"]
    priority: Literal["Critical", "High", "Medium", "Low"]

class TechRoadmap(BaseModel):
    """Tech platform deployment roadmap."""
    target_name: str
    modules: List[TechPlatformModule]
    automation_opportunities: List[AutomationOpportunity]
    phase_1_6m: List[str] = Field(..., description="Priorities for months 1-6")
    phase_2_12m: List[str] = Field(..., description="Priorities for months 7-12")
    phase_3_18m: List[str] = Field(..., description="Priorities for months 13-18")
    total_investment_eur: float = Field(..., description="Total tech investment in EUR")
    expected_annual_savings_eur: float = Field(..., description="Expected annual savings in EUR")
