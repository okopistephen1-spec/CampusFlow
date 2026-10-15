import unittest

from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    get_work_queue,
    add_note,
    view_notes,
    search_tickets,
)


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
    assigned_to=None,
    title="Test ticket",
    category="Hardware",
):
    return {
        "id": ticket_id,
        "title": title,
        "category": category,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
        "notes": [],
    }


class TestWorkflow(unittest.TestCase):

    def test_assign_ticket(self):
        ticket = make_ticket()

        result = assign_ticket(ticket, "John")

        self.assertEqual(result["assigned_to"], "John")

    def test_assign_ticket_rejects_empty_name(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            assign_ticket(ticket, " ")

    def test_resolved_ticket_cannot_be_assigned(self):
        ticket = make_ticket(status="resolved")

        with self.assertRaises(ValueError):
            assign_ticket(ticket, "John")

        self.assertIsNone(ticket["assigned_to"])

    def test_update_ticket_status(self):
        ticket = make_ticket(assigned_to="John")

        result = update_ticket_status(ticket, "in_progress")

        self.assertEqual(result["status"], "in_progress")

    def test_unassigned_ticket_cannot_start_progress(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_ticket_status(ticket, "in_progress")

        self.assertEqual(ticket["status"], "open")

    def test_update_ticket_status_rejects_invalid_status(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_ticket_status(ticket, "sleeping")

        self.assertEqual(ticket["status"], "open")

    def test_work_queue_orders_by_priority(self):
        tickets = [
            make_ticket("T001", "low"),
            make_ticket("T002", "critical"),
            make_ticket("T003", "medium"),
            make_ticket("T004", "high"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T004", "T003", "T001"],
        )

    def test_work_queue_excludes_resolved_tickets(self):
        tickets = [
            make_ticket("T001", "critical", "resolved"),
            make_ticket("T002", "low", "open"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002"],
        )

    def test_work_queue_orders_same_priority_by_numeric_id(self):
        tickets = [
            make_ticket("T010", "high"),
            make_ticket("T002", "high"),
            make_ticket("T001", "high"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T010"],
        )

    def test_add_note(self):
        ticket = make_ticket()

        note = add_note(ticket, "John", "Restarted the router")

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "John")
        self.assertEqual(note["message"], "Restarted the router")
        self.assertEqual(len(ticket["notes"]), 1)

    def test_add_note_rejects_short_message(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            add_note(ticket, "John", "Hey")

        self.assertEqual(ticket["notes"], [])

    def test_resolved_ticket_cannot_receive_note(self):
        ticket = make_ticket(status="resolved")

        with self.assertRaises(ValueError):
            add_note(ticket, "John", "Ticket needs further attention")

        self.assertEqual(ticket["notes"], [])

    def test_view_notes_orders_by_note_id(self):
        ticket = make_ticket()
        ticket["notes"] = [
            {
                "note_id": "N002",
                "author": "Jane",
                "message": "Second note",
            },
            {
                "note_id": "N001",
                "author": "John",
                "message": "First note",
            },
        ]

        notes = view_notes(ticket)

        self.assertEqual(
            [note["note_id"] for note in notes],
            ["N001", "N002"],
        )

    def test_search_title_is_case_insensitive(self):
        tickets = [
            make_ticket(title="Network Connection Failed"),
            make_ticket("T002", title="Printer problem"),
        ]

        results = search_tickets(tickets, title="NETWORK")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001"],
        )

    def test_search_category_is_case_insensitive(self):
        tickets = [
            make_ticket(category="Hardware"),
            make_ticket("T002", category="Software"),
        ]

        results = search_tickets(tickets, category="hardware")

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001"],
        )


if __name__ == "__main__":
    unittest.main()