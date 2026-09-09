"""Seed only official, source-backed records. Run: PYTHONPATH=backend python scripts/seed_data.py"""
from datetime import date
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.core import Milestone, MilestoneState, ProjectHistory, PublicationStatus, ProjectStatus, ProjectType
from app.schemas.projects import ProjectCreate, SourceIn
from app.services.projects import create_project
Base.metadata.create_all(bind=engine)
# PIB's 29 February 2024 Cabinet release is the evidence record for all entries below.
SOURCE_URL="https://www.pib.gov.in/PressReleasePage.aspx?PRID=2011415"
records=[
 {"project_name":"Tata Electronics Semiconductor Fab, Dholera","company_name":"Tata Electronics","state":"Gujarat","city":"Dholera","project_type":"Semiconductor Fab","status":"APPROVED","investment_inr":910000000000,"technology":"28 nm, 50 nm, 55 nm and 110 nm process technologies stated in the approval release.","capacity":50000,"capacity_unit":"wafers per month","approval_date":"2024-02-29","announcement_date":"2024-02-29","employment_estimate":26000},
 {"project_name":"Tata Electronics Semiconductor Assembly and Test Facility, Morigaon","company_name":"Tata Electronics","state":"Assam","city":"Morigaon","project_type":"ATMP","status":"APPROVED","investment_inr":270000000000,"capacity":48000000,"capacity_unit":"chips per day","approval_date":"2024-02-29","announcement_date":"2024-02-29","employment_estimate":27000},
 {"project_name":"CG Power Renesas Thailand Stars Microelectronics OSAT Facility, Sanand","company_name":"CG Power and Industrial Solutions","state":"Gujarat","city":"Sanand","project_type":"OSAT","status":"APPROVED","investment_inr":76000000000,"capacity":15000000,"capacity_unit":"chips per day","approval_date":"2024-02-29","announcement_date":"2024-02-29","employment_estimate":5000,"partners":"Renesas Electronics Corporation and Stars Microelectronics Public Company Limited"},
]
db=SessionLocal()
try:
 for row in records:
  if db.query(__import__('app.models.core',fromlist=['Project']).Project).filter_by(project_name=row['project_name']).first(): continue
  row['last_verified_at']=date(2024,2,29).isoformat(); row['publication_status']='PUBLISHED'; row['confidence']='HIGH'
  values=ProjectCreate(**row,sources=[SourceIn(source_type="PIB",publisher="Press Information Bureau, Government of India",title="Cabinet approves establishment of three semiconductor units under ‘Development of Semiconductors and Display Manufacturing Ecosystem in India’",url=SOURCE_URL,publication_date=date(2024,2,29),reliability="HIGH")])
  project=create_project(db,values)
  source=project.sources[0]
  db.add(Milestone(project_id=project.id,name="Government approval",state=MilestoneState.COMPLETE,milestone_date=project.approval_date,source_id=source.id))
  db.add(ProjectHistory(project_id=project.id,field_name="status",old_value=None,new_value=project.status.value,change_date=project.approval_date or project.announcement_date,source_id=source.id,notes="Initial source-backed record."))
 db.commit()
finally: db.close()
