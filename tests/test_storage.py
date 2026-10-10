import json
import tempfile
import unittest
from pathlib import Path

from campusflow.storage import save_tickets, load_tickets


class TestTicketStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.file_path = Path(self.temp_dir.name) / "tickets.json"

        self.tickets = [
            {
                "id": "T001",
                "title": "Campus Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 15,
                "priority": "critical",
                "status": "open",
                "assigned_to": None
            }
        ]

    def test_save_and_load_tickets(self):
        save_tickets(self.tickets, self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, self.tickets)

    def test_missing_file_returns_empty_list(self):
        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, [])

    def test_empty_ticket_list(self):
        save_tickets([], self.file_path)

        loaded_tickets = load_tickets(self.file_path)

        self.assertEqual(loaded_tickets, [])

    def test_malformed_json_raises_error(self):
        self.file_path.write_text(
            '{"id": "T001"',
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_non_list_json_raises_error(self):
        self.file_path.write_text(
            '{"id": "T001"}',
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)

    def test_non_object_ticket_raises_error(self):
        self.file_path.write_text(
            '[{"id": "T001"}, "invalid ticket"]',
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)


if __name__ == "__main__":
    unittest.main()