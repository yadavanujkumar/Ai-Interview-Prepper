# 🎯 AI Interview Prepper

An intelligent interview preparation tool that helps candidates prepare for interviews across any field or profession by analyzing job descriptions and CVs to provide personalized, domain-relevant guidance.

## 🚀 Features

### Core Functionality
- **📄 Document Analysis**: Upload or paste job descriptions and CVs in multiple formats (PDF, DOCX, TXT)
- **🤖 AI-Powered Matching**: Intelligent analysis of candidate-job fit across multiple dimensions
- **📊 Scoring System**: Comprehensive scoring with skills, experience, and education match percentages
- **🎓 Personalized Recommendations**: Tailored study plans and skill development suggestions
- **❓ Mock Interview Generator**: Domain-specific interview questions (technical, behavioral, situational)
- **📝 Resume Optimization**: Suggestions for improving CV alignment with job requirements

### Enhanced Features (NEW!)
- **💬 Real-time AI Chat**: Practice interviews with AI interviewer in real-time conversation
- **🔗 Job Board Integration**: Import job descriptions directly from LinkedIn, Indeed, and other major job boards
- **📈 Progress Analytics**: Track your improvement with detailed analytics and performance insights
- **🌍 Multi-language Support**: Practice interviews in multiple languages (English, Spanish, French, German, etc.)
- **🏢 Company-specific Guides**: Get tailored preparation for specific companies (Google, Amazon, Microsoft, etc.)
- **💰 Salary Negotiation Guidance**: Comprehensive salary negotiation strategies and market data

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

- Python 3.8 or higher
- pip package manager
- (Optional) OpenAI API key for enhanced AI features

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yadavanujkumar/Ai-Interview-Prepper.git
   cd Ai-Interview-Prepper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
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