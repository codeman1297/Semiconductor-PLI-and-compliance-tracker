from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.core import Confidence, MilestoneState, ProjectStatus, ProjectType, PublicationStatus, SourceType
class SourceIn(BaseModel): source_type: SourceType; publisher: str; title: str; url: str; publication_date: date|None=None; reliability: Confidence=Confidence.MEDIUM; notes: str|None=None
class SourceOut(SourceIn): id:int; model_config=ConfigDict(from_attributes=True)
class MilestoneOut(BaseModel): id:int; name:str; state:MilestoneState; milestone_date:date|None=None; notes:str|None=None; model_config=ConfigDict(from_attributes=True)
class HistoryOut(BaseModel): id:int; field_name:str; old_value:str|None; new_value:str|None; change_date:date; notes:str|None=None; model_config=ConfigDict(from_attributes=True)
class ProjectBase(BaseModel):
    project_name:str=Field(min_length=2,max_length=255); company_name:str=Field(min_length=2); state:str=Field(min_length=2); city:str|None=None; district:str|None=None; project_type:ProjectType; status:ProjectStatus; publication_status:PublicationStatus=PublicationStatus.DRAFT; confidence:Confidence=Confidence.MEDIUM; investment_inr:Decimal|None=Field(default=None,ge=0); capacity:Decimal|None=Field(default=None,ge=0); capacity_unit:str|None=None; capacity_description:str|None=None; expected_production_date:date|None=None; actual_construction_start_date:date|None=None; employment_estimate:int|None=Field(default=None,ge=0); technology:str|None=None; partners:str|None=None; government_support:str|None=None; announcement_date:date|None=None; approval_date:date|None=None; last_verified_at:date|None=None
    @model_validator(mode="after")
    def chronological_dates(self):
        if self.expected_production_date and self.announcement_date and self.expected_production_date < self.announcement_date: raise ValueError("Expected production cannot precede announcement date")
        return self
class ProjectCreate(ProjectBase): sources:list[SourceIn]=Field(min_length=1)
class ProjectUpdate(BaseModel):
    project_name:str|None=None; status:ProjectStatus|None=None; publication_status:PublicationStatus|None=None; confidence:Confidence|None=None; investment_inr:Decimal|None=Field(default=None,ge=0); capacity:Decimal|None=Field(default=None,ge=0); capacity_unit:str|None=None; expected_production_date:date|None=None; actual_construction_start_date:date|None=None; employment_estimate:int|None=Field(default=None,ge=0); partners:str|None=None; last_verified_at:date|None=None
class CompanyOut(BaseModel): id:int; name:str; slug:str; website:str|None=None; model_config=ConfigDict(from_attributes=True)
class LocationOut(BaseModel): state:str; city:str|None=None; district:str|None=None; model_config=ConfigDict(from_attributes=True)
class ProjectListOut(BaseModel): id:int; slug:str; project_name:str; project_type:ProjectType; status:ProjectStatus; publication_status:PublicationStatus; confidence:Confidence; investment_inr:Decimal|None; capacity:Decimal|None; capacity_unit:str|None; expected_production_date:date|None; last_verified_at:date|None; company:CompanyOut; location:LocationOut; model_config=ConfigDict(from_attributes=True)
class ProjectDetailOut(ProjectListOut): technology:str|None; capacity_description:str|None; actual_construction_start_date:date|None; employment_estimate:int|None; partners:str|None; government_support:str|None; announcement_date:date|None; approval_date:date|None; sources:list[SourceOut]; milestones:list[MilestoneOut]; history:list[HistoryOut]
class PaginatedProjects(BaseModel): items:list[ProjectListOut]; total:int; page:int; page_size:int
