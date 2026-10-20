import copy
import unittest

from campusflow.workflow import search_tickets, sort_results_by_priority


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


class TestSearchFilters(unittest.TestCase):
    """Acceptance case 09: combined search filters use logical AND."""

    def setUp(self):
        self.tickets = [
            make_ticket(title="Campus Wi-Fi is down", category="Network",
                        priority="critical"),
            make_ticket("T002", title="Wi-Fi slow in Lab 2", category="Network",
                        status="resolved", priority="high"),
            make_ticket("T003", title="Wi-Fi rebooted, still weak",
                        category="Software", priority="high"),
            make_ticket("T004", title="Laptop will not boot",
                        category="Hardware", priority="low"),
        ]

    def test_combined_filters_use_and(self):
        results = search_tickets(
            self.tickets,
            title="wi-fi",
            category="Network",
            status="open",
        )

        self.assertEqual([ticket["id"] for ticket in results], ["T001"])

    def test_all_filters_supplied_must_all_match(self):
        results = search_tickets(
            self.tickets,
            title="wi-fi",
            category="Network",
            status="open",
            priority="critical",
        )

        self.assertEqual([ticket["id"] for ticket in results], ["T001"])

    def test_one_matching_filter_alone_is_not_enough(self):
        # T002 matches title + category but NOT status, so AND excludes it.
        results = search_tickets(
            self.tickets,
            title="wi-fi",
            category="Network",
            status="open",
        )

        self.assertNotIn("T002", [ticket["id"] for ticket in results])

    def test_empty_filters_do_not_filter(self):
        results = search_tickets(self.tickets, category="", status="", priority="")

        self.assertEqual(len(results), 4)


class TestSearchIsReadOnly(unittest.TestCase):
    """Requirement C: search must not modify ticket records."""

    def test_search_does_not_modify_tickets(self):
        tickets = [
            make_ticket(title="Campus Wi-Fi is down", category="Network"),
            make_ticket("T002", title="Wi-Fi slow in Lab 2", status="resolved"),
        ]
        before = copy.deepcopy(tickets)

        search_tickets(tickets, title="wi-fi", category="Network",
                       status="open", priority="high")

        self.assertEqual(tickets, before)


class TestSearchCaseFolding(unittest.TestCase):
    """Acceptance case 08: title search ignores case (casefold)."""

    def test_title_search_ignores_case(self):
        tickets = [make_ticket(title="Campus Wi-Fi is down")]

        for query in ("wi-fi", "WI-FI", "Wi-Fi", "campus wifi is down".replace("wifi", "wi-fi")):
            with self.subTest(query=query):
                results = search_tickets(tickets, title=query)
                self.assertEqual(len(results), 1)

    def test_title_search_matches_substring(self):
        tickets = [make_ticket(title="Network printer offline in Lab 3")]

        results = search_tickets(tickets, title="printer")

        self.assertEqual(len(results), 1)


class TestPrioritySortedResults(unittest.TestCase):
    """Requirement D: search results sorted by priority then numeric ticket ID."""

    def test_sorts_critical_before_high_before_low(self):
        tickets = [
            make_ticket("T003", priority="low"),
            make_ticket("T002", priority="high"),
            make_ticket("T001", priority="critical"),
        ]

        results = sort_results_by_priority(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T001", "T002", "T003"],
        )

    def test_numeric_id_breaks_ties_not_text_order(self):
        # Text sorting would put T010 before T002; numeric ordering must not.
        tickets = [
            make_ticket("T010", priority="high"),
            make_ticket("T002", priority="high"),
        ]

        results = sort_results_by_priority(tickets)

        self.assertEqual([ticket["id"] for ticket in results], ["T002", "T010"])

    def test_sort_returns_new_list(self):
        tickets = [make_ticket("T002"), make_ticket("T001")]

        results = sort_results_by_priority(tickets)

        self.assertIsNot(results, tickets)
        self.assertEqual(tickets[0]["id"], "T002")  # original untouched


if __name__ == "__main__":
    unittest.main()
