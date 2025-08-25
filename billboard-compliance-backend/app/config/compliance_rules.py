from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class ZoneType(str, Enum):
    PROHIBITED = "prohibited"
    RESTRICTED = "restricted"
    PERMITTED = "permitted"
    HERITAGE = "heritage"
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"

class ContentCategory(str, Enum):
    GENERAL = "general"
    POLITICAL = "political"
    RELIGIOUS = "religious"
    ALCOHOL_TOBACCO = "alcohol_tobacco"
    HEALTHCARE = "healthcare"
    ADULT = "adult"

class BillboardType(str, Enum):
    UNIPOLES = "unipoles"
    GANTRY = "gantry"
    WALL_MOUNTED = "wall_mounted"
    ROOFTOP = "rooftop"
    KIOSK = "kiosk"
    BUS_SHELTER = "bus_shelter"
    DIGITAL = "digital"
    TRADITIONAL = "traditional"

class ComplianceRule(BaseModel):
    """Base class for all compliance rules"""
    rule_id: str
    description: str
    severity: str  # "critical", "high", "medium", "low"
    applicable_zones: List[ZoneType]
    applicable_billboard_types: List[BillboardType]
    
class SizeRestriction(ComplianceRule):
    """Rules related to billboard dimensions"""
    max_width_meters: float
    max_height_meters: float
    max_area_sqm: float
    min_ground_clearance: float = 2.5  # meters
    
class LocationRestriction(ComplianceRule):
    """Rules related to billboard placement"""
    min_distance_from_intersection: float = 30.0  # meters
    min_distance_from_pedestrian_path: float = 1.0  # meters
    min_distance_from_road: float = 1.0  # meters
    prohibited_nearby_places: Dict[str, float] = Field(
        default_factory=lambda: {
            "schools": 100.0,
            "hospitals": 100.0,
            "religious_places": 50.0,
            "heritage_sites": 100.0,
        }
    )

class ContentRestriction(ComplianceRule):
    """Rules related to billboard content"""
    prohibited_content: List[str] = Field(
        default_factory=lambda: [
            "obscene",
            "defamatory",
            "inciting_violence",
            "hate_speech",
            "unauthorized_political",
        ]
    )
    required_elements: List[str] = Field(
        default_factory=lambda: [
            "permit_number",
            "owner_contact",
            "validity_date",
        ]
    )
    
class SafetyRequirement(ComplianceRule):
    """Rules related to structural and public safety"""
    requires_structural_certificate: bool = True
    max_wind_speed_rating: Optional[float] = None  # km/h
    required_illumination: Optional[str] = None
    fire_safety_requirements: List[str] = []
    
class AdministrativeRequirement(ComplianceRule):
    """Rules related to permits and documentation"""
    requires_permit: bool = True
    permit_renewal_years: int = 1
    required_insurance: bool = True
    tax_requirements: List[str] = []
    
class ComplianceConfig(BaseModel):
    """Complete compliance configuration for a jurisdiction"""
    jurisdiction: str
    effective_date: str
    size_restrictions: Dict[ZoneType, SizeRestriction]
    location_restrictions: List[LocationRestriction]
    content_restrictions: List[ContentRestriction]
    safety_requirements: List[SafetyRequirement]
    administrative_requirements: List[AdministrativeRequirement]
    
    def get_applicable_rules(
        self, 
        zone: ZoneType, 
        billboard_type: BillboardType,
        content_category: Optional[ContentCategory] = None
    ) -> Dict[str, List[ComplianceRule]]:
        """Get all rules applicable to a specific billboard"""
        def is_applicable(rule: ComplianceRule) -> bool:
            return (
                zone in rule.applicable_zones and
                billboard_type in rule.applicable_billboard_types
            )
        
        return {
            "size": [r for r in self.size_restrictions.values() if is_applicable(r)],
            "location": [r for r in self.location_restrictions if is_applicable(r)],
            "content": [r for r in self.content_restrictions if is_applicable(r)],
            "safety": [r for r in self.safety_requirements if is_applicable(r)],
            "administrative": [r for r in self.administrative_requirements if is_applicable(r)],
        }

# Example configuration for a city
def load_default_config() -> ComplianceConfig:
    return ComplianceConfig(
        jurisdiction="Example City Municipal Corporation",
        effective_date="2023-01-01",
        size_restrictions={
            ZoneType.COMMERCIAL: SizeRestriction(
                rule_id="SIZE-COMM-001",
                description="Maximum size for commercial zone billboards",
                severity="high",
                applicable_zones=[ZoneType.COMMERCIAL],
                applicable_billboard_types=[BillboardType.UNIPOLES, BillboardType.GANTRY],
                max_width_meters=12.0,
                max_height_meters=4.0,
                max_area_sqm=48.0,
                min_ground_clearance=2.5
            ),
            # Add more zone-specific size restrictions
        },
        location_restrictions=[
            LocationRestriction(
                rule_id="LOC-001",
                description="Minimum distance from intersections",
                severity="critical",
                applicable_zones=[ZoneType.PERMITTED, ZoneType.COMMERCIAL],
                applicable_billboard_types=[BillboardType.UNIPOLES, BillboardType.GANTRY],
                min_distance_from_intersection=30.0,
                min_distance_from_pedestrian_path=1.0,
                min_distance_from_road=1.0
            ),
            # Add more location restrictions
        ],
        content_restrictions=[
            ContentRestriction(
                rule_id="CONT-001",
                description="Prohibited content",
                severity="high",
                applicable_zones=[z for z in ZoneType],
                applicable_billboard_types=[bt for bt in BillboardType],
                prohibited_content=[
                    "obscene", "defamatory", "inciting_violence",
                    "hate_speech", "unauthorized_political"
                ]
            ),
            # Add more content restrictions
        ],
        safety_requirements=[
            SafetyRequirement(
                rule_id="SAFE-001",
                description="Structural safety requirements",
                severity="critical",
                applicable_zones=[z for z in ZoneType if z != ZoneType.PROHIBITED],
                applicable_billboard_types=[bt for bt in BillboardType],
                requires_structural_certificate=True,
                max_wind_speed_rating=120.0
            ),
            # Add more safety requirements
        ],
        administrative_requirements=[
            AdministrativeRequirement(
                rule_id="ADMIN-001",
                description="Permit requirements",
                severity="high",
                applicable_zones=[z for z in ZoneType if z != ZoneType.PROHIBITED],
                applicable_billboard_types=[bt for bt in BillboardType],
                requires_permit=True,
                permit_renewal_years=1,
                required_insurance=True
            ),
            # Add more administrative requirements
        ]
    )
