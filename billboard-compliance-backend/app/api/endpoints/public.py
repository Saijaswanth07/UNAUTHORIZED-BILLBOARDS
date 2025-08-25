from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ... import models, schemas
from ...database import get_db
from ...core.config import settings

router = APIRouter()

@router.get("/heatmap", response_model=List[schemas.HeatmapPoint])
async def get_heatmap_data(
    days: int = 30,
    violation_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get heatmap data for flagged billboards within the specified time range.
    
    - **days**: Number of days of data to include (default: 30)
    - **violation_type**: Filter by specific violation type if needed
    """
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Build base query
    query = db.query(
        models.Report.latitude,
        models.Report.longitude,
        models.Violation.type,
        models.Violation.severity,
        models.Report.created_at
    ).join(
        models.Violation,
        models.Report.id == models.Violation.report_id
    ).filter(
        models.Report.status == 'verified',
        models.Report.created_at.between(start_date, end_date)
    )
    
    # Apply filters if provided
    if violation_type:
        query = query.filter(models.Violation.type == violation_type)
    
    # Convert to heatmap points
    heatmap_data = []
    for point in query.all():
        heatmap_data.append({
            "latitude": point.latitude,
            "longitude": point.longitude,
            "weight": 1,  # Can be adjusted based on severity
            "violation_type": point.type,
            "severity": point.severity,
            "date": point.created_at.isoformat()
        })
    
    return heatmap_data

@router.get("/stats", response_model=schemas.PublicStats)
async def get_public_stats(db: Session = Depends(get_db)):
    """
    Get public statistics about billboard violations
    """
    # Get total violations
    total_violations = db.query(models.Violation).count()
    
    # Get violations by type
    violations_by_type = db.query(
        models.Violation.type,
        models.func.count(models.Violation.id)
    ).group_by(models.Violation.type).all()
    
    # Get violations by severity
    violations_by_severity = db.query(
        models.Violation.severity,
        models.func.count(models.Violation.id)
    ).group_by(models.Violation.severity).all()
    
    # Get recent activity
    recent_activity = db.query(
        models.Report
    ).order_by(
        models.Report.created_at.desc()
    ).limit(10).all()
    
    return {
        "total_violations": total_violations,
        "violations_by_type": dict(violations_by_type),
        "violations_by_severity": dict(violations_by_severity),
        "recent_activity": recent_activity
    }
