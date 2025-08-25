import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from sqlalchemy.orm import Session
from .. import models

class AuditAction(str, Enum):
    """Enumeration of possible audit actions"""
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    ACCESS_DENIED = "access_denied"
    ERROR = "error"

class AuditLogger:
    """
    A class to handle audit logging for the application.
    Logs to both database and application log file.
    """
    
    def __init__(self, db: Session, logger_name: str = 'audit'):
        """
        Initialize the audit logger.
        
        Args:
            db: SQLAlchemy database session
            logger_name: Name for the logger instance
        """
        self.db = db
        self.logger = logging.getLogger(logger_name)
        
    def _log_to_database(
        self,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success"
    ) -> None:
        """
        Log an action to the database.
        
        Args:
            action: Type of action being logged
            resource_type: Type of resource being accessed/modified
            resource_id: ID of the resource (if applicable)
            user_id: ID of the user performing the action
            details: Additional details about the action
            ip_address: IP address of the requester
            user_agent: User agent string of the requester
            status: Status of the action (success/failure)
        """
        try:
            log_entry = models.AuditLog(
                action=action.value,
                resource_type=resource_type,
                resource_id=str(resource_id) if resource_id else None,
                user_id=user_id,
                details=details or {},
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                timestamp=datetime.utcnow()
            )
            self.db.add(log_entry)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to log to database: {str(e)}")
    
    def _log_to_file(
        self,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        status: str = "success"
    ) -> None:
        """
        Log an action to the application log file.
        
        Args:
            action: Type of action being logged
            resource_type: Type of resource being accessed/modified
            resource_id: ID of the resource (if applicable)
            user_id: ID of the user performing the action
            details: Additional details about the action
            ip_address: IP address of the requester
            status: Status of the action (success/failure)
        """
        log_message = (
            f"action={action.value} "
            f"resource_type={resource_type} "
            f"resource_id={resource_id or 'N/A'} "
            f"user_id={user_id or 'anonymous'} "
            f"ip={ip_address or 'unknown'} "
            f"status={status}"
        )
        
        if details:
            log_message += f" details={details}"
        
        if status == "failure":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
    
    def log(
        self,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        log_to_db: bool = True,
        log_to_file: bool = True
    ) -> None:
        """
        Log an action to the configured log destinations.
        
        Args:
            action: Type of action being logged
            resource_type: Type of resource being accessed/modified
            resource_id: ID of the resource (if applicable)
            user_id: ID of the user performing the action
            details: Additional details about the action
            ip_address: IP address of the requester
            user_agent: User agent string of the requester
            status: Status of the action (success/failure)
            log_to_db: Whether to log to the database
            log_to_file: Whether to log to the application log file
        """
        if log_to_db:
            self._log_to_database(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                user_id=user_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent,
                status=status
            )
        
        if log_to_file:
            self._log_to_file(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                user_id=user_id,
                details=details,
                ip_address=ip_address,
                status=status
            )
    
    def get_recent_logs(
        self,
        limit: int = 100,
        user_id: Optional[int] = None,
        action: Optional[AuditAction] = None,
        resource_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[models.AuditLog]:
        """
        Retrieve recent audit logs with optional filtering.
        
        Args:
            limit: Maximum number of logs to return
            user_id: Filter by user ID
            action: Filter by action type
            resource_type: Filter by resource type
            status: Filter by status (success/failure)
            
        Returns:
            List of AuditLog objects matching the criteria
        """
        query = self.db.query(models.AuditLog)
        
        if user_id is not None:
            query = query.filter(models.AuditLog.user_id == user_id)
            
        if action is not None:
            query = query.filter(models.AuditLog.action == action.value)
            
        if resource_type is not None:
            query = query.filter(models.AuditLog.resource_type == resource_type)
            
        if status is not None:
            query = query.filter(models.AuditLog.status == status)
        
        return query.order_by(models.AuditLog.timestamp.desc()).limit(limit).all()
