import os
import tempfile
import unittest

from campusflow.understanding_check import (
    QUESTIONS,
    right_score,
    run_understanding_check,
)


ALL_CORRECT = [question["answer"] for question in QUESTIONS]


class TestQuizScoring(unittest.TestCase):
    """Scoring is generic over the question bank (kept separate from it)."""

    def test_all_correct_scores_six(self):
        self.assertEqual(len(QUESTIONS), 6)
        self.assertEqual(right_score(QUESTIONS, ALL_CORRECT), 6)

    def test_one_wrong_answer_scores_five(self):
        answers = list(ALL_CORRECT)
        answers[0] = "A"

        self.assertEqual(right_score(QUESTIONS, answers), 5)

    def test_score_uses_normalized_answers(self):
        messy = [answer.casefold() for answer in ALL_CORRECT]

        self.assertEqual(right_score(QUESTIONS, messy), 6)


class TestQuizRun(unittest.TestCase):
    """Acceptance case 14: invalid answer rejected; scoring correct."""

    def run_quiz(self, inputs, note_path):
        printed = []

        score, answers, explanations = run_understanding_check(
            input_func=lambda prompt: next(inputs),
            print_func=printed.append,
            note_path=note_path,
        )

        return score, answers, explanations, printed

    def test_invalid_answer_reprompts_then_records_valid_answer(self):
        # Q1: an invalid "E" first, then the correct B; rest all correct.
        inputs = iter(
            ["E", "B"] + ALL_CORRECT[1:] + ["1", "rule invariant reasons", "5", "validate before replacing memory"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            score, answers, _, printed = self.run_quiz(
                inputs, os.path.join(tmp, "learning-note.md"))

        self.assertIn("Invalid choice. Please enter A, B, C, or D.", printed)
        self.assertEqual(answers[0], "B")
        self.assertEqual(score, 6)
        self.assertIn("Your score: 6/6", printed)

    def test_invalid_answer_not_counted_as_response(self):
        inputs = iter(
            ["Z", "B"] + ALL_CORRECT[1:] + ["2", "avoided division by zero", "6", "review needs negative tests"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            _, answers, _, _ = self.run_quiz(
                inputs, os.path.join(tmp, "learning-note.md"))

        self.assertEqual(len(answers), 6)
        self.assertNotIn("Z", answers)

    def test_wrong_answer_lowers_score(self):
        inputs = iter(
            ["A"] + ALL_CORRECT[1:] + ["1", "reasoning here", "3", "AND reasoning here"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            score, answers, _, _ = self.run_quiz(
                inputs, os.path.join(tmp, "learning-note.md"))

        self.assertEqual(score, 5)
        self.assertEqual(answers[0], "A")

    def test_invalid_explanation_question_number_reprompts(self):
        inputs = iter(
            ALL_CORRECT[:] + ["9", "1", "first explanation", "4", "second explanation"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            _, _, explanations, printed = self.run_quiz(
                inputs, os.path.join(tmp, "learning-note.md"))

        self.assertTrue(any("Invalid question number" in line for line in printed))
        self.assertEqual(
            [item["question_number"] for item in explanations],
            [1, 4],
        )

    def test_learning_note_saved_with_score_and_explanations(self):
        inputs = iter(
            ALL_CORRECT[:] + ["1", "unassigned tickets stay out of progress", "5", "validate whole file first"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "learning-note.md")
            score, _, _, printed = self.run_quiz(inputs, path)

            with open(path, encoding="utf-8") as file:
                content = file.read()

        self.assertEqual(score, 6)
        self.assertIn("Score: 6/6", content)
        self.assertIn("unassigned tickets stay out of progress", content)
        self.assertIn("validate whole file first", content)
        self.assertTrue(any("learning-note.md" in line for line in printed))

    def test_blank_explanation_reprompts(self):
        inputs = iter(
            ALL_CORRECT[:] + ["1", "", "real explanation after retry", "2", "second real explanation"]
        )

        with tempfile.TemporaryDirectory() as tmp:
            _, _, explanations, printed = self.run_quiz(
                inputs, os.path.join(tmp, "learning-note.md"))

        self.assertIn("Your explanation cannot be empty.", printed)
        self.assertEqual(explanations[0]["explanation"], "real explanation after retry")


if __name__ == "__main__":
    unittest.main()
