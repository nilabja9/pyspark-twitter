#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PythonCloudScript import clean_tweet, analyze_sentiment_polarity, analyze_sentiment_subjectivity, analyze_sentiment_combined

def test_sentiment_analysis_equivalence():
    """Test that the optimized combined function produces the same results as separate functions"""
    
    test_tweets = [
        "I love this amazing product! #awesome #great",
        "This is terrible and I hate it #bad #awful", 
        "This is just okay, nothing special #neutral",
        "@user Check out this link: https://example.com #link",
        "RT @someone: Great news everyone! 🎉",
        ""
    ]
    
    print("Testing sentiment analysis optimization...")
    print("=" * 50)
    
    all_tests_passed = True
    
    for i, tweet in enumerate(test_tweets):
        print(f"\nTest {i+1}: {repr(tweet)}")
        
        original_polarity = analyze_sentiment_polarity(tweet)
        original_subjectivity = analyze_sentiment_subjectivity(tweet)
        
        combined_polarity, combined_subjectivity = analyze_sentiment_combined(tweet)
        
        polarity_match = original_polarity == combined_polarity
        subjectivity_match = original_subjectivity == combined_subjectivity
        
        print(f"  Original: polarity={original_polarity}, subjectivity={original_subjectivity}")
        print(f"  Combined: polarity={combined_polarity}, subjectivity={combined_subjectivity}")
        print(f"  Match: polarity={polarity_match}, subjectivity={subjectivity_match}")
        
        if not (polarity_match and subjectivity_match):
            all_tests_passed = False
            print("  ❌ FAILED")
        else:
            print("  ✅ PASSED")
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests PASSED! The optimization maintains functional equivalence.")
    else:
        print("❌ Some tests FAILED! The optimization may have introduced bugs.")
    
    return all_tests_passed

if __name__ == "__main__":
    test_sentiment_analysis_equivalence()
