from pydantic import BaseModel, Field, field_validator


class TrendingCompany(BaseModel):
    company_name: str = Field(..., description="Full company name")
    ticker: str = Field(..., description="Stock ticker symbol")
    reason_trending: str = Field(
        ..., description="Why the company is currently trending"
    )
    catalysts: list[str] = Field(
        default_factory=list, description="Key recent catalysts"
    )
    sources: list[str] = Field(
        default_factory=list, description="Source references or URLs, when available"
    )


class TrendingCompanyList(BaseModel):
    companies: list[TrendingCompany] = Field(
        ..., description="Exactly 3 unique trending companies"
    )

    @field_validator("companies")
    @classmethod
    def validate_count_and_uniqueness(
        cls, v: list[TrendingCompany]
    ) -> list[TrendingCompany]:
        if len(v) != 3:
            raise ValueError(f"Expected exactly 3 trending companies, got {len(v)}")
        tickers = [c.ticker.strip().upper() for c in v]
        if len(set(tickers)) != len(tickers):
            raise ValueError("Duplicate company ticker in trending companies list")
        return v


class TrendingCompanyResearch(BaseModel):
    company_name: str = Field(..., description="Full company name")
    ticker: str = Field(..., description="Stock ticker symbol")
    investment_thesis: str = Field(..., description="Investment thesis")
    business_model_and_revenue_drivers: str = Field(
        ..., description="Business model and major revenue drivers"
    )
    competitive_position: str = Field(..., description="Competitive position")
    recent_financial_performance: str = Field(
        ..., description="Recent revenue and earnings performance"
    )
    growth_trends: str = Field(..., description="Revenue and earnings growth trends")
    profitability_and_margins: str = Field(..., description="Profitability and margins")
    cash_flow_and_balance_sheet: str = Field(
        ..., description="Cash flow and balance-sheet strength"
    )
    debt_and_liquidity: str = Field(..., description="Debt and liquidity")
    earnings_results_and_guidance: str = Field(
        ..., description="Recent earnings results and management guidance"
    )
    valuation_considerations: str = Field(..., description="Valuation considerations")
    recent_catalysts: str = Field(
        ..., description="Important recent news and catalysts"
    )
    key_risks: str = Field(..., description="Material risks and negative developments")
    analyst_sentiment: str = Field(
        default="", description="Analyst sentiment, when useful and current"
    )
    bull_case: str = Field(..., description="Bull case")
    bear_case: str = Field(..., description="Bear case")
    overall_assessment: str = Field(..., description="Overall assessment")
    sources: list[str] = Field(
        default_factory=list,
        description="Source references for significant current claims, when available",
    )


class TrendingCompanyResearchList(BaseModel):
    research: list[TrendingCompanyResearch] = Field(
        ..., description="Research covering exactly the 3 trending companies"
    )

    @field_validator("research")
    @classmethod
    def validate_exactly_three_and_unique(
        cls, v: list[TrendingCompanyResearch]
    ) -> list[TrendingCompanyResearch]:
        if len(v) != 3:
            raise ValueError(f"Expected research for exactly 3 companies, got {len(v)}")
        tickers = [r.ticker.strip().upper() for r in v]
        if len(set(tickers)) != len(tickers):
            raise ValueError("Duplicate company ticker in research list")
        return v
