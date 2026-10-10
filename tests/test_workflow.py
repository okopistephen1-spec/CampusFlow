import pytest

from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    get_work_queue,
)


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": "Test ticket",
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


def test_assign_ticket():
    ticket = make_ticket()

    result = assign_ticket(ticket, "John")

    assert result["assigned_to"] == "John"


def test_assign_ticket_rejects_empty_name():
    ticket = make_ticket()

    with pytest.raises(ValueError):
        assign_ticket(ticket, " ")


def test_update_ticket_status():
    ticket = make_ticket(assigned_to="John")

    result = update_ticket_status(ticket, "in_progress")

    assert result["status"] == "in_progress"


def test_update_ticket_status_rejects_invalid_status():
    ticket = make_ticket()

    with pytest.raises(ValueError):
        update_ticket_status(ticket, "sleeping")


def test_work_queue_orders_by_priority():
    tickets = [
        make_ticket("T001", "low"),
        make_ticket("T002", "critical"),
        make_ticket("T003", "medium"),
    ]

    queue = get_work_queue(tickets)

    assert [ticket["id"] for ticket in queue] == [
        "T002",
        "T003",
        "T001",
    ]


def test_work_queue_excludes_resolved_tickets():
    tickets = [
        make_ticket("T001", "critical", "resolved"),
        make_ticket("T002", "low", "open"),
    ]

    queue = get_work_queue(tickets)

    assert [ticket["id"] for ticket in queue] == ["T002"]

