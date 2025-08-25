# Billboard Compliance System

A comprehensive solution for detecting and reporting non-compliant billboards using AI and citizen reporting.

## 📋 Project Deliverables

### 1. Prototype
- **Mobile App**: For citizen reporting and status tracking
- **Reporting Portal**: For compliance monitoring and management

### 2. Architecture
- [System Architecture](./docs/architecture.md)
- Data flow diagrams
- Component interactions
- Third-party integrations

### 3. Documentation
- [Technical Documentation](./docs/documentation.md)
- API References
- Deployment Guides
- User Manuals

### 4. Compliance Framework
- [Compliance Guidelines](./docs/compliance_guidelines.md)
- Violation criteria
- Legal requirements
- Best practices

## 🚀 Features

### Mobile App
- 📱 Report violations with photo/video evidence
- 📍 GPS tagging and geofencing
- 🔔 Real-time status updates
- 📊 View report history
- 🔒 Secure authentication
- 🏆 Track rewards and achievements
- 👥 Referral program

### Admin Portal
- 🖥️ Dashboard with key metrics
- 📋 Case management
- 📈 Analytics and reporting
- 👥 User and role management
- ⚙️ System configuration
- 🎯 Incentive program management

### Public Dashboard
- 🌍 Interactive heatmap of violations
- 📊 Real-time statistics
- 🏆 Leaderboard of top contributors
- 📱 Mobile-responsive design

### Backend Services
- 🏗️ RESTful API
- 🔍 AI-powered compliance checking
- 📦 File storage and management
- 🔄 Background task processing
- 🔐 Authentication and authorization
- 🎮 Gamification engine
- 📊 Analytics and reporting

## 🛠️ Tech Stack

### Frontend
- **Mobile**: React Native (iOS/Android)
- **Web**: React.js with TypeScript
- **State Management**: Redux Toolkit
- **Maps**: Mapbox GL
- **UI Components**: Material-UI

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL (relational), MongoDB (documents)
- **ORM**: SQLAlchemy, Pydantic
- **Storage**: AWS S3/Google Cloud Storage
- **Search**: Elasticsearch

### AI/ML
- **Computer Vision**: OpenCV, TensorFlow
- **NLP**: spaCy, Transformers
- **Image Processing**: PIL, scikit-image

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack
## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 13+
- Redis
- pip (Python package manager)

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/billboard-compliance-backend.git
   cd billboard-compliance-backend
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start services using Docker:
   ```bash
   docker-compose up -d --build
   ```

4. Run database migrations:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. Start the development server:
   ```bash
   docker-compose exec web uvicorn app.main:app --reload
   ```

### Frontend Setup
See the [frontend repository](https://github.com/yourusername/billboard-compliance-frontend) for setup instructions.

## 📚 Documentation

- [API Documentation](https://api.billboardcompliance.com/docs)
- [Architecture](./docs/architecture.md)
- [Compliance Guidelines](./docs/compliance_guidelines.md)
- [Technical Documentation](./docs/documentation.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Project Lead**: [Sai Jaswanth.K]
- **Backend Developer**: [Sai Jaswanth.K]
- **Frontend Developer**: [Sai Jaswanth.K]
- **AI/ML Engineer**: [Sai Jaswanth.K]
- **UI/UX Designer**: [Sai Jaswanth.K]

## 📧 Contact

For inquiries, please contact [saijaswanthkommineni@gmail.com]

---

<div align="center">
  Made with ❤️ by the Billboard Compliance Team
</div>
   git clone https://github.com/yourusername/billboard-compliance-backend.git
   cd billboard-compliance-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/billboard_compliance
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

6. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic models
│   ├── crud.py              # Database operations
│   ├── auth.py              # Authentication logic
│   └── utils/               # Utility functions
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── uploads/                 # Uploaded files
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with FastAPI
- Uses PostgreSQL for data storage
- OpenCV for image processing
- JWT for authentication
