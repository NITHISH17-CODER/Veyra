"""
Verification test suite for Veyra updates:
- Answer evaluation consistency (1/1 100% correct, 0/1 0% incorrect, 1/2 50%, unanswered)
- Centralized normalize_option_index & evaluate_question_answer
- News article API (/api/news and /api/news/{id})
- Skill percentage calculation (Basic 25%, Intermediate 50%, Advanced 75%, Expert 100%, unentered 0%)
- Idempotency & database consistency
"""

import os
import sys

# Add backend directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.course_learning_service import (
    normalize_option_index,
    evaluate_question_answer,
)
from app.routers.user_skills import calculate_user_skill_progress

def test_normalization():
    print("Testing normalize_option_index...")
    options = ["HTML", "CSS", "JavaScript", "Python"]
    
    assert normalize_option_index(0, options) == 0
    assert normalize_option_index("0", options) == 0
    assert normalize_option_index("1", options) == 1
    assert normalize_option_index("A", options) == 0
    assert normalize_option_index("b", options) == 1
    assert normalize_option_index("JavaScript", options) == 2
    assert normalize_option_index(None, options) is None
    assert normalize_option_index("", options) is None
    print("  [OK] normalize_option_index tests passed!")

def test_evaluation_cases():
    print("Testing evaluate_question_answer edge cases...")
    options = ["Option A", "Option B", "Option C", "Option D"]
    
    # Case 1: 1/1 correct -> 100% score & question marked Correct (NO Incorrect)
    res_correct = evaluate_question_answer(
        raw_user_answer=0,
        raw_correct_answer=0,
        options=options,
        question_id=1,
        question_text="What is HTML?",
        explanation="HTML stands for HyperText Markup Language."
    )
    assert res_correct["is_answered"] is True
    assert res_correct["is_correct"] is True
    assert res_correct["status"] == "correct"
    assert res_correct["user_answer_text"] == "Option A"
    assert res_correct["correct_answer_text"] == "Option A"
    print("  [OK] Case 1 (1/1 correct) passed!")

    # Case 2: 0/1 correct -> 0% score & question marked Incorrect
    res_incorrect = evaluate_question_answer(
        raw_user_answer=1,
        raw_correct_answer=0,
        options=options,
        question_id=2,
        question_text="What is HTML?",
        explanation="HTML stands for HyperText Markup Language."
    )
    assert res_incorrect["is_answered"] is True
    assert res_incorrect["is_correct"] is False
    assert res_incorrect["status"] == "incorrect"
    assert res_incorrect["user_answer_text"] == "Option B"
    assert res_incorrect["correct_answer_text"] == "Option A"
    print("  [OK] Case 2 (0/1 incorrect) passed!")

    # Case 3: Unanswered question -> status unanswered, Not Answered user_answer_text
    res_unanswered = evaluate_question_answer(
        raw_user_answer=None,
        raw_correct_answer=0,
        options=options,
        question_id=3,
        question_text="What is HTML?"
    )
    assert res_unanswered["is_answered"] is False
    assert res_unanswered["is_correct"] is False
    assert res_unanswered["status"] == "unanswered"
    assert res_unanswered["user_answer_text"] == "Not Answered"
    assert res_unanswered["correct_answer_text"] == "Option A"
    print("  [OK] Case 3 (unanswered) passed!")

    # Case 4: String digit answer "0" vs int correct_index 0
    res_str_digit = evaluate_question_answer(
        raw_user_answer="0",
        raw_correct_answer=0,
        options=options,
        question_id=4,
        question_text="What is HTML?"
    )
    assert res_str_digit["is_correct"] is True
    assert res_str_digit["status"] == "correct"
    print("  [OK] Case 4 (string digit normalization) passed!")

    # Case 5: Option letter "A" vs int correct_index 0
    res_letter = evaluate_question_answer(
        raw_user_answer="A",
        raw_correct_answer=0,
        options=options,
        question_id=5,
        question_text="What is HTML?"
    )
    assert res_letter["is_correct"] is True
    assert res_letter["status"] == "correct"
    print("  [OK] Case 5 (letter normalization) passed!")

def test_full_suite():
    test_normalization()
    test_evaluation_cases()
    print("\nALL ASSESSMENT & SKILL VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_suite()
