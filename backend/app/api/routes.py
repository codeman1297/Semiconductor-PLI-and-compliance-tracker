from datetime import date, timedelta
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.config import get_settings
from app.db.session import get_db
from app.models.core import Company, Project, ProjectHistory, ProjectStatus, ProjectType, PublicationStatus, Source
from app.schemas.projects import CompanyOut, PaginatedProjects, ProjectCreate, ProjectDetailOut, ProjectListOut, ProjectUpdate, SourceIn, SourceOut
from app.services.projects import add_source, create_project, project_query, update_project
router=APIRouter(prefix="/api")
def admin_key(x_admin_key:str|None=Header(default=None)):
    if x_admin_key != get_settings().admin_api_key: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Admin credentials required")
def get_project_or_404(slug:str,db:Session):
    project=db.scalar(project_query().where(Project.slug==slug))
    if not project: raise HTTPException(404,"Project not found")
    return project
@router.get("/projects",response_model=PaginatedProjects)
def list_projects(q:str|None=None,status:ProjectStatus|None=None,state:str|None=None,project_type:ProjectType|None=None,company:str|None=None,year:int|None=None,sort:str="last_verified",page:int=Query(1,ge=1),page_size:int=Query(20,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=project_query().where(Project.publication_status==PublicationStatus.PUBLISHED)
    if q: stmt=stmt.join(Project.company).join(Project.location).where(or_(Project.project_name.ilike(f"%{q}%"),Company.name.ilike(f"%{q}%"),__import__('app.models.core',fromlist=['Location']).Location.state.ilike(f"%{q}%")))
    if status: stmt=stmt.where(Project.status==status)
    if state: stmt=stmt.join(Project.location).where(__import__('app.models.core',fromlist=['Location']).Location.state.ilike(state))
    if project_type: stmt=stmt.where(Project.project_type==project_type)
    if company: stmt=stmt.join(Project.company).where(Company.slug==company)
    if year: stmt=stmt.where(func.extract('year',Project.expected_production_date)==year)
    order={"investment":Project.investment_inr.desc(),"expected_production":Project.expected_production_date.asc(),"status":Project.status.asc(),"last_verified":Project.last_verified_at.desc()}.get(sort,Project.last_verified_at.desc())
    total=db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery())) or 0
    return {"items":db.scalars(stmt.order_by(order).offset((page-1)*page_size).limit(page_size)).unique().all(),"total":total,"page":page,"page_size":page_size}
@router.get("/projects/{slug}",response_model=ProjectDetailOut)
def project_detail(slug:str,db:Session=Depends(get_db)): return get_project_or_404(slug,db)
@router.get("/companies",response_model=list[CompanyOut])
def companies(db:Session=Depends(get_db)): return db.scalars(select(Company).order_by(Company.name)).all()
@router.get("/states")
def states(db:Session=Depends(get_db)): return db.execute(select(__import__('app.models.core',fromlist=['Location']).Location.state,func.count(Project.id)).join(Project).where(Project.publication_status==PublicationStatus.PUBLISHED).group_by(__import__('app.models.core',fromlist=['Location']).Location.state).order_by(__import__('app.models.core',fromlist=['Location']).Location.state)).all()
@router.get("/changes")
def changes(days:int=Query(7,ge=1,le=365),db:Session=Depends(get_db)): return db.execute(select(ProjectHistory,Project.slug,Project.project_name,Source.url,Source.title).join(Project).outerjoin(Source,Source.id==ProjectHistory.source_id).where(Project.publication_status==PublicationStatus.PUBLISHED,ProjectHistory.change_date>=date.today()-timedelta(days=days)).order_by(ProjectHistory.change_date.desc())).all()
@router.get("/stats")
def stats(db:Session=Depends(get_db)):
    published=Project.publication_status==PublicationStatus.PUBLISHED
    total=db.scalar(select(func.count(Project.id)).where(published)) or 0; investment=db.scalar(select(func.coalesce(func.sum(Project.investment_inr),0)).where(published)) or 0
    return {"total_projects":total,"total_announced_investment_inr":float(investment),"under_construction":db.scalar(select(func.count(Project.id)).where(published,Project.status.in_([ProjectStatus.UNDER_CONSTRUCTION,ProjectStatus.CONSTRUCTION_STARTED]))) or 0,"operational":db.scalar(select(func.count(Project.id)).where(published,Project.status==ProjectStatus.OPERATIONAL)) or 0,"states":db.scalar(select(func.count(func.distinct(__import__('app.models.core',fromlist=['Location']).Location.state))).join(Project).where(published)) or 0,"by_status":[{"label":x[0].value,"count":x[1]} for x in db.execute(select(Project.status,func.count(Project.id)).where(published).group_by(Project.status)).all()]}
@router.post("/admin/projects",response_model=ProjectDetailOut,status_code=201,dependencies=[Depends(admin_key)])
def admin_create(data:ProjectCreate,db:Session=Depends(get_db)): return create_project(db,data)
@router.patch("/admin/projects/{slug}",response_model=ProjectDetailOut,dependencies=[Depends(admin_key)])
def admin_update(slug:str,data:ProjectUpdate,db:Session=Depends(get_db)): return update_project(db,get_project_or_404(slug,db),data)
@router.post("/admin/projects/{slug}/sources",response_model=SourceOut,status_code=201,dependencies=[Depends(admin_key)])
def admin_source(slug:str,data:SourceIn,db:Session=Depends(get_db)): return add_source(db,get_project_or_404(slug,db),data)
