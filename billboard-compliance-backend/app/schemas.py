from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "citizen"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class BillboardBase(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    is_permitted: bool = False
    permit_number: Optional[str] = None
    owner_name: Optional[str] = None
    owner_contact: Optional[str] = None

class BillboardCreate(BillboardBase):
    pass

class Billboard(BillboardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReportStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class ReportBase(BaseModel):
    billboard_id: int
    description: str
    latitude: float
    longitude: float

class ReportCreate(ReportBase):
    pass

class Report(ReportBase):
    id: int
    reporter_id: int
    status: ReportStatus
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ViolationType(str, Enum):
    UNAUTHORIZED = "unauthorized"
    SIZE_VIOLATION = "size_violation"
    LOCATION_VIOLATION = "location_violation"
    STRUCTURAL_ISSUE = "structural_issue"
    CONTENT_VIOLATION = "content_violation"
    EXPIRED_PERMIT = "expired_permit"

class ViolationBase(BaseModel):
    report_id: int
    billboard_id: int
    violation_type: ViolationType
    description: str
    severity: str  # low, medium, high

class ViolationCreate(ViolationBase):
    pass

class Violation(ViolationBase):
    id: int
    reporter_id: int
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
