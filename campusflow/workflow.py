def find_ticket(tickets, ticket_id):
    """Find a ticket by its ID."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id} was not found.")


def assign_ticket(ticket_or_tickets, ticket_id_or_name, staff_name=None):
    """Assign a ticket to a staff member."""
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

    if new_status not in {"open", "in_progress", "resolved"}:
        raise ValueError(
            "Invalid status. Choose open, in_progress, or resolved."
        )

    current_status = ticket["status"]

    if current_status == "resolved":
        if new_status != "open":
            raise ValueError(
                "Reopen a resolved ticket before making further changes."
            )

        ticket["status"] = "open"
        return ticket

    if current_status == "open" and new_status == "resolved":
        raise ValueError(
            "Move the ticket to in_progress before resolving it."
        )

    if current_status == "open" and new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError(
                "Assign the ticket before moving it to in_progress."
            )

    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets ordered by priority and ID."""
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in {"open", "in_progress"}
    ]

    return sorted(
        unresolved_tickets,
        key=lambda ticket: (
            priority_order[ticket["priority"].lower()],
            int(ticket["id"][1:]),
        ),
    )