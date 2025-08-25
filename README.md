# Billboard Compliance Management System

A comprehensive platform for managing and monitoring billboard compliance with local regulations and ordinances.

## 📋 Features

### Core Functionality
- 📋 Billboard registration and management
- 🔍 Compliance inspection tracking
- ⚠️ Violation reporting and resolution
- 📁 Document and media management
- 📊 Reporting and analytics

### User Management
- 🔐 JWT authentication
- 👥 Role-based access control
- 👤 User activity logs
- 🔄 Profile management

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: MySQL/MariaDB
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Validation**: Pydantic

### Frontend (Separate Repository)
- **Framework**: React.js
- **State Management**: Context API
- **UI Components**: Material-UI
- **Maps**: Mapbox GL

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- MySQL/MariaDB
- pip (Python package manager)
- Node.js 16+ (for frontend)

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

For inquiries, please contact [saijaswanthkommineni@gmail.com](saijaswanthkommineni@gmail.com)

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
