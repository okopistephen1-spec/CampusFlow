from pathlib import Path
from datetime import datetime


QUESTIONS = [
    {
        "question": (
            "Q1. Ticket T001 is open and unassigned. "
            "A user tries to move it to in_progress. What should happen?"
        ),
        "options": {
            "A": "Accept the transition",
            "B": "Reject the transition and preserve all data",
            "C": "Resolve the ticket automatically",
            "D": "Remove the ticket",
        },
        "answer": "B",
    },
    {
        "question": (
            "Q2. The application has zero tickets. "
            "What should the resolution percentage display?"
        ),
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
    },
    {
        "question": (
            "Q3. You search for title='wifi', category='Network', "
            "and status='open'. Which tickets should match?"
        ),
        "options": {
            "A": "Tickets matching any one of the three filters",
            "B": "Every ticket in the system",
            "C": "Only tickets matching all three filters",
            "D": "Only tickets with high priority",
        },
        "answer": "C",
    },
    {
        "question": (
            "Q4. Why should searching for tickets not modify "
            "the original ticket collection?"
        ),
        "options": {
            "A": "To prevent searches from accidentally changing data",
            "B": "To make every ticket resolved",
            "C": "To delete duplicate tickets automatically",
            "D": "To prevent users from viewing tickets",
        },
        "answer": "A",
    },
    {
        "question": (
            "Q5. A ticket is already resolved. A user tries to add "
            "a new note. What should happen if resolved tickets "
            "cannot receive new notes?"
        ),
        "options": {
            "A": "Add the note and reopen the ticket automatically",
            "B": "Delete the existing notes",
            "C": "Accept the note without checking the ticket",
            "D": "Reject the note and preserve the existing data",
        },
        "answer": "D",
    },
    {
        "question": (
            "Q6. Why should automated tests check the ticket's state "
            "after an invalid operation?"
        ),
        "options": {
            "A": "To make the test output longer",
            "B": "To verify that rejected operations did not change data",
            "C": "To generate new ticket IDs",
            "D": "To skip input validation",
        },
        "answer": "B",
    },
]


def right_score(questions, user_answers):
    """Calculate the number of correct answers."""

    score = 0

    for question, user_answer in zip(questions, user_answers):
        if user_answer.upper() == question["answer"]:
            score += 1

    return score

def save_learning_note(explanations, score):
    """Save quiz results and explanations to a local learning note."""

    
    project_root = Path(__file__).resolve().parent.parent

    
    note_path = project_root / "docs" / "learning-note.md"

    
    note_path.parent.mkdir(parents=True, exist_ok=True)

    
    with note_path.open("a", encoding="utf-8") as file:
        file.write("\n## Engineering Understanding Check\n")
        file.write(f"Date: {datetime.now():%Y-%m-%d %H:%M}\n")
        file.write(f"Score: {score}/{len(QUESTIONS)}\n\n")

        for item in explanations:
            file.write(
                f"### Question {item['question_number']}\n"
            )
            file.write(f"{item['explanation']}\n\n")

        file.write("---\n")

    print(f"\nLearning note saved successfully to: {note_path}")


def run_understanding_check():
    """Run the interactive Engineering Understanding Check."""

    print("\n======================================")
    print("  Engineering Understanding Check")
    print("======================================")

    print("\nAnswer all the question by entering A, B, C, or D.")
    print("You will receive one point for each correct answer.")

    user_answers = []

    for question in QUESTIONS:
        print("\n" + question["question"])

        for option, description in question["options"].items():
            print(f"{option}. {description}")

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer in question["options"]:
                user_answers.append(answer)
                break

            print("Invalid choice. Please enter A, B, C, or D.")

    score = right_score(QUESTIONS, user_answers)

    print("\n======================================")
    print("           QUIZ RESULTS")
    print("======================================")
    print(f"Your score: {score}/{len(QUESTIONS)}")

    print("\n======================================")
    print("       EXPLAIN YOUR ANSWERS")
    print("======================================")

    explanations = []

    for question_number in (1, 2):
        print(f"\nExplain your reasoning for Question {question_number}.")

        explanation = input("Your explanation: ").strip()

        while not explanation:
            print("Your explanation cannot be empty.")
            explanation = input("Your explanation: ").strip()

        explanations.append({
            "question_number": question_number,
            "explanation": explanation
        })

    save_learning_note(explanations, score)

    print("\nYour learning note has been saved to docs/learning-note.md")
        

if __name__ == "__main__":
    run_understanding_check()