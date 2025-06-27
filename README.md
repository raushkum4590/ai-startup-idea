# 🚀 AI Startup Idea Generator & Market Validator

A powerful Streamlit application that generates innovative startup ideas and validates them using AI-powered market analysis. Built with OpenRouter API and Mistral AI.

## Features

### 💡 Startup Idea Generation
- Generate 3 unique startup ideas based on your criteria
- Customizable inputs: industry, target audience, budget, problem focus
- Detailed idea breakdown including value proposition, revenue model, and competitive advantages

### 🔍 Market Validation
- Comprehensive market analysis for any startup idea
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Market opportunity scoring (1-10)
- Competition level assessment
- Financial projections for 3 years
- Go-to-market strategy recommendations
- Risk assessment and success probability

### 📈 Analytics Dashboard
- Visual representation of validation scores
- SWOT analysis distribution charts
- Competition level gauge
- Interactive charts using Plotly

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (get it from [OpenRouter](https://openrouter.ai/))

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd startup-idea-generator
   ```

2. **Set up your API key**
   ```bash
   # Copy the environment template
   copy .env.example .env
   
   # Edit .env file and add your OpenRouter API key
   # OPENROUTER_API_KEY=your_actual_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Get your OpenRouter API key**
   - Visit [OpenRouter](https://openrouter.ai/)
   - Sign up for an account
   - Get your API key from the dashboard
   - Add it to your .env file

## Usage Guide

### 1. Generate Startup Ideas
1. Ensure your API key is configured in the .env file
2. The sidebar will show "✅ API Key configured and ready!" when properly set up
3. Fill in the idea generation form:
   - **Industry/Sector**: Choose from predefined options
   - **Target Audience**: Describe your ideal customers
   - **Budget Range**: Select your initial investment capacity
   - **Problem Focus**: Describe the main problem to solve
4. Click "Generate Startup Ideas" to get 3 AI-generated ideas

### 2. Validate Ideas
1. Either select an idea from the generation step or manually enter:
   - Startup name
   - Description
   - Target market
2. Click "Validate Idea" to get comprehensive market analysis
3. Review the detailed validation report including:
   - Market opportunity score
   - Competition analysis
   - SWOT breakdown
   - Financial projections
   - Recommendations

### 3. View Analytics
- Navigate to the Analytics tab to see visual representations
- Compare validation scores
- Analyze SWOT distribution
- Monitor competition levels

## API Configuration

### OpenRouter API
- **Model Used**: `mistralai/mistral-small-3.2-24b-instruct:free`
- **Provider**: OpenRouter
- **Cost**: Free tier available
- **Rate Limits**: As per OpenRouter's free tier limits

### API Key Security
- API keys are loaded from the .env file (never displayed in UI)
- .env file is excluded from version control (.gitignore)
- No API key information shown in the interface
- Secure environment variable loading

## Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **OpenRouter API**: AI model access
- **Mistral AI**: Language model for generation and validation
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation
- **Requests**: HTTP client for API calls

### Application Architecture
```
app.py
├── StartupIdeaGenerator (Main class)
│   ├── call_openrouter_api()
│   ├── generate_startup_ideas()
│   └── validate_startup_idea()
├── UI Components
│   ├── Sidebar (API key, settings)
│   ├── Tab 1: Idea Generation
│   ├── Tab 2: Market Validation
│   └── Tab 3: Analytics Dashboard
└── Styling (Custom CSS)
```

## Features in Detail

### Idea Generation
The AI generates startup ideas with:
- **Name**: Creative startup names
- **Description**: Clear 2-3 sentence descriptions
- **Value Proposition**: Unique selling points
- **Market Size**: Target market analysis
- **Revenue Model**: How the startup makes money
- **Key Features**: 3-4 main product features
- **Competitive Advantage**: What sets it apart

### Market Validation
Comprehensive analysis including:
- **Market Opportunity Score**: 1-10 rating
- **Competition Level**: Low/Medium/High assessment
- **Market Trends**: Current industry analysis
- **SWOT Analysis**: Detailed breakdown
- **Go-to-Market Strategy**: Launch recommendations
- **Financial Projections**: 3-year outlook
- **Risk Assessment**: Potential challenges
- **Success Probability**: 1-10 likelihood rating
- **Key Metrics**: Important KPIs to track
- **Recommendations**: Actionable next steps

### Analytics Dashboard
Visual insights featuring:
- **Score Comparison Charts**: Bar charts for key metrics
- **SWOT Distribution**: Pie charts showing analysis breakdown
- **Competition Gauge**: Visual competition level indicator
- **Interactive Elements**: Plotly-powered visualizations

## Customization

### Adding New Industries
Edit the industry selectbox options in `app.py`:
```python
industry = st.selectbox(
    "Industry/Sector",
    ["Technology", "Healthcare", "Your New Industry", ...]
)
```

### Modifying Budget Ranges
Update the budget range options:
```python
budget_range = st.selectbox(
    "Initial Budget Range",
    ["Under $10K", "Your Custom Range", ...]
)
```

### Styling Customization
Modify the CSS in the `st.markdown()` sections to change:
- Colors and gradients
- Card styles
- Layout spacing
- Typography

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify your OpenRouter API key is correct
   - Check if you have credits in your OpenRouter account
   - Ensure the API key has proper permissions

2. **Slow Response Times**
   - Free tier models may have slower response times
   - Consider upgrading to paid OpenRouter plans for faster responses

3. **JSON Parsing Errors**
   - The AI occasionally returns malformed JSON
   - The app includes error handling and retry logic
   - Try regenerating if errors persist

4. **Installation Issues**
   - Ensure Python 3.8+ is installed
   - Use virtual environments to avoid conflicts
   - Update pip: `pip install --upgrade pip`

### Error Messages
- **"Please enter your OpenRouter API key"**: Add API key in sidebar
- **"Failed to parse AI response"**: Retry the operation
- **"API Error"**: Check internet connection and API key validity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support and questions:
1. Check the troubleshooting section
2. Review OpenRouter documentation
3. Create an issue in the repository

## Future Enhancements

- [ ] Save and export ideas/validations
- [ ] User authentication and history
- [ ] Multiple AI model comparisons
- [ ] Industry-specific templates
- [ ] Integration with business plan generators
- [ ] Market research data integration
- [ ] Competitor analysis tools
- [ ] Financial modeling improvements

---

**Made with ❤️ using Streamlit and OpenRouter API | Powered by Mistral AI**
