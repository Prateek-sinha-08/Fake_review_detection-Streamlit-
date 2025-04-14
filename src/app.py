import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from components.ReviewScraper import ReviewScraper
from components.ReviewAnalyzer import ReviewAnalyzer

# Set page configuration
st.set_page_config(
    page_title="Review Authenticity Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .sub-header {
        color: #374151;
        font-size: 1.5rem;
        font-weight: 600;
    }
    .result-box {
        background-color: #f0f9ff;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #bae6fd;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<p class="main-header">Review Authenticity Analyzer</p>', unsafe_allow_html=True)
st.markdown("""
This tool helps you determine if product reviews are genuine or fake using Natural Language Processing.
Simply enter a product URL, and we'll analyze the reviews for authenticity.
""")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    This application uses machine learning to detect fake reviews. 
    It analyzes patterns in language, review timing, and reviewer behavior 
    to estimate the authenticity of product reviews.
    """)
    
    st.header("Supported Websites")
    st.write("""
    Currently supports:
    - Amazon
    - Best Buy
    - Walmart
    
    More websites coming soon!
    """)
    
    st.header("How It Works")
    st.write("""
    1. Enter a product URL
    2. Our scraper collects the reviews
    3. NLP model analyzes each review
    4. Results show authenticity percentage
    """)

# Main content
url = st.text_input("Enter product URL:", placeholder="https://www.amazon.com/product-page")

# Advanced options collapse
with st.expander("Advanced Options"):
    min_reviews = st.slider("Minimum reviews to analyze", 10, 100, 30)
    confidence_threshold = st.slider("Confidence threshold", 0.5, 0.95, 0.7)

if st.button("Analyze Reviews"):
    if url:
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Scrape reviews
        status_text.text("Scraping reviews from the provided URL...")
        progress_bar.progress(10)
        
        try:
            scraper = ReviewScraper()
            reviews = scraper.scrape(url, min_count=min_reviews)
            
            if not reviews:
                st.error("Could not find reviews on the provided page. Please check the URL and try again.")
            else:
                progress_bar.progress(40)
                status_text.text(f"Successfully scraped {len(reviews)} reviews. Analyzing...")
                
                # Step 2: Analyze reviews
                analyzer = ReviewAnalyzer()
                results = analyzer.analyze_reviews(reviews, threshold=confidence_threshold)
                
                progress_bar.progress(90)
                status_text.text("Analysis complete! Generating report...")
                
                # Step 3: Show results
                real_percentage = results["real_percentage"]
                fake_percentage = results["fake_percentage"]
                
                # Clear progress indicators
                progress_bar.progress(100)
                status_text.empty()
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<p class="sub-header">Authenticity Score</p>', unsafe_allow_html=True)
                    
                    # Create authenticity gauge
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.set_xlim(0, 100)
                    ax.set_ylim(0, 10)
                    ax.set_title("Review Authenticity", fontsize=16)
                    ax.set_xticks([0, 25, 50, 75, 100])
                    ax.set_yticks([])
                    
                    # Create gauge sections
                    ax.axvspan(0, 30, facecolor='#ef4444', alpha=0.8)
                    ax.axvspan(30, 70, facecolor='#fbbf24', alpha=0.8)
                    ax.axvspan(70, 100, facecolor='#22c55e', alpha=0.8)
                    
                    # Add gauge arrow
                    ax.arrow(real_percentage, 5, 0, 0, head_width=2, head_length=5, 
                             fc='black', ec='black', width=0.5)
                    
                    # Add labels
                    plt.text(15, 2, "Mostly Fake", ha='center', fontsize=12)
                    plt.text(50, 2, "Mixed", ha='center', fontsize=12)
                    plt.text(85, 2, "Mostly Real", ha='center', fontsize=12)
                    plt.text(real_percentage, 8, f"{real_percentage}%", ha='center', 
                             fontweight='bold', fontsize=14)
                    
                    st.pyplot(fig)
                
                with col2:
                    st.markdown('<p class="sub-header">Analysis Details</p>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="result-box">
                        <h3>Summary</h3>
                        <p><strong>{real_percentage}%</strong> of reviews appear to be genuine</p>
                        <p><strong>{fake_percentage}%</strong> of reviews appear to be fake</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    recommendation = ""
                    if real_percentage >= 70:
                        recommendation = "✅ Reviews for this product are likely trustworthy."
                    elif real_percentage >= 30:
                        recommendation = "⚠️ Mixed reviews - proceed with caution and check the negative reviews."
                    else:
                        recommendation = "❌ Reviews appear suspicious. Be cautious when considering this product."
                    
                    st.markdown(f"""
                    <div class="result-box" style="margin-top: 1rem;">
                        <h3>Recommendation</h3>
                        <p>{recommendation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show detailed review breakdown
                st.markdown('<p class="sub-header">Review Breakdown</p>', unsafe_allow_html=True)
                
                # Sample data for demonstration
                df = pd.DataFrame({
                    'Review': [r["text"][:100] + "..." for r in results["reviews"][:10]],
                    'Rating': [r["rating"] for r in results["reviews"][:10]],
                    'Authenticity': [f"{r['authenticity_score']:.0%}" for r in results["reviews"][:10]],
                    'Likely Fake': [r["is_fake"] for r in results["reviews"][:10]]
                })
                
                # Style the dataframe
                def color_fake(val):
                    color = '#fecaca' if val else '#dcfce7'
                    return f'background-color: {color}'
                
                styled_df = df.style.applymap(color_fake, subset=['Likely Fake'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Download detailed results
                csv = results["export_csv"]
                st.download_button(
                    label="Download Detailed Results",
                    data=csv,
                    file_name="review_analysis.csv",
                    mime="text/csv",
                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
    else:
        st.warning("Please enter a valid product URL to analyze.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.8rem;">
    <p>Review Authenticity Analyzer | Built with Streamlit and Python</p>
    <p>This tool is for educational purposes only. Results should not be considered definitive.</p>
</div>
""", unsafe_allow_html=True)