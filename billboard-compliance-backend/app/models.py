from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    INSPECTOR = "inspector"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.CITIZEN)
    is_active = Column(Boolean, default=True)
    
    reports = relationship("Report", back_populates="reporter")
    violations = relationship("Violation", back_populates="reporter")

class Billboard(Base):
    __tablename__ = "billboards"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String)
    width = Column(Float)  # in meters
    height = Column(Float)  # in meters
    is_permitted = Column(Boolean, default=False)
    permit_number = Column(String, nullable=True)
    owner_name = Column(String)
    owner_contact = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    reports = relationship("Report", back_populates="billboard")
    violations = relationship("Violation", back_populates="billboard")

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    REJECTED = "rejected"

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    billboard_id = Column(Integer, ForeignKey("billboards.id"))
    reporter_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    description = Column(String)
    image_url = Column(String)
    video_url = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    billboard = relationship("Billboard", back_populates="reports")
    reporter = relationship("User", back_populates="reports")
    violations = relationship("Violation", back_populates="report")

class ViolationType(str, enum.Enum):
    UNAUTHORIZED = "unauthorized"
    SIZE_VIOLATION = "size_violation"
    LOCATION_VIOLATION = "location_violation"
    STRUCTURAL_ISSUE = "structural_issue"
    CONTENT_VIOLATION = "content_violation"
    EXPIRED_PERMIT = "expired_permit"

class Violation(Base):
    __tablename__ = "violations"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    billboard_id = Column(Integer, ForeignKey("billboards.id"))
    reporter_id = Column(Integer, ForeignKey("users.id"))
    violation_type = Column(Enum(ViolationType))
    description = Column(String)
    severity = Column(String)  # low, medium, high
    status = Column(String, default="reported")  # reported, confirmed, resolved
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    report = relationship("Report", back_populates="violations")
    billboard = relationship("Billboard", back_populates="violations")
    reporter = relationship("User", back_populates="violations")
