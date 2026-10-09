import unittest

from campusflow.tickets import (
    calculate_priority,
    validate_ticket,
    validate_urgency,
    validate_category,
    validate_affected_users,
    create_ticket,
    generate_ticket_id
    
)

class TestTickets(unittest.TestCase):

    def test_calculate_priority(self):
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 5), "high")
        self.assertEqual(calculate_priority("low", 10), "high")
        self.assertEqual(calculate_priority("medium", 2), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_validate_ticket(self):
        self.assertTrue(validate_ticket("Wi-Fi is down"))
        self.assertFalse(validate_ticket(""))
        self.assertFalse(validate_ticket("   "))

    def test_validate_urgency(self):
        self.assertTrue(validate_urgency("high"))
        self.assertTrue(validate_urgency("medium"))
        self.assertTrue(validate_urgency("low"))
        self.assertFalse(validate_urgency("urgent"))

    def test_validate_category(self):
        self.assertTrue(validate_category("Network"))
        self.assertTrue(validate_category("Hardware"))
        self.assertTrue(validate_category("Software"))
        self.assertTrue(validate_category("Other"))
        self.assertFalse(validate_category("Electricity"))

    def test_validate_affected_users(self):
        self.assertTrue(validate_affected_users(5))
        self.assertFalse(validate_affected_users(0))
        self.assertFalse(validate_affected_users(-2))
        self.assertFalse(validate_affected_users("5"))

    

    def test_create_ticket(self):
        ticket = create_ticket(
            "T001",
            "Campus Wi-Fi is down",
            "Network",
            "high",
            15
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_generate_ticket_id(self):
        tickets = [
            {"id": "T001"},
            {"id": "T002"},
            {"id": "T004"}
        ]


if __name__ == "__main__":
    unittest.main()