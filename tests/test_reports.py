from campusflow.reports import generate_ticket_report


def make_ticket(
    ticket_id,
    priority="medium",
    status="open",
    assigned_to=None,
):
    """Create a sample ticket for testing."""
    return {
        "id": ticket_id,
        "title": "Test ticket",
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


def test_generate_ticket_report_counts_total_tickets():
    tickets = [
        make_ticket("T001"),
        make_ticket("T002"),
        make_ticket("T003"),
    ]

    report = generate_ticket_report(tickets)

    assert report["total"] == 3


def test_generate_ticket_report_counts_statuses():
    tickets = [
        make_ticket("T001", status="open"),
        make_ticket("T002", status="open"),
        make_ticket("T003", status="in_progress"),
        make_ticket("T004", status="resolved"),
    ]

    report = generate_ticket_report(tickets)

    assert report["open"] == 2
    assert report["in_progress"] == 1
    assert report["resolved"] == 1


def test_generate_ticket_report_counts_priorities():
    tickets = [
        make_ticket("T001", priority="critical"),
        make_ticket("T002", priority="critical"),
        make_ticket("T003", priority="high"),
        make_ticket("T004", priority="low"),
    ]

    report = generate_ticket_report(tickets)

    assert report["by_priority"] == {
        "critical": 2,
        "high": 1,
        "low": 1,
    }


def test_generate_ticket_report_counts_assignees():
    tickets = [
        make_ticket("T001", assigned_to="John"),
        make_ticket("T002", assigned_to="John"),
        make_ticket("T003", assigned_to="Mary"),
        make_ticket("T004", assigned_to=None),
    ]

    report = generate_ticket_report(tickets)

    assert report["by_assignee"] == {
        "John": 2,
        "Mary": 1,
        "Unassigned": 1,
    }


def test_generate_ticket_report_handles_empty_list():
    report = generate_ticket_report([])

    assert report == {
        "total": 0,
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "by_priority": {},
        "by_assignee": {},
    }


def test_generate_ticket_report_does_not_modify_tickets():
    tickets = [
        make_ticket("T001", priority="critical", assigned_to="John"),
        make_ticket("T002", priority="low"),
    ]

    original_tickets = [ticket.copy() for ticket in tickets]

    generate_ticket_report(tickets)

    assert tickets == original_tickets
    