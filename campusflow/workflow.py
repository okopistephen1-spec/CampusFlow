def find_ticket(tickets, ticket_id):
    """Find a ticket using its ID."""

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(ticket_or_tickets, ticket_id_or_name, staff_name=None):
    """Assign a ticket to a staff member."""

    # Allow either a ticket dictionary or a ticket collection.
    if isinstance(ticket_or_tickets, dict):
        ticket = ticket_or_tickets
        staff_name = ticket_id_or_name

    else:
        ticket = find_ticket(ticket_or_tickets, ticket_id_or_name)

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be blank.")

    if ticket["status"] == "resolved":
        raise ValueError(
            "Reopen the ticket before modifying a resolved ticket."
        )

    ticket["assigned_to"] = staff_name.strip()

    return ticket


def update_ticket_status(ticket, new_status):
    """Update a ticket's status while enforcing workflow rules."""

    if not isinstance(new_status, str):
        raise ValueError("Status must be text.")

    new_status = new_status.strip().lower()

    valid_statuses = {"open", "in_progress", "resolved"}

    if new_status not in valid_statuses:
        raise ValueError(
            "Invalid status. Choose open, in_progress, or resolved."
        )

    current_status = ticket["status"]

    # A resolved ticket must be reopened before further changes.
    if current_status == "resolved":
        if new_status != "open":
            raise ValueError(
                "Reopen a resolved ticket before making further changes."
            )

        ticket["status"] = "open"
        return ticket

    # An open ticket must pass through in_progress before resolution.
    if current_status == "open" and new_status == "resolved":
        raise ValueError(
            "Move the ticket to in_progress before resolving it."
        )

    # A ticket must be assigned before entering in_progress.
    if current_status == "open" and new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError(
                "Assign the ticket before moving it to in_progress."
            )

    ticket["status"] = new_status

    return ticket


def get_work_queue(tickets):
    """Return open tickets ordered by priority and ticket ID."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    open_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] == "open"
    ]

    return sorted(
        open_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"].lower()],
            int(ticket["id"][1:]),
        ),
    )


def add_note(ticket, author, message):
    """Add a note to an open or in-progress ticket."""

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Author name cannot be blank.")

    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError(
            "Note message must contain between 5 and 300 characters."
        )

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before adding a note.")

    notes = ticket.get("notes")

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be stored as a list.")

    highest_id = 0

    for existing_note in notes:
        if not isinstance(existing_note, dict):
            raise ValueError("Invalid note data.")

        note_id = existing_note.get("note_id", "")

        if (
            isinstance(note_id, str)
            and len(note_id) == 4
            and note_id.startswith("N")
            and note_id[1:].isdigit()
        ):
            highest_id = max(highest_id, int(note_id[1:]))

    new_note = {
        "note_id": f"N{highest_id + 1:03d}",
        "author": author.strip(),
        "message": message,
    }

    notes.append(new_note)

    return new_note


def view_notes(ticket):
    """Return a ticket's notes in note-ID order."""

    notes = ticket.get("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be stored as a list.")

    for note in notes:
        if not isinstance(note, dict):
            raise ValueError("Invalid note data.")

        note_id = note.get("note_id", "")

        if not (
            isinstance(note_id, str)
            and len(note_id) == 4
            and note_id.startswith("N")
            and note_id[1:].isdigit()
        ):
            raise ValueError("Invalid note ID.")

    return sorted(
        notes,
        key=lambda note: int(note["note_id"][1:]),
    )