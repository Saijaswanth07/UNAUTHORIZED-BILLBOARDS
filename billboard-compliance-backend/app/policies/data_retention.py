from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
from sqlalchemy.orm import Session
from .. import models

class DataRetentionPolicy:
    """
    Handles data retention and automatic cleanup of sensitive data.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the data retention policy.
        
        Args:
            config: Configuration dictionary with retention periods
        """
        self.config = config or {
            'report_retention_days': 365,  # Keep reports for 1 year
            'anonymize_reports_after_days': 30,  # Anonymize personal data after 30 days
            'delete_original_images_after_days': 30,  # Delete original images after processing
            'keep_processed_data_days': 90,  # Keep processed data (no images) for 90 days
            'audit_log_retention_days': 365 * 2,  # Keep audit logs for 2 years
        }
        self.logger = logging.getLogger(__name__)
    
    def anonymize_report(self, db: Session, report_id: int) -> bool:
        """
        Anonymize a report by removing personal data.
        
        Args:
            db: Database session
            report_id: ID of the report to anonymize
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            report = db.query(models.Report).filter(models.Report.id == report_id).first()
            if not report:
                return False
                
            # Remove or anonymize personal data
            if hasattr(report, 'device_id'):
                report.device_id = f"anonymized_{report.id}"
                
            if hasattr(report, 'ip_address'):
                report.ip_address = "0.0.0.0"
                
            if hasattr(report, 'user_agent'):
                report.user_agent = "anonymized"
                
            db.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Error anonymizing report {report_id}: {str(e)}")
            db.rollback()
            return False
    
    def delete_old_data(self, db: Session) -> Dict[str, int]:
        """
        Delete old data according to retention policy.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with counts of deleted/anonymized items
        """
        result = {
            'anonymized_reports': 0,
            'deleted_reports': 0,
            'deleted_original_images': 0,
            'deleted_audit_logs': 0,
        }
        
        try:
            # Anonymize old reports
            anonymize_date = datetime.utcnow() - timedelta(
                days=self.config['anonymize_reports_after_days']
            )
            
            old_reports = db.query(models.Report).filter(
                models.Report.created_at < anonymize_date,
                models.Report.is_anonymized == False  # noqa: E712
            ).all()
            
            for report in old_reports:
                if self.anonymize_report(db, report.id):
                    report.is_anonymized = True
                    db.commit()
                    result['anonymized_reports'] += 1
            
            # Delete very old reports
            delete_date = datetime.utcnow() - timedelta(
                days=self.config['report_retention_days']
            )
            
            old_reports = db.query(models.Report).filter(
                models.Report.created_at < delete_date
            ).all()
            
            for report in old_reports:
                # Delete associated files
                if report.image_path and hasattr(report, 'is_original_image_deleted') \
                   and not report.is_original_image_deleted:
                    try:
                        # Delete the file from storage
                        # Implementation depends on your storage solution
                        # e.g., os.remove(report.image_path)
                        report.is_original_image_deleted = True
                        result['deleted_original_images'] += 1
                    except Exception as e:
                        self.logger.error(f"Error deleting image {report.image_path}: {str(e)}")
                
                db.delete(report)
                result['deleted_reports'] += 1
            
            # Delete old audit logs
            audit_log_date = datetime.utcnow() - timedelta(
                days=self.config['audit_log_retention_days']
            )
            
            old_logs = db.query(models.AuditLog).filter(
                models.AuditLog.timestamp < audit_log_date
            ).delete(synchronize_session=False)
            
            result['deleted_audit_logs'] = old_logs
            db.commit()
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in data retention cleanup: {str(e)}")
            db.rollback()
            return result
    
    def get_retention_summary(self) -> Dict:
        """
        Get a summary of the current retention policy.
        
        Returns:
            Dictionary with retention policy details
        """
        return {
            'policy': {
                'report_retention_days': self.config['report_retention_days'],
                'anonymize_reports_after_days': self.config['anonymize_reports_after_days'],
                'delete_original_images_after_days': self.config['delete_original_images_after_days'],
                'keep_processed_data_days': self.config['keep_processed_data_days'],
                'audit_log_retention_days': self.config['audit_log_retention_days'],
            },
            'last_run': datetime.utcnow().isoformat(),
            'next_run': (datetime.utcnow() + timedelta(days=1)).isoformat(),
        }
