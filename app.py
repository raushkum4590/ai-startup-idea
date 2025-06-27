import streamlit as st
import requests
import json
import time
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
import pathlib
current_dir = pathlib.Path(__file__).parent.absolute()
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Alternative method to load API key if dotenv fails
def load_api_key_fallback():
    """Fallback method to load API key directly from .env file"""
    try:
        env_file = current_dir / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('OPENROUTER_API_KEY='):
                        return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading .env file: {e}")
    return None

# Page configuration
st.set_page_config(
    page_title="AI Startup Idea Generator & Market Validator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .idea-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .validation-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StartupIdeaGenerator:
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-small-3.2-24b-instruct:free"
        
        # Load API key from multiple sources (priority order):
        # 1. Streamlit secrets (for cloud deployment)
        # 2. Environment variable
        # 3. .env file fallback
        self.api_key = None
        
        # Try Streamlit secrets first (for cloud deployment)
        try:
            if hasattr(st, 'secrets') and 'OPENROUTER_API_KEY' in st.secrets:
                self.api_key = st.secrets['OPENROUTER_API_KEY']
        except Exception:
            pass
        
        # Fallback to environment variable or .env file
        if not self.api_key:
            self.api_key = os.getenv('OPENROUTER_API_KEY') or load_api_key_fallback()
        
        # Debug: Check if API key is loaded (for development only)
        if self.api_key:
            print(f"✅ API Key loaded: {self.api_key[:8]}...")
        else:
            print("❌ API Key not found in any source")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Environment file exists: {os.path.exists('.env')}")
            print(f"Environment file exists (absolute): {os.path.exists(current_dir / '.env')}")
        
    def call_openrouter_api(self, messages, max_tokens=2000):
        """Call OpenRouter API with the specified model"""
        # Only use environment variable API key
        api_key = self.api_key
        
        if not api_key:
            st.error("⚠️ OpenRouter API key not found!")
            st.info("""
            **Setup Instructions:**
            
            **Local Development:** Create a .env file with: `OPENROUTER_API_KEY=your_key_here`
            
            **Streamlit Cloud:** Add `OPENROUTER_API_KEY = "your_key_here"` to your app secrets
            """)
            return None
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            with st.spinner("Generating response..."):
                response = requests.post(self.api_url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def generate_startup_ideas(self, industry, target_audience, budget_range, problem_focus):
        """Generate startup ideas based on user inputs"""
        prompt = f"""
        Generate 3 innovative startup ideas based on the following criteria:
        
        Industry: {industry}
        Target Audience: {target_audience}
        Budget Range: {budget_range}
        Problem Focus: {problem_focus}
        
        For each idea, provide:
        1. Startup Name
        2. Brief Description (2-3 sentences)
        3. Unique Value Proposition
        4. Target Market Size
        5. Revenue Model
        6. Key Features (3-4 bullet points)
        7. Competitive Advantage
        
        Format the response as JSON with the following structure:
        {{
            "ideas": [
                {{
                    "name": "Startup Name",
                    "description": "Brief description",
                    "value_proposition": "Unique value proposition",
                    "market_size": "Target market size",
                    "revenue_model": "Revenue model",
                    "key_features": ["Feature 1", "Feature 2", "Feature 3"],
                    "competitive_advantage": "Competitive advantage"
                }}
            ]
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self.call_openrouter_api(messages)
        
        if response:
            try:
                # Clean the response if it contains markdown formatting
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                # Additional cleaning for common AI response issues
                if cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response[3:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                # Try to find JSON content if wrapped in text
                if "{" in cleaned_response and "}" in cleaned_response:
                    start_idx = cleaned_response.find("{")
                    end_idx = cleaned_response.rfind("}") + 1
                    cleaned_response = cleaned_response[start_idx:end_idx]
                
                return json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse AI response: {str(e)}")
                st.error("Raw response for debugging:")
                st.code(response[:500] + "..." if len(response) > 500 else response)
                st.info("Please try again. The AI sometimes returns malformed JSON.")
                return None
            except Exception as e:
                st.error(f"Unexpected error parsing response: {str(e)}")
                return None
        return None
    
    def validate_startup_idea(self, idea_name, description, target_market):
        """Validate a startup idea and provide market analysis"""
        prompt = f"""
        Perform a comprehensive market validation analysis for this startup idea:
        
        Startup Name: {idea_name}
        Description: {description}
        Target Market: {target_market}
        
        Provide a detailed analysis including:
        1. Market Opportunity Score (1-10)
        2. Competition Level (Low/Medium/High)
        3. Market Trends Analysis
        4. SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
        5. Go-to-Market Strategy
        6. Financial Projections (Year 1-3)
        7. Risk Assessment
        8. Success Probability (1-10)
        9. Key Metrics to Track
        10. Recommendations
        
        Format the response as JSON with the following structure:
        {{
            "market_opportunity_score": 8,
            "competition_level": "Medium",
            "market_trends": "Analysis of current market trends",
            "swot": {{
                "strengths": ["Strength 1", "Strength 2"],
                "weaknesses": ["Weakness 1", "Weakness 2"],
                "opportunities": ["Opportunity 1", "Opportunity 2"],
                "threats": ["Threat 1", "Threat 2"]
            }},
            "go_to_market": "Go-to-market strategy",
            "financial_projections": {{
                "year_1": "Year 1 projection",
                "year_2": "Year 2 projection",
                "year_3": "Year 3 projection"
            }},
            "risk_assessment": "Risk assessment details",
            "success_probability": 7,
            "key_metrics": ["Metric 1", "Metric 2", "Metric 3"],
            "recommendations": ["Recommendation 1", "Recommendation 2"]
        }}
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = self.call_openrouter_api(messages, max_tokens=3000)
        
        if response:
            try:
                # Clean the response if it contains markdown formatting
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                # Additional cleaning for common AI response issues
                if cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response[3:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                cleaned_response = cleaned_response.strip()
                
                # Try to find JSON content if wrapped in text
                if "{" in cleaned_response and "}" in cleaned_response:
                    start_idx = cleaned_response.find("{")
                    end_idx = cleaned_response.rfind("}") + 1
                    cleaned_response = cleaned_response[start_idx:end_idx]
                
                return json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                st.error(f"Failed to parse validation response: {str(e)}")
                st.error("Raw response for debugging:")
                st.code(response[:500] + "..." if len(response) > 500 else response)
                st.info("Please try again. The AI sometimes returns malformed JSON.")
                return None
            except Exception as e:
                st.error(f"Unexpected error parsing validation response: {str(e)}")
                return None
        return None

def main():
    # Initialize the generator
    generator = StartupIdeaGenerator()
    
    # Header
    st.markdown('<div class="main-header">🚀 AI Startup Idea Generator & Market Validator</div>', unsafe_allow_html=True)
    st.markdown("Generate innovative startup ideas and validate them with AI-powered market analysis")
    
    # Sidebar for API key and settings
    with st.sidebar:
        st.header("🔑 Configuration")
        
        # Check if API key is loaded from environment (don't display the key)
        env_api_key = generator.api_key  # Use the generator's loaded key
        if env_api_key:
            st.success("✅ API Key configured and ready!")
        else:
            st.error("❌ API key not found")
            st.markdown("""
            **Setup Required:**
            
            **For Local Development:**
            1. Create a `.env` file in the project folder
            2. Add: `OPENROUTER_API_KEY=your_key_here`
            3. Restart the application
            
            **For Streamlit Cloud:**
            1. Go to your app settings
            2. Add to Secrets: `OPENROUTER_API_KEY = "your_key_here"`
            3. Redeploy the application
            """)
            
            # Debug information
            with st.expander("🔧 Debug Info"):
                st.write(f"Current directory: {os.getcwd()}")
                st.write(f".env file exists: {os.path.exists('.env')}")
                env_path = pathlib.Path(__file__).parent.absolute() / '.env'
                st.write(f".env absolute path exists: {env_path.exists()}")
                
                # Check Streamlit secrets
                try:
                    if hasattr(st, 'secrets'):
                        st.write("✅ Streamlit secrets available")
                        if 'OPENROUTER_API_KEY' in st.secrets:
                            st.write("✅ API key found in Streamlit secrets")
                        else:
                            st.write("❌ API key not found in Streamlit secrets")
                    else:
                        st.write("❌ Streamlit secrets not available")
                except Exception as e:
                    st.write(f"❌ Error checking Streamlit secrets: {e}")
                
                if env_path.exists():
                    st.write("✅ .env file found")
                    try:
                        with open(env_path, 'r') as f:
                            content = f.read()
                            if 'OPENROUTER_API_KEY=' in content:
                                st.write("✅ API key variable found in .env")
                            else:
                                st.write("❌ API key variable not found in .env")
                    except Exception as e:
                        st.write(f"❌ Error reading .env: {e}")
        
        st.markdown("---")
        st.header("💡 Quick Tips")
        st.markdown("""
        - Be specific about your target audience
        - Consider current market trends
        - Think about scalability
        - Focus on real problems
        - Validate ideas before investing
        """)
        
        st.markdown("---")
        st.header("� Features")
        st.markdown("""
        ✨ **Idea Generation**
        - AI-powered startup concepts
        - Industry-specific suggestions
        - Budget-aware recommendations
        
        🔍 **Market Validation**
        - SWOT analysis
        - Competition assessment
        - Financial projections
        - Success probability
        
        📊 **Analytics**
        - Visual insights
        - Market scoring
        - Risk assessment
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["💡 Generate Ideas", "🔍 Validate Ideas", "📈 Analytics"])
    
    with tab1:
        st.markdown('<div class="section-header">Generate Startup Ideas</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Industry/Sector",
                ["Technology", "Healthcare", "Education", "Finance", "E-commerce", 
                 "Entertainment", "Food & Beverage", "Transportation", "Real Estate", 
                 "Environment", "Fashion", "Sports", "Travel", "Other"]
            )
            
            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Small business owners, Students, Remote workers"
            )
        
        with col2:
            budget_range = st.selectbox(
                "Initial Budget Range",
                ["Under $10K", "$10K - $50K", "$50K - $100K", "$100K - $500K", "$500K+"]
            )
            
            problem_focus = st.text_area(
                "Problem/Pain Point to Address",
                placeholder="Describe the main problem your startup should solve"
            )
        
        if st.button("🚀 Generate Startup Ideas", type="primary"):
            if not all([industry, target_audience, budget_range, problem_focus]):
                st.warning("Please fill in all fields to generate ideas.")
            else:
                ideas_data = generator.generate_startup_ideas(industry, target_audience, budget_range, problem_focus)
                
                if ideas_data and 'ideas' in ideas_data:
                    st.session_state['generated_ideas'] = ideas_data['ideas']
                    
                    for i, idea in enumerate(ideas_data['ideas']):
                        with st.container():
                            st.markdown(f"""
                            <div class="idea-card">
                                <h3>💡 {idea['name']}</h3>
                                <p><strong>Description:</strong> {idea['description']}</p>
                                <p><strong>Value Proposition:</strong> {idea['value_proposition']}</p>
                                <p><strong>Market Size:</strong> {idea['market_size']}</p>
                                <p><strong>Revenue Model:</strong> {idea['revenue_model']}</p>
                                <p><strong>Competitive Advantage:</strong> {idea['competitive_advantage']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Key Features
                            st.markdown("**Key Features:**")
                            for feature in idea['key_features']:
                                st.markdown(f"• {feature}")
                            
                            if st.button(f"🔍 Validate This Idea", key=f"validate_{i}"):
                                st.session_state['idea_to_validate'] = idea
                                st.session_state['active_tab'] = 1
                                st.rerun()
                            
                            st.markdown("---")
    
    with tab2:
        st.markdown('<div class="section-header">Market Validation</div>', unsafe_allow_html=True)
        
        # Check if an idea was selected for validation
        if 'idea_to_validate' in st.session_state:
            idea = st.session_state['idea_to_validate']
            st.info(f"Validating: **{idea['name']}**")
            
            # Auto-populate fields
            idea_name = st.text_input("Startup Name", value=idea['name'])
            description = st.text_area("Description", value=idea['description'])
            target_market = st.text_input("Target Market", value=idea.get('market_size', ''))
        else:
            # Manual input
            idea_name = st.text_input("Startup Name", placeholder="Enter your startup idea name")
            description = st.text_area("Description", placeholder="Describe your startup idea")
            target_market = st.text_input("Target Market", placeholder="Describe your target market")
        
        if st.button("🔍 Validate Idea", type="primary"):
            if not all([idea_name, description, target_market]):
                st.warning("Please fill in all fields for validation.")
            else:
                validation_data = generator.validate_startup_idea(idea_name, description, target_market)
                
                if validation_data:
                    st.session_state['validation_results'] = validation_data
                    
                    # Display validation results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Market Opportunity", f"{validation_data['market_opportunity_score']}/10")
                    with col2:
                        st.metric("Competition Level", validation_data['competition_level'])
                    with col3:
                        st.metric("Success Probability", f"{validation_data['success_probability']}/10")
                    
                    st.markdown(f"""
                    <div class="validation-card">
                        <h3>📊 Market Analysis for {idea_name}</h3>
                        <p><strong>Market Trends:</strong> {validation_data['market_trends']}</p>
                        <p><strong>Go-to-Market Strategy:</strong> {validation_data['go_to_market']}</p>
                        <p><strong>Risk Assessment:</strong> {validation_data['risk_assessment']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # SWOT Analysis
                    st.markdown("### SWOT Analysis")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Strengths**")
                        for strength in validation_data['swot']['strengths']:
                            st.markdown(f"✅ {strength}")
                        
                        st.markdown("**Opportunities**")
                        for opportunity in validation_data['swot']['opportunities']:
                            st.markdown(f"🚀 {opportunity}")
                    
                    with col2:
                        st.markdown("**Weaknesses**")
                        for weakness in validation_data['swot']['weaknesses']:
                            st.markdown(f"⚠️ {weakness}")
                        
                        st.markdown("**Threats**")
                        for threat in validation_data['swot']['threats']:
                            st.markdown(f"🚨 {threat}")
                    
                    # Financial Projections
                    st.markdown("### Financial Projections")
                    proj_col1, proj_col2, proj_col3 = st.columns(3)
                    
                    with proj_col1:
                        st.markdown(f"**Year 1:** {validation_data['financial_projections']['year_1']}")
                    with proj_col2:
                        st.markdown(f"**Year 2:** {validation_data['financial_projections']['year_2']}")
                    with proj_col3:
                        st.markdown(f"**Year 3:** {validation_data['financial_projections']['year_3']}")
                    
                    # Key Metrics and Recommendations
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### Key Metrics to Track")
                        for metric in validation_data['key_metrics']:
                            st.markdown(f"📊 {metric}")
                    
                    with col2:
                        st.markdown("### Recommendations")
                        for rec in validation_data['recommendations']:
                            st.markdown(f"💡 {rec}")
    
    with tab3:
        st.markdown('<div class="section-header">Analytics Dashboard</div>', unsafe_allow_html=True)
        
        # Display analytics if validation results exist
        if 'validation_results' in st.session_state:
            validation = st.session_state['validation_results']
            
            # Create visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Score comparison chart
                scores_df = pd.DataFrame({
                    'Metric': ['Market Opportunity', 'Success Probability'],
                    'Score': [validation['market_opportunity_score'], validation['success_probability']],
                    'Max Score': [10, 10]
                })
                
                fig = px.bar(scores_df, x='Metric', y='Score', 
                           title='Validation Scores',
                           color='Score',
                           color_continuous_scale='RdYlGn')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # SWOT Analysis visualization
                swot_data = validation['swot']
                categories = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
                counts = [len(swot_data['strengths']), len(swot_data['weaknesses']), 
                         len(swot_data['opportunities']), len(swot_data['threats'])]
                
                fig = px.pie(values=counts, names=categories, title='SWOT Analysis Distribution')
                st.plotly_chart(fig, use_container_width=True)
            
            # Competition level indicator
            competition_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
            competition_color = competition_colors.get(validation['competition_level'], 'blue')
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = {'Low': 3, 'Medium': 6, 'High': 9}[validation['competition_level']],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Competition Level"},
                gauge = {
                    'axis': {'range': [None, 10]},
                    'bar': {'color': competition_color},
                    'steps': [
                        {'range': [0, 3], 'color': "lightgreen"},
                        {'range': [3, 7], 'color': "yellow"},
                        {'range': [7, 10], 'color': "lightcoral"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 8
                    }
                }
            ))
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Generate and validate a startup idea to see analytics!")
    
    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and OpenRouter API | Powered by Mistral AI")

if __name__ == "__main__":
    main()
