from pathlib import Path
from datetime import datetime


# Question bank required by the CampusFlow Next guide (section 05).
# DATA ONLY: scoring logic (right_score) reads the "answer" field generically,
# so editing a question never requires touching the scoring code.
QUESTIONS = [
    {
        "question": (
            "Q1. Ticket T001 is open and unassigned. A user tries to move it "
            "to in_progress. What should CampusFlow do?"
        ),
        "options": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket",
        },
        "answer": "B",
        "feedback": (
            "Requirement A: an unassigned open ticket must not enter "
            "in_progress, and a rejected action leaves all data unchanged "
            "(workflow.update_ticket_status raises ValueError)."
        ),
    },
    {
        "question": (
            "Q2. The app has zero tickets. What should the resolution "
            "percentage display?"
        ),
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation",
        },
        "answer": "C",
        "feedback": (
            "Requirement D: reports.py only divides when total > 0, so an "
            "empty dataset shows 0% instead of ZeroDivisionError."
        ),
    },
    {
        "question": (
            "Q3. Filter title='wifi', category='Network', status='open'. "
            "Which records should match?"
        ),
        "options": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records",
        },
        "answer": "B",
        "feedback": (
            "Requirement C: supplied filters combine with logical AND "
            "(workflow.search_tickets)."
        ),
    },
    {
        "question": (
            "Q4. A resolved ticket receives 'Add note'. What should happen?"
        ),
        "options": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently",
        },
        "answer": "C",
        "feedback": (
            "Requirement B: only open or in_progress tickets accept notes; "
            "existing notes are preserved through resolve and reopen."
        ),
    },
    {
        "question": (
            "Q5. The JSON file includes two tickets with the same ID. "
            "What should load do?"
        ),
        "options": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently",
        },
        "answer": "C",
        "feedback": (
            "Requirement E: the whole file is validated BEFORE memory is "
            "replaced; a rejected load keeps the current collection intact."
        ),
    },
    {
        "question": (
            "Q6. A PR changes validation but has no negative-case tests. "
            "Best review action?"
        ),
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it",
        },
        "answer": "B",
        "feedback": (
            "Peer review must name a specific behaviour or missing test; "
            "validation changes need negative tests proving rejected "
            "actions change nothing."
        ),
    },
]

VALID_ANSWERS = ("A", "B", "C", "D")
QUESTION_NUMBERS = tuple(str(question_number) for question_number in range(1, len(QUESTIONS) + 1))


def right_score(questions, user_answers):
    """Calculate the number of correct answers (one point each)."""

    score = 0

    for question, user_answer in zip(questions, user_answers):
        if str(user_answer).strip().upper() == question["answer"]:
            score += 1

    return score


def save_learning_note(explanations, score, note_path=None):
    """Save quiz results and explanations to a local learning note."""

    if note_path is None:
        project_root = Path(__file__).resolve().parent.parent
        note_path = project_root / "docs" / "learning-note.md"

    note_path = Path(note_path)
    note_path.parent.mkdir(parents=True, exist_ok=True)

    with note_path.open("a", encoding="utf-8") as file:
        file.write("\n## Engineering Understanding Check\n")
        file.write(f"Date: {datetime.now():%Y-%m-%d %H:%M}\n")
        file.write(f"Score: {score}/{len(QUESTIONS)}\n\n")

        for item in explanations:
            file.write(f"### Question {item['question_number']}\n")
            file.write(f"{item['explanation']}\n\n")

        file.write("---\n")

    return note_path


def ask_valid_answer(question, input_func, print_func):
    """Prompt until the user enters a valid A/B/C/D answer."""

    while True:
        answer = str(input_func("Your answer (A/B/C/D): ")).strip().upper()

        if answer in question["options"]:
            return answer

        print_func("Invalid choice. Please enter A, B, C, or D.")


def ask_explanations(input_func, print_func, count=2):
    """Ask the user to explain `count` of their answers in their own words.

    Explanations are recorded for mentor discussion; they are never
    auto-graded on keywords.
    """

    explanations = []

    while len(explanations) < count:
        number = str(input_func(
            f"Which question would you like to explain? ({'/'.join(QUESTION_NUMBERS)}): "
        )).strip()

        if number not in QUESTION_NUMBERS:
            print_func(f"Invalid question number. Choose from: {', '.join(QUESTION_NUMBERS)}.")
            continue

        explanation = str(input_func(
            f"Explain your answer to Q{number} in your own words: "
        )).strip()

        while not explanation:
            print_func("Your explanation cannot be empty.")
            explanation = str(input_func("Your explanation: ")).strip()

        explanations.append({
            "question_number": int(number),
            "explanation": explanation,
        })

    return explanations


def run_understanding_check(input_func=input, print_func=print, note_path=None):
    """Run the interactive Engineering Understanding Check.

    input_func / print_func can be injected so the whole flow is testable
    without typing manually (milestone B6).
    Returns (score, user_answers, explanations).
    """

    print_func("\n======================================")
    print_func("  Engineering Understanding Check")
    print_func("======================================")
    print_func("\nAnswer each question by entering A, B, C, or D.")
    print_func("You will receive one point for each correct answer.")

    user_answers = []

    for question in QUESTIONS:
        print_func("\n" + question["question"])

        for option, description in question["options"].items():
            print_func(f"{option}. {description}")

        answer = ask_valid_answer(question, input_func, print_func)
        user_answers.append(answer)

        print_func(f"Recorded: {answer}")
        print_func(f"Feedback: {question['feedback']}")

    score = right_score(QUESTIONS, user_answers)

    print_func("\n======================================")
    print_func("           QUIZ RESULTS")
    print_func("======================================")
    print_func(f"Your score: {score}/{len(QUESTIONS)}")

    print_func("\nNow explain, in your own words, TWO of your answers.")
    print_func("These are recorded for mentor discussion, not auto-graded.")

    explanations = ask_explanations(input_func, print_func)

    saved_to = save_learning_note(explanations, score, note_path=note_path)

    print_func(f"\nYour learning note has been saved to: {saved_to}")

    return score, user_answers, explanations


if __name__ == "__main__":
    run_understanding_check()
