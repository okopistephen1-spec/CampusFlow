def generate_ticket_report(tickets):
    """Generate a summary of ticket counts and statistics."""

    report = {
        "total": len(tickets),
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "unresolved": 0,
        "resolution_percentage": 0,
        "by_priority": {},
        "by_category": {},
        "by_assignee": {},
    }

    for ticket in tickets:
        # Count tickets by their current status
        status = ticket.get("status")

        if status in {"open", "in_progress", "resolved"}:
            report[status] += 1

        # Count tickets by priority
        priority = ticket.get("priority", "unknown")

        report["by_priority"][priority] = (
            report["by_priority"].get(priority, 0) + 1
        )

        # Count tickets by category
        category = ticket.get("category", "unknown")

        report["by_category"][category] = (
            report["by_category"].get(category, 0) + 1
        )

        # Count tickets by assignee
        assignee = ticket.get("assigned_to") or "Unassigned"

        report["by_assignee"][assignee] = (
            report["by_assignee"].get(assignee, 0) + 1
        )

    # Calculate unresolved tickets
    report["unresolved"] = (
        report["open"] + report["in_progress"]
    )

    # Calculate resolution percentage safely
    if report["total"] > 0:
        report["resolution_percentage"] = (
            report["resolved"] / report["total"]
        ) * 100

    return report