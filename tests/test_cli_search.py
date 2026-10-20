import unittest
from unittest import mock

import main


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


class TestSearchByTitleCli(unittest.TestCase):
    """Milestone B6: CLI filter choices tested without typing manually.

    main.py loads tickets.json at import time; these tests pass their own
    ticket list to the function, so no live data is touched.
    """

    def run_search(self, tickets, scripted_inputs):
        printed = []

        with mock.patch("builtins.input", side_effect=scripted_inputs), \
                mock.patch("builtins.print"):
            results = main.search_tickets_by_title(tickets)

        return results

    def test_invalid_category_reprompts_until_valid(self):
        tickets = [
            make_ticket(title="Campus Wi-Fi is down", category="Network"),
            make_ticket("T002", title="Wi-Fi slow in Lab 2", category="Network",
                        status="resolved"),
        ]

        results = self.run_search(tickets, [
            "wi-fi",        # title
            "Building",     # invalid category -> must re-prompt
            "network",      # valid category
            "open",         # status filter
            "",             # skip priority
            "n",            # no re-sort
        ])

        self.assertEqual([ticket["id"] for ticket in results], ["T001"])

    def test_invalid_status_reprompts_until_valid(self):
        tickets = [make_ticket(title="Laptop screen flickers")]

        results = self.run_search(tickets, [
            "",             # no title filter
            "",             # skip category
            "closed",       # invalid status -> re-prompt
            "open",         # valid status
            "",             # skip priority
            "n",
        ])

        self.assertEqual(len(results), 1)

    def test_skip_all_filters_returns_everything(self):
        tickets = [
            make_ticket(),
            make_ticket("T002", title="Wi-Fi trouble", category="Network"),
        ]

        results = self.run_search(tickets, ["", "", "", "", "n"])

        self.assertEqual(len(results), 2)

    def test_no_results_returns_empty_list(self):
        tickets = [make_ticket(title="Laptop screen flickers")]

        results = self.run_search(tickets, ["printer", "", "", "", "n"])

        self.assertEqual(results, [])

    def test_priority_sort_option_orders_results(self):
        tickets = [
            make_ticket("T010", title="Wi-Fi trouble", category="Network",
                        priority="high"),
            make_ticket("T002", title="Wi-Fi trouble", category="Network",
                        priority="high"),
            make_ticket("T003", title="Wi-Fi trouble", category="Network",
                        priority="critical"),
        ]

        results = self.run_search(tickets, [
            "wi-fi", "", "", "", "y",   # choose the priority-sorted view
        ])

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T003", "T002", "T010"],
        )


if __name__ == "__main__":
    unittest.main()
