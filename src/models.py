from pydantic import BaseModel, Field
from typing import List, Optional

class FinancialMetric(BaseModel):
    name: str = Field(description="Name of the financial metric or KPI (e.g., Revenue, EBITDA, Net Profit)")
    value: str = Field(description="Value of the metric including currency or unit (e.g., 120M EUR, 5.4%)")
    year: Optional[str] = Field(description="The year associated with the financial metric")
    context: Optional[str] = Field(description="Additional context or details regarding the metric")

class BusinessReportSummary(BaseModel):
    company_name: str = Field(description="Name of the company")
    report_type: str = Field(description="Type of the report (e.g., Annual Report, Quarterly Report, Sustainability Statement)")
    reporting_period: str = Field(description="Reporting period (e.g., Financial Year 2025)")
    key_metrics: List[FinancialMetric] = Field(description="List of key financial or operational metrics")
    summary: str = Field(description="A concise summary of the key findings in the document")
    challenges_or_risks: List[str] = Field(description="Challenges, risks, or future outlooks mentioned in the document")
