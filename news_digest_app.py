
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any
import time

# Configure page
st.set_page_config(
    page_title="Personalized News Digest",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a87 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .news-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #1f4e79;
    }
    .news-meta {
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .news-title {
        color: #1f4e79;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .news-summary {
        color: #333;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class NewsDigestApp:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        """Initialize session state variables"""
        if 'saved_articles' not in st.session_state:
            st.session_state.saved_articles = []
        if 'user_ratings' not in st.session_state:
            st.session_state.user_ratings = {}
        if 'selected_categories' not in st.session_state:
            st.session_state.selected_categories = ['Technology']
        if 'frequency' not in st.session_state:
            st.session_state.frequency = 'Daily'
        if 'current_view' not in st.session_state:
            st.session_state.current_view = 'All News'

    def get_mock_news_data(self) -> List[Dict[str, Any]]:
        """Return mock news data for demonstration"""
        return [
            {
                "id": "1",
                "title": "Revolutionary AI Breakthrough in Natural Language Processing",
                "summary": "Researchers have developed a new AI model that can understand context and nuance in human language with unprecedented accuracy. This breakthrough could transform how we interact with technology in our daily lives.",
                "source": "TechCrunch",
                "publishedAt": "2025-01-15T10:30:00Z",
                "urlToImage": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400",
                "category": "Technology",
                "url": "https://techcrunch.com/ai-breakthrough"
            },
            {
                "id": "2", 
                "title": "Global Markets Rise as Tech Stocks Surge",
                "summary": "Major stock markets worldwide experienced significant gains today, driven primarily by strong performance in technology sectors. Analysts attribute the surge to positive earnings reports and investor optimism.",
                "source": "Financial Times",
                "publishedAt": "2025-01-15T09:15:00Z",
                "urlToImage": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400",
                "category": "Business",
                "url": "https://ft.com/tech-stocks-surge"
            },
            {
                "id": "3",
                "title": "Championship Finals Set for Epic Showdown",
                "summary": "Two powerhouse teams will clash in what promises to be the most exciting championship final in recent history. Both teams have shown exceptional form throughout the season.",
                "source": "ESPN",
                "publishedAt": "2025-01-15T08:45:00Z",
                "urlToImage": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400",
                "category": "Sports",
                "url": "https://espn.com/championship-finals"
            },
            {
                "id": "4",
                "title": "New Study Reveals Benefits of Mediterranean Diet",
                "summary": "A comprehensive 10-year study shows that following a Mediterranean diet can significantly reduce the risk of cardiovascular disease and improve overall longevity.",
                "source": "Health Journal",
                "publishedAt": "2025-01-15T07:30:00Z",
                "urlToImage": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400",
                "category": "Health",
                "url": "https://healthjournal.com/mediterranean-diet"
            },
            {
                "id": "5",
                "title": "Scientists Discover New Exoplanet in Habitable Zone",
                "summary": "Astronomers have identified a new Earth-like planet orbiting within the habitable zone of a nearby star system. The discovery brings us one step closer to finding potentially life-supporting worlds.",
                "source": "National Geographic",
                "publishedAt": "2025-01-15T05:10:00Z",
                "urlToImage": "https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=400",
                "category": "Science",
                "url": "https://natgeo.com/exoplanet-discovery"
            }
        ]

    def get_news_api_data(self, categories: List[str], api_key: str) -> List[Dict[str, Any]]:
        """Fetch real news data from NewsAPI"""
        if not api_key:
            return self.get_mock_news_data()

        articles = []
        for category in categories:
            try:
                url = f"https://newsapi.org/v2/top-headlines"
                params = {
                    'category': category.lower(),
                    'country': 'us',
                    'apiKey': api_key,
                    'pageSize': 10
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get('articles', []):
                        articles.append({
                            'id': f"{category}_{len(articles)}",
                            'title': article.get('title', ''),
                            'summary': article.get('description', ''),
                            'source': article.get('source', {}).get('name', ''),
                            'publishedAt': article.get('publishedAt', ''),
                            'urlToImage': article.get('urlToImage', ''),
                            'category': category,
                            'url': article.get('url', '')
                        })
            except Exception as e:
                st.error(f"Error fetching news for {category}: {str(e)}")

        return articles if articles else self.get_mock_news_data()

    def summarize_with_gemini(self, text: str, gemini_api_key: str) -> str:
        """Summarize text using Gemini API"""
        if not gemini_api_key or not text:
            return text[:200] + "..." if len(text) > 200 else text

        try:
            # Placeholder for Gemini API integration
            # In a real implementation, you would make the API call here
            return text[:200] + "..." if len(text) > 200 else text

        except Exception as e:
            st.error(f"Error with Gemini API: {str(e)}")
            return text[:200] + "..." if len(text) > 200 else text

    def render_sidebar(self):
        """Render the sidebar with user preferences"""
        st.sidebar.header("🎯 Personalize Your Feed")

        # API Keys Section
        st.sidebar.subheader("🔑 API Configuration")
        news_api_key = st.sidebar.text_input("NewsAPI Key", type="password", help="Get your free API key from newsapi.org")
        gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Get your API key from Google AI Studio")

        # Categories Selection
        st.sidebar.subheader("📂 Select Categories")
        categories = ['Technology', 'Business', 'Sports', 'Health', 'Entertainment', 'Science']
        selected_categories = st.sidebar.multiselect(
            "Choose your interests:",
            categories,
            default=st.session_state.selected_categories
        )
        st.session_state.selected_categories = selected_categories if selected_categories else ['Technology']

        # Frequency Selection
        st.sidebar.subheader("⏰ Update Frequency")
        frequency = st.sidebar.radio(
            "How often do you want updates?",
            ['Daily', 'Weekly'],
            index=0 if st.session_state.frequency == 'Daily' else 1
        )
        st.session_state.frequency = frequency

        # View Selection
        st.sidebar.subheader("👁️ View Mode")
        current_view = st.sidebar.selectbox(
            "Select view:",
            ['All News', 'Saved Articles'],
            index=0 if st.session_state.current_view == 'All News' else 1
        )
        st.session_state.current_view = current_view

        # Stats
        st.sidebar.subheader("📊 Your Stats")
        st.sidebar.metric("Saved Articles", len(st.session_state.saved_articles))
        st.sidebar.metric("Categories", len(st.session_state.selected_categories))

        return news_api_key, gemini_api_key

    def render_article_card(self, article: Dict[str, Any], gemini_api_key: str = None):
        """Render an individual article card"""
        with st.container():
            st.markdown('<div class="news-card">', unsafe_allow_html=True)

            # Article metadata
            try:
                published_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                formatted_date = published_date.strftime("%B %d, %Y at %I:%M %p")
            except:
                formatted_date = "Recent"

            st.markdown(f"""
                <div class="news-meta">
                    📅 {formatted_date} | 📰 {article['source']} | 🏷️ {article['category']}
                </div>
            """, unsafe_allow_html=True)

            # Article title
            st.markdown(f'<div class="news-title">{article["title"]}</div>', unsafe_allow_html=True)

            # Article image and summary in columns
            col1, col2 = st.columns([1, 2])

            with col1:
                if article.get('urlToImage'):
                    st.image(article['urlToImage'], use_container_width=True)

            with col2:
                summary = self.summarize_with_gemini(article['summary'], gemini_api_key)
                st.markdown(f'<div class="news-summary">{summary}</div>', unsafe_allow_html=True)

            # Action buttons
            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])

            with col1:
                # Rating system
                article_id = article['id']
                current_rating = st.session_state.user_ratings.get(article_id, 0)
                rating = st.select_slider(
                    f"Rate this article",
                    options=[0, 1, 2, 3, 4, 5],
                    value=current_rating,
                    format_func=lambda x: "⭐" * x if x > 0 else "No rating",
                    key=f"rating_{article_id}"
                )
                if rating != current_rating:
                    st.session_state.user_ratings[article_id] = rating
                    st.success(f"Rated {rating} stars!")

            with col2:
                # Save/Unsave button
                is_saved = article_id in [a['id'] for a in st.session_state.saved_articles]
                save_button_text = "💾 Saved" if is_saved else "💾 Save"
                if st.button(save_button_text, key=f"save_{article_id}"):
                    if is_saved:
                        st.session_state.saved_articles = [a for a in st.session_state.saved_articles if a['id'] != article_id]
                        st.success("Article removed!")
                    else:
                        st.session_state.saved_articles.append(article)
                        st.success("Article saved!")
                    st.rerun()

            with col3:
                # Share button
                if st.button("🔗 Share", key=f"share_{article_id}"):
                    st.write(f"Share: {article['title']}")

            with col4:
                # Read more button
                if article.get('url'):
                    st.link_button("📖 Read Full", article['url'])

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

    def render_main_content(self, articles: List[Dict[str, Any]], gemini_api_key: str = None):
        """Render the main content area"""

        if st.session_state.current_view == 'Saved Articles':
            st.markdown('<div class="main-header"><h1>💾 Your Saved Articles</h1></div>', unsafe_allow_html=True)
            articles_to_show = st.session_state.saved_articles
            if not articles_to_show:
                st.info("📝 No saved articles yet. Save some articles from the 'All News' view!")
                return
        else:
            st.markdown('<div class="main-header"><h1>📰 Personalized News Digest</h1></div>', unsafe_allow_html=True)
            articles_to_show = [a for a in articles if a['category'] in st.session_state.selected_categories]

            if not articles_to_show:
                st.warning("No articles found for your selected categories.")
                return

        # Search functionality
        search_query = st.text_input("🔍 Search articles...", placeholder="Enter keywords to search")
        if search_query:
            articles_to_show = [
                a for a in articles_to_show 
                if search_query.lower() in a['title'].lower() or search_query.lower() in a['summary'].lower()
            ]

        # Display articles count
        st.info(f"📊 Showing {len(articles_to_show)} articles")

        # Render articles
        for article in articles_to_show:
            self.render_article_card(article, gemini_api_key)

    def run(self):
        """Main application runner"""
        news_api_key, gemini_api_key = self.render_sidebar()

        # Get articles
        if news_api_key:
            articles = self.get_news_api_data(st.session_state.selected_categories, news_api_key)
        else:
            articles = self.get_mock_news_data()
            st.info("🔑 Using demo data. Add your NewsAPI key for real news!")

        # Render main content
        self.render_main_content(articles, gemini_api_key)

        # Instructions
        with st.expander("📖 How to Use This App"):
            st.markdown("""
            ### 🚀 Getting Started
            1. **Add API Keys** (optional): Get free keys from NewsAPI.org and Google AI Studio
            2. **Select Categories**: Choose your interests from the sidebar
            3. **Browse Articles**: Read summaries and rate articles
            4. **Save Articles**: Keep favorites for later reading

            ### 🆓 Demo Mode
            Without API keys, the app uses demo data to showcase functionality.
            """)

# Run the application
if __name__ == "__main__":
    app = NewsDigestApp()
    app.run()
