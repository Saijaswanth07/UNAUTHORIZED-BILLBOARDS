from typing import Dict, List, Optional
from datetime import datetime
import logging
from ..config.compliance_rules import ComplianceConfig, ZoneType, BillboardType
from ..models import Billboard, ViolationType

class ComplianceChecker:
    """Service for checking billboard compliance against regulations."""
    
    def __init__(self, config: Optional[ComplianceConfig] = None):
        self.config = config or self._load_default_config()
        self.logger = logging.getLogger(__name__)
    
    def _load_default_config(self) -> ComplianceConfig:
        from ..config.compliance_rules import load_default_config
        return load_default_config()
    
    def check_billboard_compliance(self, billboard: Billboard, report_data: Dict) -> Dict:
        """Check if a billboard is compliant with all regulations."""
        try:
            zone = ZoneType(billboard.zone_type.lower())
            billboard_type = BillboardType(billboard.billboard_type.lower())
            
            # Get applicable rules
            rules = self.config.get_applicable_rules(zone, billboard_type)
            
            # Check each compliance category
            violations = []
            violations.extend(self._check_size(billboard, rules["size"]))
            violations.extend(self._check_location(billboard, report_data, rules["location"]))
            violations.extend(self._check_content(billboard, report_data, rules["content"]))
            violations.extend(self._check_safety(billboard, rules["safety"]))
            violations.extend(self._check_administrative(billboard, rules["administrative"]))
            
            return {
                "is_compliant": len(violations) == 0,
                "violations": violations,
                "checked_at": datetime.utcnow().isoformat(),
                "billboard_id": str(billboard.id)
            }
            
        except Exception as e:
            self.logger.error(f"Compliance check failed: {str(e)}")
            raise
    
    def _check_size(self, billboard: Billboard, rules: List) -> List[Dict]:
        """Check size compliance."""
        violations = []
        for rule in rules:
            if billboard.width_meters > rule.max_width_meters:
                violations.append(self._create_violation(rule, "Width exceeds maximum allowed"))
            if billboard.height_meters > rule.max_height_meters:
                violations.append(self._create_violation(rule, "Height exceeds maximum allowed"))
            if (billboard.width_meters * billboard.height_meters) > rule.max_area_sqm:
                violations.append(self._create_violation(rule, "Area exceeds maximum allowed"))
        return violations
    
    def _check_location(self, billboard: Billboard, report_data: Dict, rules: List) -> List[Dict]:
        """Check location compliance."""
        violations = []
        for rule in rules:
            if 'location' in report_data:
                loc = report_data['location']
                if loc.get('distance_from_intersection', float('inf')) < rule.min_distance_from_intersection:
                    violations.append(self._create_violation(rule, "Too close to intersection"))
        return violations
    
    def _check_content(self, billboard: Billboard, report_data: Dict, rules: List) -> List[Dict]:
        """Check content compliance."""
        violations = []
        if 'content_analysis' not in report_data:
            return violations
            
        for rule in rules:
            content = report_data['content_analysis']
            for prohibited in rule.prohibited_content:
                if prohibited in content.get('detected_content', {}):
                    violations.append(self._create_violation(rule, f"Prohibited content: {prohibited}"))
        return violations
    
    def _check_safety(self, billboard: Billboard, rules: List) -> List[Dict]:
        """Check safety compliance."""
        violations = []
        for rule in rules:
            if rule.requires_structural_certificate and not billboard.structural_certificate_id:
                violations.append(self._create_violation(rule, "Missing structural certificate"))
        return violations
    
    def _check_administrative(self, billboard: Billboard, rules: List) -> List[Dict]:
        """Check administrative compliance."""
        violations = []
        for rule in rules:
            if rule.requires_permit and not billboard.permit_number:
                violations.append(self._create_violation(rule, "Missing permit"))
            if hasattr(billboard, 'permit_expiry_date') and billboard.permit_expiry_date < datetime.utcnow().date():
                violations.append(self._create_violation(rule, "Permit expired"))
        return violations
    
    def _create_violation(self, rule, message: str) -> Dict:
        """Helper to create a violation dictionary."""
        return {
            "rule_id": rule.rule_id,
            "type": self._map_rule_to_violation_type(rule),
            "severity": rule.severity,
            "message": message,
            "details": {"rule_description": rule.description}
        }
    
    def _map_rule_to_violation_type(self, rule) -> str:
        """Map rule type to violation type."""
        rule_name = rule.__class__.__name__.lower()
        if 'size' in rule_name:
            return ViolationType.SIZE_VIOLATION
        elif 'location' in rule_name:
            return ViolationType.LOCATION_VIOLATION
        elif 'content' in rule_name:
            return ViolationType.CONTENT_VIOLATION
        elif 'safety' in rule_name:
            return ViolationType.SAFETY_VIOLATION
        else:
            return ViolationType.ADMINISTRATIVE_VIOLATION
