"""Pydantic models for public API schemas.

This module contains Pydantic models used for request/response validation
in the public API endpoints.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class HeatmapPoint(BaseModel):
    """Heatmap data point for billboard violations"""
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    weight: float = Field(1.0, description="Weight/intensity of the point")
    violation_type: str = Field(..., description="Type of violation")
    severity: str = Field(..., description="Severity level (low/medium/high)")
    date: str = Field(..., description="ISO formatted date of the violation")

class ViolationStats(BaseModel):
    """Statistics about violations"""
    total: int = Field(..., description="Total number of violations")
    by_type: Dict[str, int] = Field(
        ...,
        description="Count of violations by type"
    )
    by_severity: Dict[str, int] = Field(
        ...,
        description="Count of violations by severity"
    )

class ActivityItem(BaseModel):
    """Recent activity item"""
    id: str = Field(..., description="Unique identifier")
    type: str = Field(..., description="Type of activity")
    description: str = Field(..., description="Description of the activity")
    timestamp: datetime = Field(
        ...,
        description="When the activity occurred"
    )
    location: Optional[Dict[str, float]] = Field(
        None,
        description=(
            "Geographic location if applicable, "
            "contains 'lat' and 'lng' keys"
        )
    )

class PublicStats(BaseModel):
    """Public statistics and metrics"""
    total_violations: int = Field(
        ...,
        description="Total number of violations"
    )
    violations_by_type: Dict[str, int] = Field(
        ...,
        description="Count of violations by type"
    )
    violations_by_severity: Dict[str, int] = Field(
        ...,
        description="Count of violations by severity"
    )
    recent_activity: List[Dict[str, Any]] = Field(
        ...,
        description="Recent activities"
    )

class LeaderboardUser(BaseModel):
    """User ranking on the leaderboard"""
    user_id: str = Field(..., description="User ID")
    username: str = Field(..., description="Display name")
    score: int = Field(..., description="Total points")
    reports: int = Field(..., description="Number of reports submitted")
    rank: int = Field(..., description="Current ranking position")

class RewardTier(BaseModel):
    """Reward tier definition"""
    name: str = Field(..., description="Name of the tier")
    points_required: int = Field(
        ...,
        description="Points needed to reach this tier"
    )
    benefits: List[str] = Field(
        ...,
        description="List of benefits at this tier"
    )