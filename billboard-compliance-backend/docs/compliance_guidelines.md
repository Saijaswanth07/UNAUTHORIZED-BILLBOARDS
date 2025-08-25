# Billboard Compliance Guidelines

## 1. Legal Framework

### 1.1 National Policies
- **Model Outdoor Advertising Policy 2016 (MoHUA)**
  - Regulates outdoor advertisements across India
  - Aims for uniformity in urban outdoor advertising
  - Defines zones for advertising (prohibited, restricted, permitted)
  - Specifies size, illumination, and safety standards

- **Municipal Corporation Acts**
  - Local municipal corporations enforce advertising regulations
  - Examples: Mumbai Municipal Corporation Act, Delhi Municipal Corporation Act
  - Requires licenses/permits for billboard installation

- **Motor Vehicles Act, 1988**
  - Regulates advertisements visible from highways
  - Prohibits distracting advertisements near roads

### 1.2 Key Regulatory Bodies
- **Ministry of Housing and Urban Affairs (MoHUA)**
- **State Urban Development Departments**
- **Local Municipal Corporations**
- **National Highways Authority of India (NHAI)**
- **Airports Authority of India (AAI)**

## 2. Violation Criteria

### 2.1 Content Violations
- Obscene, indecent, or objectionable content
- False or misleading advertisements
- Advertisements promoting illegal activities
- Unauthorized political or religious content
- Content violating cultural or religious sentiments

### 2.2 Structural Violations
| Parameter | Standard | Violation Condition |
|-----------|----------|---------------------|
| Maximum Size | 40ft x 30ft (varies by location) | Exceeding specified dimensions |
| Height from Ground | Min 2.5m pedestrian clearance | Blocking pedestrian pathways |
| Distance from Road | 1m from road boundary | Encroaching on road space |
| Distance from Intersection | 30m from junction | Obstructing visibility |
| Illumination | Non-flashing, <1000 nits at night | Causing glare/distraction |
| Structural Safety | Certified by structural engineer | No valid certification |

### 2.3 Location-Based Violations
- **Prohibited Areas**:
  - Heritage sites and monuments
  - Religious places
  - Educational institutions
  - Government buildings
  - Hospitals
  - Within 100m of historical monuments (AMASR Act, 1958)

- **Restricted Areas**:
  - Residential zones (limited size/content)
  - Within 200m of airports (height restrictions)
  - Highway corridors (NHAI guidelines)

### 2.4 Administrative Violations
- Absence of valid permit/license
- Failure to display QR code/unique ID
- Non-payment of advertisement tax
- Expired permit/license
- Unauthorized modifications to approved design

## 3. Documentation Requirements

### 3.1 Mandatory Information
- Valid permit/license number
- Owner/agency details
- Installation date and validity period
- Structural safety certificate
- Tax payment receipts
- Insurance certificate

### 3.2 Digital Verification
- QR code linking to municipal database
- Digital permit verification system
- Online payment integration for fees
- Real-time status tracking

## 4. Penalty Structure

| Violation Type | First Offense | Repeat Offense |
|----------------|---------------|-----------------|
| Unauthorized Installation | ₹25,000 + Removal | ₹50,000 + Legal Action |
| Expired Permit | 2x Renewal Fee | 5x Renewal Fee |
| Size Violation | ₹10,000 + Correction | ₹25,000 + Removal |
| Content Violation | ₹15,000 + Removal | ₹50,000 + Legal Action |
| Safety Hazard | Immediate Removal + ₹50,000 | ₹1,00,000 + Blacklist |
| Tax Evasion | 3x Tax Due | 5x Tax Due + Legal Action |

## 5. Technical Implementation Guidelines

### 5.1 Image Analysis Parameters
- Dimension verification (pixel-to-meter conversion)
- Text recognition for permit numbers
- QR code scanning for digital verification
- Obstruction analysis (pedestrian/vehicle pathways)
- Structural integrity assessment

### 5.2 Geofencing Requirements
- GPS coordinate verification
- Zone-based compliance checking
- Proximity analysis (schools, hospitals, etc.)
- Distance from road/intersection calculation

### 5.3 Data Requirements
- Municipal GIS data for zoning
- Permit/license database
- Historical violation records
- Tax payment records
- Structural safety certifications

## 6. Compliance Workflow

1. **Pre-Installation**
   - Application submission with design
   - Structural safety certification
   - Payment of fees
   - Permit issuance with QR code

2. **Post-Installation**
   - Physical verification
   - Compliance documentation upload
   - Activation of advertisement

3. **Ongoing Monitoring**
   - Regular automated checks
   - Citizen reporting mechanism
   - Periodic safety inspections
   - Renewal reminders

## 7. References
- Model Outdoor Advertising Policy 2016 (MoHUA)
- Municipal Corporation Acts (State-specific)
- Motor Vehicles Act, 1988
- Ancient Monuments and Archaeological Sites and Remains Act, 1958
- Local municipal corporation guidelines
- NHAI Outdoor Advertising Policy
- AAI Aerodrome Standards

## 8. Implementation Notes
- All measurements should be verified against local municipal regulations
- Regular updates to compliance rules should be accommodated
- Integration with municipal databases is essential for real-time verification
- Multi-language support for violation notifications
- Accessibility features for differently-abled users in reporting interface
