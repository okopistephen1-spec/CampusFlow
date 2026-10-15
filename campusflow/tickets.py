def calculate_priority(urgency, affected_users):
    """Calculate ticket priority based on urgency and affected users."""

    urgency = urgency.lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"

    elif urgency == "high" or affected_users >= 10:
        return "high"

    elif urgency == "medium" or affected_users >= 3:
        return "medium"

    else:
        return "low"


def validate_ticket(title):
    """Check that a ticket title is not empty."""

    return isinstance(title, str) and bool(title.strip())


def validate_ticket_id(ticket_id):
    """Check that a ticket ID follows the T001 format."""

    return (
        isinstance(ticket_id, str)
        and len(ticket_id) == 4
        and ticket_id.startswith("T")
        and ticket_id[1:].isdigit()
    )


def validate_urgency(urgency):
    """Check whether the urgency level is valid."""

    return (
        isinstance(urgency, str)
        and urgency.lower() in {"low", "medium", "high"}
    )


def validate_category(category):
    """Check whether the ticket category is valid."""

    return (
        isinstance(category, str)
        and category in {"Network", "Hardware", "Software", "Other"}
    )


def validate_affected_users(affected_users):
    """Check that affected_users is a positive integer."""

    return (
        isinstance(affected_users, int)
        and not isinstance(affected_users, bool)
        and affected_users > 0
    )


def create_ticket(ticket_id, title, category, urgency, affected_users):
    """Create a new ticket after validating its details."""

    if not validate_ticket_id(ticket_id):
        raise ValueError("Invalid ticket ID. Use the format T001.")

    if not validate_ticket(title):
        raise ValueError("Ticket title cannot be blank.")

    if not validate_category(category):
        raise ValueError("Invalid ticket category.")

    if not validate_urgency(urgency):
        raise ValueError("Invalid urgency level.")

    if not validate_affected_users(affected_users):
        raise ValueError("Affected users must be a positive integer.")

    return {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency.lower(),
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }


def generate_ticket_id(tickets):
    """Generate the next available ticket ID."""

    highest_id = 0

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if validate_ticket_id(ticket_id):
            highest_id = max(highest_id, int(ticket_id[1:]))

    return f"T{highest_id + 1:03d}"