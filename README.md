# 🎯 AI Interview Prepper

A modern, intelligent interview preparation platform built with cutting-edge web technologies. Features modular frontend and backend architecture similar to high-tech companies, providing personalized interview preparation across any field or profession.

![AI Interview Prepper](https://github.com/user-attachments/assets/9c1388ce-2ec3-42f8-88d6-c0c003a834bb)

## ✨ Modern Architecture

### Frontend (Modern JavaScript)
- **⚡ Vite Build System**: Lightning-fast development with hot module replacement
- **🧩 Component-Based Architecture**: Modular, reusable UI components
- **📱 Responsive Design**: Mobile-first design with modern CSS Grid/Flexbox
- **🎨 Design System**: Consistent theming with CSS custom properties
- **🔄 State Management**: Centralized application state with event bus pattern
- **📡 API Client**: Modern fetch-based HTTP client with error handling

### Backend (Flask + Python)
- **🏭 Application Factory Pattern**: Scalable Flask architecture
- **📦 Blueprint Organization**: Modular route organization
- **⚙️ Centralized Configuration**: Environment-based configuration management
- **🛠️ Dependency Injection**: Service-based architecture for easy testing
- **🔌 RESTful API Design**: Clean, documented API endpoints
- **🔒 Security**: Input validation, file upload security, and error handling

## 🚀 Features

### Core Functionality
- **📄 Smart Document Processing**: Upload or paste job descriptions and CVs (PDF, DOCX, TXT)
- **🤖 AI-Powered Analysis**: Intelligent candidate-job fit analysis
- **📊 Comprehensive Scoring**: Skills, experience, and education match percentages
- **🎓 Personalized Recommendations**: Tailored study plans and skill development
- **❓ Dynamic Mock Interviews**: Domain-specific interview questions
- **📝 Resume Optimization**: CV improvement suggestions

### Enhanced Features
- **💬 Real-time AI Chat**: Practice interviews with conversational AI
- **🔗 Job Board Integration**: Import jobs from LinkedIn, Indeed, Glassdoor
- **📈 Progress Analytics**: Detailed performance tracking and insights
- **🌍 Multi-language Support**: Practice in multiple languages
- **🏢 Company-specific Guides**: Tailored preparation for top companies
- **💰 Salary Negotiation**: Comprehensive negotiation strategies

### Supported Domains
- Software Engineering & Development
- Data Science & Analytics  
- Healthcare & Medical
- Education & Training
- Design & Creative
- Marketing & Sales
- General Professional Roles

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Document Processing**: PyPDF2, python-docx
- **AI Integration**: OpenAI API (optional)
- **Styling**: Custom CSS with animations and responsive design

## 📋 Prerequisites

- **Python 3.8+**: For backend services
- **Node.js 16+**: For frontend build tools
- **pip**: Python package manager
- **(Optional)** OpenAI API key for enhanced AI features

## ⚡ Quick Start

### Development Mode (Recommended)

```bash
# Clone the repository
git clone https://github.com/yadavanujkumar/Ai-Interview-Prepper.git
cd Ai-Interview-Prepper

# Run the development script (starts both backend and frontend)
./dev.sh
```

This will start:
- 🐍 **Backend**: http://localhost:5000 (Flask API)
- ⚡ **Frontend**: http://localhost:3000 (Vite dev server with hot reload)

### Manual Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Set Up Environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Start Backend**
   ```bash
   python app.py
   ```

5. **Start Frontend Development Server** (in another terminal)
   ```bash
   npm run dev
   ```

### Production Build

```bash
# Build frontend assets
npm run build

# Run production server
python app.py
```
   - Open your browser and navigate to `http://localhost:5000`

## 🎯 How to Use

### 1. Upload Documents
- **Job Description**: Upload a file or paste the text of the job posting
- **CV/Resume**: Upload your resume or paste your CV content
- Supported formats: PDF, DOCX, TXT

### 2. Get Analysis
- Receive a comprehensive fit score (0-100%)
- View breakdown by skills, experience, and education
- See identified gaps and strengths

### 3. Review Recommendations
- **Skills to Develop**: Missing technical and soft skills
- **Study Plan**: Personalized learning suggestions
- **Resume Improvements**: Tips for better CV alignment

### 4. Practice Interviews
- Choose difficulty level (Easy, Medium, Hard)
- Get domain-specific questions:
  - **Technical**: Role-specific technical questions
  - **Behavioral**: STAR method scenarios
  - **Situational**: Problem-solving scenarios

## 📁 Project Structure

```
Ai-Interview-Prepper/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── document_processor.py  # Document text extraction
│   ├── ai_analyzer.py         # Job-CV analysis engine
│   └── interview_generator.py # Mock interview questions
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── results.html    # Analysis results
│   └── interview.html  # Mock interview
├── static/             # Static assets
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── app.js      # JavaScript functionality
└── uploads/            # File upload directory (auto-created)
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# Flask configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# OpenAI API (optional - app works without it)
OPENAI_API_KEY=your-openai-api-key-here
```

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, TXT
- Files are processed temporarily and not stored permanently

## 🎨 Features in Detail

### Intelligent Analysis Engine
- **Domain Detection**: Automatically identifies job domain/industry
- **Skill Extraction**: Finds relevant technical and soft skills
- **Experience Calculation**: Estimates years of experience from CV
- **Education Assessment**: Evaluates educational qualifications
- **Fit Scoring**: Multi-dimensional scoring algorithm

### Mock Interview Questions
- **Dynamic Generation**: Questions tailored to specific job and candidate
- **Multiple Difficulty Levels**: Easy, Medium, Hard
- **Answer Frameworks**: STAR method for behavioral, structured approach for technical
- **Print-Friendly**: Clean formatting for offline practice

### Responsive Design
- **Mobile-Friendly**: Works on all device sizes
- **Dark Mode Ready**: Prepared for future dark mode implementation
- **Accessibility**: Screen reader friendly with proper ARIA labels
- **Print Optimization**: Clean printing for results and questions

## 🔮 Future Enhancements

- [x] Real-time AI chat for interview practice
- [x] Integration with job boards (LinkedIn, Indeed)
- [x] Progress tracking and analytics
- [x] Multi-language support
- [x] Company-specific preparation guides
- [x] Salary negotiation guidance
- [ ] Video interview simulation
- [ ] Interview scheduling integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bootstrap for the responsive UI framework
- Flask for the lightweight web framework
- OpenAI for AI capabilities (optional integration)
- Font Awesome for icons
- All contributors and users providing feedback

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yadavanujkumar/Ai-Interview-Prepper/issues) page
2. Create a new issue with detailed description
3. Provide sample inputs and expected outputs when reporting bugs

## 🌟 Show Your Support

If this project helped you prepare for your interview, please give it a ⭐ on GitHub!

---

**Built with ❤️ to help you ace your interviews!**