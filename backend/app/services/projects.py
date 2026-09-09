from datetime import date
from slugify import slugify
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload
from app.models.core import Company, Location, Project, ProjectHistory, PublicationStatus, Source
from app.schemas.projects import ProjectCreate, ProjectUpdate
TRACKED_FIELDS={"status","investment_inr","capacity","expected_production_date","actual_construction_start_date","employment_estimate","partners"}
def unique_slug(db:Session, value:str)->str:
    base=slugify(value); slug=base; n=2
    while db.scalar(select(Project).where(Project.slug==slug)): slug=f"{base}-{n}"; n+=1
    return slug
def project_query(): return select(Project).options(selectinload(Project.company),selectinload(Project.location),selectinload(Project.sources),selectinload(Project.milestones),selectinload(Project.history))
def create_project(db:Session, data:ProjectCreate)->Project:
    company=db.scalar(select(Company).where(Company.name==data.company_name)) or Company(name=data.company_name,slug=slugify(data.company_name))
    location=db.scalar(select(Location).where(Location.state==data.state,Location.city==data.city,Location.district==data.district)) or Location(state=data.state,city=data.city,district=data.district)
    db.add_all([company,location]); db.flush(); values=data.model_dump(exclude={"company_name","state","city","district","sources"})
    project=Project(**values,slug=unique_slug(db,data.project_name),company_id=company.id,location_id=location.id)
    db.add(project); db.flush(); db.add_all([Source(project_id=project.id,**source.model_dump()) for source in data.sources]); db.commit(); return db.scalar(project_query().where(Project.id==project.id))
def update_project(db:Session, project:Project, data:ProjectUpdate)->Project:
    for field,value in data.model_dump(exclude_unset=True).items():
        old=getattr(project,field)
        if old != value:
            setattr(project,field,value)
            if field in TRACKED_FIELDS: db.add(ProjectHistory(project_id=project.id,field_name=field,old_value=str(old.value if hasattr(old,'value') else old) if old is not None else None,new_value=str(value.value if hasattr(value,'value') else value) if value is not None else None,change_date=date.today()))
    db.commit(); return db.scalar(project_query().where(Project.id==project.id))
def add_source(db:Session,project:Project,source_data):
    source=Source(project_id=project.id,**source_data.model_dump()); db.add(source); db.commit(); db.refresh(source); return source
