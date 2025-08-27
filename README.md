# 🎯 AI Interview Prepper

A streamlined, API-focused interview preparation platform built with Flask. Features a clean, modular backend architecture with a simple web interface for AI-powered interview analysis.

## ✨ Simplified Architecture

### Backend (Flask + Python)
- **🏭 Application Factory Pattern**: Scalable Flask architecture
- **📦 Blueprint Organization**: Modular route organization
- **⚙️ Centralized Configuration**: Environment-based configuration management
- **🛠️ Dependency Injection**: Service-based architecture for easy testing
- **🔌 RESTful API Design**: Clean, documented API endpoints
- **🔒 Security**: Input validation, file upload security, and error handling

### Frontend (Minimal Web Interface)
- **🎨 Simple UI**: Single-page interface using CDN resources
- **📱 Responsive Design**: Bootstrap-based responsive layout
- **⚡ API Integration**: Direct API calls for all functionality
- **🎯 Focused UX**: Clean, functional interface without complexity

## 🚀 Features

### Core Functionality
- **📄 CV/Job Description Analysis**: AI-powered matching and gap analysis
- **❓ Interview Question Generation**: Personalized questions based on role requirements
- **📚 Study Resources**: Curated learning materials by domain
- **💼 Company Insights**: Interview tips for major companies
- **💰 Salary Guidance**: Negotiation strategies and market insights

### API Endpoints
- `POST /api/analyze` - Analyze CV against job description
- `POST /interview/generate` - Generate interview questions
- `GET /api/study-resources` - Get learning resources
- `GET /api/companies` - Company-specific interview guides
- `GET /api/salary` - Salary negotiation guidance
- `POST /api/chat` - AI chat interface

## 🛠️ Technology Stack

### Backend
- **Flask 2.3.3** - Web framework
- **Python 3.8+** - Programming language
- **OpenAI API** - AI-powered analysis
- **PyPDF2** - PDF processing
- **python-docx** - Word document processing

### Frontend
- **Bootstrap 5.3** - UI framework (CDN)
- **FontAwesome** - Icons (CDN)
- **Vanilla JavaScript** - API interactions

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, for AI features)

## ⚡ Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/Ai-Interview-Prepper.git
   cd Ai-Interview-Prepper
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Interface**
   - Open your browser and navigate to `http://localhost:5000`
   - Use the simple web interface or call API endpoints directly

## 🎯 How to Use

### Web Interface
1. Navigate to `http://localhost:5000`
2. Paste or upload your job description and CV
3. Click "Analyze Fit" to get AI-powered analysis
4. Generate interview questions and access study resources

### API Usage
```bash
# Analyze CV fit
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"job_description": "...", "cv_text": "..."}'

# Generate interview questions
curl -X POST http://localhost:5000/interview/generate \
  -H "Content-Type: application/json" \
  -d '{"job_description": "...", "cv_text": "...", "difficulty": 2}'

# Get study resources
curl http://localhost:5000/api/study-resources?domain=technology

# Get company guides
curl http://localhost:5000/api/companies
```

## 📁 Project Structure

```
Ai-Interview-Prepper/
├── app/                    # Flask application package
│   ├── __init__.py        # Application factory
│   ├── core/              # Core configurations and utilities
│   │   ├── config.py      # Configuration management
│   │   ├── extensions.py  # Flask extensions
│   │   └── utils.py       # Utility functions
│   └── routes/            # Route blueprints
│       ├── main.py        # Main routes and UI
│       └── features.py    # Feature API routes
├── api/                   # API route modules
│   ├── interview_routes.py
│   ├── study_resources_routes.py
│   └── ...
├── services/              # Business logic services
├── utils/                 # Utility modules
│   ├── ai_analyzer.py
│   ├── document_processor.py
│   └── interview_generator.py
├── tests/                 # Test files
├── uploads/               # File uploads directory
├── app.py                # Application entry point
└── requirements.txt      # Python dependencies
```

## ⚙️ Configuration

Set environment variables in `.env` file:

```env
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
FLASK_ENV=development
```

## 🔮 Future Enhancements

- **Database Integration**: Store user sessions and analysis history
- **Authentication System**: User accounts and personalized recommendations
- **Enhanced AI Features**: More sophisticated analysis and recommendations
- **Mobile App**: Native mobile applications
- **Analytics Dashboard**: Detailed performance tracking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing powerful AI capabilities
- Flask community for the excellent web framework
- Bootstrap for the responsive UI components

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

## 🌟 Show Your Support

Give a ⭐️ if this project helped you!