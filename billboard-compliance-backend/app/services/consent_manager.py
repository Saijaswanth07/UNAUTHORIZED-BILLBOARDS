from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from .. import models
from ..schemas.consent import ConsentCreate, ConsentUpdate, ConsentStatus
from ..utils.audit_logger import AuditLogger, AuditAction

class ConsentManager:
    """
    Manages user consents and permissions for data processing.
    """
    
    def __init__(self, db: Session, audit_logger: Optional[AuditLogger] = None):
        """
        Initialize the ConsentManager.
        
        Args:
            db: Database session
            audit_logger: Optional audit logger instance
        """
        self.db = db
        self.audit_logger = audit_logger or AuditLogger(db)
    
    def get_user_consents(
        self, 
        user_id: int, 
        active_only: bool = True
    ) -> List[models.Consent]:
        """
        Get all consents for a user.
        
        Args:
            user_id: ID of the user
            active_only: Whether to return only active consents
            
        Returns:
            List of Consent objects
        """
        query = self.db.query(models.Consent).filter(
            models.Consent.user_id == user_id
        )
        
        if active_only:
            query = query.filter(
                models.Consent.status == ConsentStatus.ACTIVE,
                models.Consent.expires_at > datetime.utcnow()
            )
            
        return query.all()
    
    def get_consent(
        self, 
        consent_id: int, 
        user_id: Optional[int] = None
    ) -> Optional[models.Consent]:
        """
        Get a specific consent by ID.
        
        Args:
            consent_id: ID of the consent
            user_id: Optional user ID to verify ownership
            
        Returns:
            Consent object if found, None otherwise
        """
        query = self.db.query(models.Consent).filter(
            models.Consent.id == consent_id
        )
        
        if user_id is not None:
            query = query.filter(models.Consent.user_id == user_id)
            
        return query.first()
    
    def create_consent(
        self, 
        consent_data: ConsentCreate, 
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.Consent:
        """
        Create a new consent record.
        
        Args:
            consent_data: Consent data
            user_id: ID of the user giving consent
            ip_address: IP address of the user
            user_agent: User agent string
            
        Returns:
            Created Consent object
        """
        # Check for existing active consent of the same type
        existing = self.db.query(models.Consent).filter(
            models.Consent.user_id == user_id,
            models.Consent.consent_type == consent_data.consent_type,
            models.Consent.status == ConsentStatus.ACTIVE,
            models.Consent.expires_at > datetime.utcnow()
        ).first()
        
        if existing:
            # Update existing consent
            return self.update_consent(
                consent_id=existing.id,
                consent_data=ConsentUpdate(
                    status=consent_data.status,
                    expires_at=consent_data.expires_at,
                    version=consent_data.version,
                    metadata=consent_data.metadata
                ),
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        # Create new consent
        db_consent = models.Consent(
            **consent_data.dict(),
            user_id=user_id,
            granted_at=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.add(db_consent)
        self.db.commit()
        self.db.refresh(db_consent)
        
        # Log the consent action
        if self.audit_logger:
            self.audit_logger.log(
                action=AuditAction.CREATE,
                resource_type="consent",
                resource_id=str(db_consent.id),
                user_id=user_id,
                details={
                    "consent_type": db_consent.consent_type,
                    "status": db_consent.status,
                    "version": db_consent.version
                },
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        return db_consent
    
    def update_consent(
        self, 
        consent_id: int, 
        consent_data: ConsentUpdate,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.Consent:
        """
        Update an existing consent.
        
        Args:
            consent_id: ID of the consent to update
            consent_data: Updated consent data
            user_id: ID of the user updating the consent
            ip_address: IP address of the user
            user_agent: User agent string
            
        Returns:
            Updated Consent object
        """
        db_consent = self.get_consent(consent_id, user_id)
        if not db_consent:
            raise ValueError("Consent not found")
        
        # Store previous values for audit
        previous_status = db_consent.status
        
        # Update fields
        update_data = consent_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_consent, field, value)
        
        db_consent.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_consent)
        
        # Log the update
        if self.audit_logger:
            self.audit_logger.log(
                action=AuditAction.UPDATE,
                resource_type="consent",
                resource_id=str(consent_id),
                user_id=user_id,
                details={
                    "previous_status": previous_status,
                    "new_status": db_consent.status,
                    "updated_fields": list(update_data.keys())
                },
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        return db_consent
    
    def revoke_consent(
        self, 
        consent_id: int, 
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.Consent:
        """
        Revoke a consent by setting its status to REVOKED.
        
        Args:
            consent_id: ID of the consent to revoke
            user_id: ID of the user revoking the consent
            ip_address: IP address of the user
            user_agent: User agent string
            
        Returns:
            Updated Consent object
        """
        return self.update_consent(
            consent_id=consent_id,
            consent_data=ConsentUpdate(status=ConsentStatus.REVOKED),
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    def has_consent(
        self, 
        user_id: int, 
        consent_type: str,
        require_active: bool = True
    ) -> bool:
        """
        Check if a user has given consent for a specific type.
        
        Args:
            user_id: ID of the user
            consent_type: Type of consent to check
            require_active: Whether to check for active consents only
            
        Returns:
            bool: True if consent is given, False otherwise
        """
        query = self.db.query(models.Consent).filter(
            models.Consent.user_id == user_id,
            models.Consent.consent_type == consent_type,
            models.Consent.status == ConsentStatus.ACTIVE,
            models.Consent.expires_at > datetime.utcnow()
        )
        
        if not require_active:
            query = query.filter(
                models.Consent.status.in_([ConsentStatus.ACTIVE, ConsentStatus.EXPIRED])
            )
        
        return query.first() is not None
    
    def get_required_consents(
        self,
        feature: str,
        version: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get the list of required consents for a specific feature.
        
        Args:
            feature: Name of the feature
            version: Optional version of the feature
            
        Returns:
            List of required consents with their descriptions
        """
        # This could be loaded from a configuration file or database
        CONSENT_REQUIREMENTS = {
            "photo_upload": [
                {
                    "type": "privacy_policy",
                    "title": "Privacy Policy",
                    "description": "Agree to our privacy policy and data processing terms.",
                    "required": True,
                    "default_expiry_days": 365
                },
                {
                    "type": "location_tracking",
                    "title": "Location Services",
                    "description": "Allow us to access your location to tag reports with geolocation data.",
                    "required": False,
                    "default_expiry_days": 90
                },
                {
                    "type": "camera_access",
                    "title": "Camera Access",
                    "description": "Allow access to your camera to take photos of billboards.",
                    "required": True,
                    "default_expiry_days": 365
                }
            ],
            "analytics": [
                {
                    "type": "usage_statistics",
                    "title": "Usage Statistics",
                    "description": "Allow us to collect anonymous usage statistics to improve our service.",
                    "required": False,
                    "default_expiry_days": 365
                }
            ]
        }
        
        return CONSENT_REQUIREMENTS.get(feature, [])
    
    def check_feature_access(
        self, 
        user_id: int, 
        feature: str,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check if a user has all required consents for a feature.
        
        Args:
            user_id: ID of the user
            feature: Name of the feature
            version: Optional version of the feature
            
        Returns:
            Dictionary with access information
        """
        required_consents = self.get_required_consents(feature, version)
        
        result = {
            "has_access": True,
            "missing_consents": [],
            "required_consents": []
        }
        
        for consent_req in required_consents:
            consent_type = consent_req["type"]
            is_required = consent_req.get("required", True)
            
            result["required_consents"].append({
                "type": consent_type,
                "title": consent_req.get("title", ""),
                "description": consent_req.get("description", ""),
                "required": is_required,
                "granted": self.has_consent(user_id, consent_type)
            })
            
            if is_required and not self.has_consent(user_id, consent_type):
                result["has_access"] = False
                result["missing_consents"].append(consent_type)
        
        return result
