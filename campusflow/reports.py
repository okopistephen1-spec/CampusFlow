def generate_ticket_report(tickets):
    """Generate a summary of ticket counts."""
    report = {
        "total": len(tickets),
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "by_priority": {},
        "by_assignee": {},
    }

    for ticket in tickets:
        status = ticket.get("status")

        if status in {"open", "in_progress", "resolved"}:
            report[status] += 1

        priority = ticket.get("priority", "unknown")
        report["by_priority"][priority] = (
            report["by_priority"].get(priority, 0) + 1
        )

        assignee = ticket.get("assigned_to") or "Unassigned"
        report["by_assignee"][assignee] = (
            report["by_assignee"].get(assignee, 0) + 1
        )

    return report
