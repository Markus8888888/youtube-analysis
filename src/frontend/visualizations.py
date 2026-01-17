import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def render_sentiment_gauge(sentiment_score):
    """
    Renders a gauge chart for sentiment score (-1 to 1).
    """
    # Normalize -1 to 1 score to 0-100 for the gauge
    value = (sentiment_score + 1) * 50
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': "Overall Sentiment"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF0000" if value < 40 else "#00CC96" if value > 60 else "#FFA500"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "gray"},
                {'range': [60, 100], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

def render_topic_chart(topics_data):
    """
    Renders a horizontal bar chart for top topics.
    Expects a dict or dataframe: {'Topic': [], 'Count': []}
    """
    df = pd.DataFrame(topics_data)
    
    if df.empty:
        st.info("No topics identified yet.")
        return

    fig = px.bar(
        df, 
        x='Count', 
        y='Topic', 
        orientation='h',
        title="🔥 Trending Topics",
        color='Count',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=350)
    st.plotly_chart(fig, use_container_width=True)