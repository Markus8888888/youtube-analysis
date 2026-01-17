"""
Integration tests for the AI Brain
Tests all 4 tasks: sentiment analysis, chatbot, query categorization, insights
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from brain import AIBrain

def test_health_check():
    """Verify all components are working"""
    print("\n" + "="*60)
    print("TEST 0: Health Check")
    print("="*60)
    
    brain = AIBrain()
    health = brain.health_check()
    
    print(f"Status: {health['status']}")
    for key, value in health.items():
        if key != "status":
            print(f"  {key}: {value}")
    
    return health["status"] == "healthy"


def test_sentiment_analysis():
    """Task 1: Test single comment analysis"""
    print("\n" + "="*60)
    print("TEST 1: Sentiment Analysis (Single Comment)")
    print("="*60)
    
    brain = AIBrain()
    
    test_comments = [
        "This is an amazing video! Best content ever!",
        "Terrible quality. Waste of time.",
        "It's okay, nothing special but decent."
    ]
    
    for comment in test_comments:
        print(f"\nAnalyzing: '{comment}'")
        result = brain.analyze_comments(comment)
        
        if "error" not in result:
            print(f"  Sentiment: {result.get('sentiment_score', 'N/A')}")
            print(f"  Themes: {result.get('top_3_themes', [])}")
            print(f"  Controversy: {result.get('controversy_level', 'N/A')}/10")
        else:
            print(f"  Error: {result['error']}")
    
    return True


def test_batch_analysis():
    """Task 1: Test batch comment analysis"""
    print("\n" + "="*60)
    print("TEST 1B: Batch Comment Analysis")
    print("="*60)
    
    brain = AIBrain()
    
    comments = [
        "Love the editing style!",
        "Audio quality needs work",
        "Great explanation of the topic",
        "Too long and boring",
        "Best tutorial I've found!"
    ]
    
    print(f"\nAnalyzing {len(comments)} comments...")
    results = brain.analyze_batch_comments(comments)
    
    print(f"\nAverage Sentiment: {results['aggregated']['avg_sentiment']:.2f}")
    print(f"Average Controversy: {results['aggregated']['avg_controversy']:.1f}/10")
    print(f"Most common themes: {dict(sorted(results['aggregated']['theme_frequency'].items(), key=lambda x: x[1], reverse=True)[:3])}")
    
    return True


def test_chatbot():
    """Task 2: Test conversational chatbot"""
    print("\n" + "="*60)
    print("TEST 2: Chatbot Conversation")
    print("="*60)
    
    brain = AIBrain()
    
    questions = [
        "How can I improve my video engagement?",
        "What does sentiment analysis tell me?",
        "Can you explain the controversy metric?"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        response = brain.chat(question)
        # Print first 200 chars to keep output manageable
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"A: {preview}")
    
    print(f"\n[Conversation history maintained - {len(brain.chat_manager.chat_session.history)} turns]")
    
    # Clear history for next test
    brain.clear_chat_history()
    
    return True


def test_query_categorization():
    """Task 3: Test query routing"""
    print("\n" + "="*60)
    print("TEST 3: Query Categorization")
    print("="*60)
    
    brain = AIBrain()
    
    queries = [
        "Are people liking my video?",  # sentiment
        "How many views did I get?",     # engagement
        "What topics are viewers interested in?",  # content
        "Tell me a joke"                 # general
    ]
    
    for query in queries:
        category = brain.categorize_query(query)
        print(f"Query: '{query}'")
        print(f"  Category: {category}\n")
    
    return True


def test_insights_generation():
    """Task 4: Test insight generation"""
    print("\n" + "="*60)
    print("TEST 4: Insight Generation")
    print("="*60)
    
    brain = AIBrain()
    
    # Mock analytics data
    analytics_data = {
        "avg_sentiment": 0.72,
        "avg_controversy": 2.5,
        "total_comments": 1250,
        "top_themes": ["editing", "audio quality", "length"],
        "theme_frequency": {
            "editing": 340,
            "audio quality": 285,
            "length": 198
        }
    }
    
    print("Input analytics data:")
    print(f"  Average Sentiment: {analytics_data['avg_sentiment']}")
    print(f"  Controversy Level: {analytics_data['avg_controversy']}/10")
    print(f"  Total Comments: {analytics_data['total_comments']}")
    print(f"  Top Themes: {', '.join(analytics_data['top_themes'])}")
    
    print("\nGenerating insights...")
    insights = brain.generate_insights(analytics_data)
    print(f"\n{insights[:500]}...")  # Print first 500 chars
    
    return True


def test_full_pipeline():
    """Task 4: Test complete analysis pipeline"""
    print("\n" + "="*60)
    print("TEST 5: Full Analysis Pipeline")
    print("="*60)
    
    brain = AIBrain()
    
    comments = [
        "Excellent production quality!",
        "The thumbnail is misleading",
        "Very informative, learned a lot",
        "Audio sync issues throughout",
        "Best video in the series!"
    ]
    
    print(f"Running full analysis on {len(comments)} comments...\n")
    report = brain.full_analysis(comments, include_insights=True)
    
    print(f"Status: {report['status']}")
    print(f"Comments analyzed: {report['comment_count']}")
    print(f"Average sentiment: {report['sentiment_analysis']['avg_sentiment']:.2f}")
    print(f"Average controversy: {report['sentiment_analysis']['avg_controversy']:.1f}/10")
    print(f"\nTop recommendations:")
    print(report['insights'][:300] + "...")
    
    return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI BRAIN INTEGRATION TEST SUITE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Batch Analysis", test_batch_analysis),
        ("Chatbot", test_chatbot),
        ("Query Categorization", test_query_categorization),
        ("Insights Generation", test_insights_generation),
        ("Full Pipeline", test_full_pipeline),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} FAILED: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_status in results.items():
        status = "[PASS]" if passed_status else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n*** All tests passed! AI Brain is ready! ***")
    else:
        print(f"\n*** {total - passed} test(s) failed. Check errors above. ***")
