import json
import os
import tempfile
from pathlib import Path


def save_tickets(tickets, file_path):
    """
    Save a list of ticket dictionaries to a JSON file.

    Args:
        tickets (list): A list of ticket dictionaries.
        file_path (str or Path): The destination JSON file path.
    """
    file_path = Path(file_path)

    # Create parent directories if they don't exist.
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None

    try:
        # Create a temporary file in the same directory.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=file_path.parent,
            delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

            json.dump(tickets, temp_file, indent=4)
            temp_file.flush()
            os.fsync(temp_file.fileno())

        # Replace the destination file with the completed temporary file.
        os.replace(temp_path, file_path)

    finally:
        # Clean up the temporary file if it still exists.
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def load_tickets(file_path):
    file_path = Path(file_path)

    # If the file doesn't exist, return an empty list.
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path}: {error}"
        ) from error

    # Ensure the JSON data is a list.
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list")

    # Ensure each item is a dictionary.
    if not all(isinstance(ticket, dict) for ticket in tickets):
        raise ValueError("Every ticket must be a JSON object")

    return tickets
