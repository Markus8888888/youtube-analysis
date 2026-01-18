import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def render_sentiment_gauge(sentiment_score):
    """
    Renders a premium circular gauge for sentiment score (-1 to 1).
    """
    # Normalize -1 to 1 score to 0-100 for the gauge
    value = (sentiment_score + 1) * 50
    
    # Determine color based on sentiment
    if value < 40:
        color = "#ef4444"  # Red
    elif value > 60:
        color = "#10b981"  # Green
    else:
        color = "#f59e0b"  # Orange
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        number = {'suffix': "%", 'font': {'size': 48, 'color': 'white'}},
        title = {'text': "Overall Sentiment", 'font': {'size': 16, 'color': '#9ca3af'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.2)"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 100], 'color': 'rgba(255,255,255,0.05)'}
            ],
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_topic_chart(topics_data):
    """
    Renders a premium horizontal bar chart for top topics.
    """
    df = pd.DataFrame(topics_data)
    
    if df.empty:
        st.info("No topics identified yet.")
        return
    
    fig = px.bar(
        df.sort_values('Count'), 
        x='Count', 
        y='Topic', 
        orientation='h',
        title="🔥 Trending Topics",
    )
    
    # Premium gradient colors
    fig.update_traces(
        marker=dict(
            color=df['Count'],
            colorscale=[[0, '#9333ea'], [1, '#ec4899']],
            line=dict(width=0)
        ),
        hovertemplate='<b>%{y}</b><br>%{x} mentions<extra></extra>'
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white', 'size': 12},
        title={'font': {'size': 16, 'color': 'white'}},
        xaxis={'gridcolor': 'rgba(255,255,255,0.1)', 'color': '#9ca3af'},
        yaxis={'color': 'white'},
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)