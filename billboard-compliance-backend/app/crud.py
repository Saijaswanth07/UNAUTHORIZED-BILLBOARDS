from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime
from . import models, schemas, auth
from .database import get_db
from .config import settings
from typing import List

router = APIRouter()

# File upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Billboard operations
@router.post("/billboards/", response_model=schemas.Billboard)
def create_billboard(
    billboard: schemas.BillboardCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role not in ["inspector", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create billboard"
        )
    db_billboard = models.Billboard(**billboard.dict())
    db.add(db_billboard)
    db.commit()
    db.refresh(db_billboard)
    return db_billboard

@router.get("/billboards/", response_model=List[schemas.Billboard])
def read_billboards(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    billboards = db.query(models.Billboard).offset(skip).limit(limit).all()
    return billboards

# Report operations
@router.post("/reports/", response_model=schemas.Report)
async def create_report(
    report: schemas.ReportCreate,
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Save image if provided
    image_url = None
    if image:
        file_extension = os.path.splitext(image.filename)[1]
        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/{UPLOAD_DIR}/{filename}"
    
    # Create report
    db_report = models.Report(
        **report.dict(),
        reporter_id=current_user.id,
        image_url=image_url,
        status=schemas.ReportStatus.PENDING
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # TODO: Add billboard detection and violation checking logic
    
    return db_report

@router.get("/reports/", response_model=List[schemas.Report])
def read_reports(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role == "admin":
        reports = db.query(models.Report).offset(skip).limit(limit).all()
    else:
        reports = db.query(models.Report).filter(
            models.Report.reporter_id == current_user.id
        ).offset(skip).limit(limit).all()
    return reports

# Violation operations
@router.post("/violations/", response_model=schemas.Violation)
def create_violation(
    violation: schemas.ViolationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Check if the user has permission to create violations
    if current_user.role not in ["inspector", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create violation"
        )
    
    # Create violation
    db_violation = models.Violation(
        **violation.dict(),
        reporter_id=current_user.id,
        status="reported"
    )
    
    db.add(db_violation)
    db.commit()
    db.refresh(db_violation)
    
    # Update report status
    report = db.query(models.Report).filter(
        models.Report.id == violation.report_id
    ).first()
    
    if report:
        report.status = schemas.ReportStatus.IN_REVIEW
        db.commit()
    
    return db_violation

@router.get("/violations/", response_model=List[schemas.Violation])
def read_violations(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role == "admin":
        violations = db.query(models.Violation).offset(skip).limit(limit).all()
    else:
        violations = db.query(models.Violation).filter(
            models.Violation.reporter_id == current_user.id
        ).offset(skip).limit(limit).all()
    return violations
