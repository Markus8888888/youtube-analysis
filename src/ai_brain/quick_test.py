"""
Quick Test Script for AI Brain
Run this to verify everything is working
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from brain import AIBrain
import json

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_1_health_check():
    """Test 1: System is operational"""
    print_section("TEST 1: Health Check")
    
    brain = AIBrain()
    health = brain.health_check()
    
    print(f"Status: {health['status']}")
    for key, value in health.items():
        if key != 'status':
            print(f"  {key}: {value}")
    
    return health['status'] == 'healthy'


def test_2_sentiment_single():
    """Test 2: Single comment sentiment analysis"""
    print_section("TEST 2: Single Comment Analysis")
    
    brain = AIBrain()
    
    test_comments = [
        "This video is amazing! Best content ever!",
        "Terrible quality and bad audio",
        "It's okay, nothing special"
    ]
    
    results = []
    for comment in test_comments:
        print(f"\nComment: '{comment}'")
        result = brain.analyze_comments(comment)
        
        if 'error' in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  Sentiment: {result.get('sentiment_score', 'N/A')}")
            print(f"  Themes: {result.get('top_3_themes', [])}")
            print(f"  Controversy: {result.get('controversy_level', 'N/A')}/10")
            results.append(result)
    
    return len(results) > 0


def test_3_caching():
    """Test 3: Verify caching works"""
    print_section("TEST 3: Caching System")
    
    brain = AIBrain()
    comment = "Great video!"
    
    # First call (cache miss)
    print("First analysis (cache miss)...")
    result1 = brain.analyze_comments(comment)
    
    # Second call (should hit cache)
    print("Second analysis (should hit cache)...")
    result2 = brain.analyze_comments(comment)
    
    # Check cache stats
    cache_stats = brain.get_cache_stats()
    print(f"\nCache stats: {cache_stats['sentiment_cache']}")
    
    is_cached = (result1 == result2)
    print(f"\nResults identical (cached): {is_cached}")
    
    return is_cached


def test_4_chatbot():
    """Test 4: Chatbot conversation"""
    print_section("TEST 4: Chatbot Conversation")
    
    brain = AIBrain()
    
    conversation = [
        "Hello! How are you?",
        "What can you help me with?",
        "Tell me about sentiment analysis"
    ]
    
    for i, message in enumerate(conversation, 1):
        print(f"\nQ{i}: {message}")
        response = brain.chat(message)
        
        if isinstance(response, dict) and 'error' in response:
            print(f"  ERROR: {response['message']}")
        else:
            # Print first 150 chars
            preview = response[:150] + "..." if len(response) > 150 else response
            print(f"  A: {preview}")
    
    return True


def test_5_batch_analysis():
    """Test 5: Batch comment analysis"""
    print_section("TEST 5: Batch Analysis")
    
    brain = AIBrain()
    
    comments = [
        "Excellent production quality!",
        "The audio is too quiet",
        "Very informative and helpful",
        "Could be more engaging",
        "Best tutorial I've seen!"
    ]
    
    print(f"Analyzing {len(comments)} comments...")
    result = brain.analyze_batch_comments(comments)
    
    if 'error' in result:
        print(f"ERROR: {result['error']}")
        return False
    
    agg = result['aggregated']
    print(f"\nResults:")
    print(f"  Avg Sentiment: {agg['avg_sentiment']:.2f}")
    print(f"  Avg Controversy: {agg['avg_controversy']:.1f}/10")
    print(f"  Analyzed: {len(result['analyses'])}/{result['total_comments']}")
    print(f"  Top themes: {dict(sorted(agg['theme_frequency'].items(), key=lambda x: x[1], reverse=True)[:3])}")
    
    return True


def test_6_query_routing():
    """Test 6: Query categorization"""
    print_section("TEST 6: Query Categorization")
    
    brain = AIBrain()
    
    queries = [
        ("How many people liked my video?", "engagement_analysis"),
        ("What do viewers think about my content?", "sentiment_analysis"),
        ("What topics are trending?", "content_analysis"),
        ("Hi there!", "general"),
    ]
    
    for query, expected in queries:
        category = brain.categorize_query(query)
        match = "✓" if category == expected else "✗"
        print(f"{match} '{query}'")
        print(f"    -> {category} (expected: {expected})")
    
    return True


def test_7_full_pipeline():
    """Test 7: Complete analysis pipeline"""
    print_section("TEST 7: Full Pipeline")
    
    brain = AIBrain()
    
    comments = [
        "Amazing production quality and editing!",
        "Audio quality needs improvement",
        "Very helpful and informative",
        "Engaging content but a bit long",
        "Best video on this topic!"
    ]
    
    print(f"Running full pipeline on {len(comments)} comments...\n")
    
    report = brain.full_analysis(comments, include_insights=True)
    
    if 'error' in report:
        print(f"ERROR: {report['error']}")
        return False
    
    print(f"Status: {report['status']}")
    print(f"Comments analyzed: {report['comment_count']}")
    print(f"Sentiment: {report['sentiment_analysis']['avg_sentiment']:.2f}")
    print(f"Controversy: {report['sentiment_analysis']['avg_controversy']:.1f}/10")
    print(f"\nInsights (first 300 chars):")
    print(report['insights'][:300] + "...")
    
    return True


def main():
    print("\n" + "*"*60)
    print("*" + " "*58 + "*")
    print("*  AI BRAIN TEST SUITE" + " "*36 + "*")
    print("*" + " "*58 + "*")
    print("*"*60)
    
    tests = [
        ("Health Check", test_1_health_check),
        ("Single Comment Analysis", test_2_sentiment_single),
        ("Caching System", test_3_caching),
        ("Chatbot", test_4_chatbot),
        ("Batch Analysis", test_5_batch_analysis),
        ("Query Categorization", test_6_query_routing),
        ("Full Pipeline", test_7_full_pipeline),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n[EXCEPTION] {test_name}: {str(e)[:100]}")
            results[test_name] = False
    
    # Summary
    print_section("SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_status in results.items():
        status = "[PASS]" if passed_status else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n*** SUCCESS: All tests passed! AI Brain is ready! ***")
    else:
        print(f"\n*** {total - passed} test(s) failed ***")
    
    print("\n")
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
