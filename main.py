from campusflow.tickets import (
    create_ticket,
    generate_ticket_id,
    validate_category,
    validate_urgency,
    validate_affected_users,
)

from campusflow.workflow import (
    find_ticket,
    search_tickets,
    sort_results_by_priority,
    get_work_queue,
    assign_ticket as assign_ticket_record,
    update_ticket_status as apply_status_change,
    add_note,
    view_notes,
)

from campusflow.understanding_check import run_understanding_check

from campusflow.storage import load_tickets, save_tickets


# Load saved tickets when the application starts.
tickets = load_tickets("tickets.json")


def create_new_ticket():
    """Collect information and create a new ticket."""

    while True:
        title = input("Enter ticket title: ").strip()

        if title:
            break

        print("Ticket title cannot be empty. Please try again.")

    while True:
        category = input(
            "Enter ticket category (Network/Hardware/Software/Other): "
        ).strip()

        validate_categories = {
            "network": "Network",
            "hardware": "Hardware",
            "software": "Software",
            "other": "Other",
        }

        category = validate_categories.get(category.casefold())

        if category:
            break
        
        print("Invalid category. Please try again.")

    while True:
        urgency = input(
            "Enter its urgency (low/medium/high): "
        ).strip().lower()

        if validate_urgency(urgency):
            break

        print("Invalid urgency. Enter low, medium, or high.")

    while True:
        try:
            affected_users = int(
                input("Enter the number of users affected: ")
            )

            if validate_affected_users(affected_users):
                break

            print("The number of users must be greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")

    ticket_id = generate_ticket_id(tickets)

    if any(ticket["id"] == ticket_id for ticket in tickets):
        print("Error: This ticket ID already exists.")
        return

    try:
        ticket = create_ticket(
            ticket_id,
            title,
            category,
            urgency,
            affected_users,
        )

        tickets.append(ticket)
        save_tickets(tickets, "tickets.json")

    except (ValueError, OSError) as error:
        # Remove the ticket if saving fails after it was appended.
        if "ticket" in locals() and ticket in tickets:
            tickets.remove(ticket)

        print(f"Could not create ticket: {error}")
        return

    print("\nTicket created successfully!")
    print(ticket)


def view_tickets(tickets):
    """Display all tickets."""

    if not tickets:
        print("\nNo tickets found. You can create a new ticket.")
        return

    print("\n=== ALL TICKETS ===")

    for ticket in tickets:
        print("------------------------")
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Urgency: {ticket['urgency']}")
        print(f"Affected Users: {ticket['affected_users']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned To: {ticket['assigned_to']}")


def update_ticket_status(tickets):
    """Allow the user to update a ticket's status."""

    if not tickets:
        print("\nNo tickets available to update.")
        return

    ticket_id = input(
        "Enter the ticket ID you want to update: "
    ).strip()

    ticket = next(
        (item for item in tickets if item["id"] == ticket_id),
        None,
    )

    if ticket is None:
        print("Ticket ID not found.")
        return

    print(f"\nCurrent status: {ticket['status']}")
    print("1. Open")
    print("2. In progress")
    print("3. Resolved")

    choice = input("Choose the new status: ").strip()

    statuses = {
        "1": "open",
        "2": "in_progress",
        "3": "resolved",
    }

    if choice not in statuses:
        print("Invalid choice.")
        return

    old_status = ticket["status"]

    try:
        apply_status_change(ticket, statuses[choice])
        save_tickets(tickets, "tickets.json")

    except (ValueError, OSError) as error:
        # Restore the previous status if the operation fails.
        ticket["status"] = old_status
        print(f"Could not update the ticket: {error}")
        return

    print("Ticket status updated successfully!")


def assign_ticket(tickets):
    """Assign a ticket to a staff member."""

    if not tickets:
        print("\nNo tickets available to assign.")
        return

    ticket_id = input("Enter the ticket ID: ").strip()

    ticket = next(
        (item for item in tickets if item["id"] == ticket_id),
        None,
    )

    if ticket is None:
        print("Ticket ID not found.")
        return

    staff_name = input(
        "Enter the staff member's name: "
    ).strip()

    old_assignee = ticket.get("assigned_to")

    try:
        assign_ticket_record(ticket, staff_name)
        save_tickets(tickets, "tickets.json")

    except (ValueError, OSError) as error:
        # Restore the previous assignment if saving fails.
        ticket["assigned_to"] = old_assignee
        print(f"Could not assign ticket: {error}")
        return

    print(f"Ticket {ticket_id} assigned to {staff_name}.")


def search_ticket(tickets):
    """Search for a ticket using its ID."""

    if not tickets:
        print("\nNo tickets available to search.")
        return

    ticket_id = input("Enter the ticket ID you want to find: ").strip()

    try:
        ticket = find_ticket(tickets, ticket_id)

        print("\n===== TICKET FOUND =====")
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Urgency: {ticket['urgency']}")
        print(f"Affected Users: {ticket['affected_users']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned To: {ticket['assigned_to']}")

    except ValueError as error:
        print(error)

def search_tickets_by_title(tickets):
    title = input("Enter the title of the ticket: ").strip()

    category = input(
        "enter the category either(Network/Hardware/Software/Other)"
    ).strip()

    valid_categories = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
    }

    if category:
        category = valid_categories.get(category.casefold())

        if category is None:
            print("Invalid category. Please try again")
            return

    status = input(
        "enter status(open/in_progress/resolved), "
        "or press Enter to skip"
    ).strip().lower()

    if status and status not in {"open", "in_progress", "resolved"}:
        print("Invalid status")
        return

    priority = input(
        "enter priority (critical/high/medium/low), "
        "or press Enter to skip"
    ).strip().lower()

    if priority and priority not in {"critical", "high", "medium", "low"}:
        print("Wrong priority")
        return

    results = search_tickets(
        tickets,
        title=title,
        category=category,
        status=status,
        priority=priority,
    )

    if not results:
        print("No result matched the ticket")
        return

    print(f"\nFound {len(results)} matching ticket(s):")

    for ticket in results:
        print("-" * 35)
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket['assigned_to']}")

    


def add_ticket_note(tickets):
    """Add a note to an existing ticket."""

    if not tickets:
        print("\nNo tickets available.")
        return

    ticket_id = input("Enter the ticket ID: ").strip()

    ticket = next(
        (item for item in tickets if item["id"] == ticket_id),
        None,
    )

    if ticket is None:
        print("Ticket ID not found.")
        return

    author = input("Enter your name: ").strip()
    message = input("Enter your desired message: ").strip()

    # Support older saved tickets that do not have a notes field.
    ticket.setdefault("notes", [])

    try:
        note = add_note(ticket, author, message)

    except ValueError as error:
        print(f"Could not add note: {error}")
        return

    try:
        save_tickets(tickets, "tickets.json")

    except OSError as error:
        # Undo the note addition if saving fails.
        ticket["notes"].remove(note)
        print(f"Could not save the note: {error}")
        return

    print("\nNote added successfully!")
    print(f"Note ID: {note['note_id']}")


def view_ticket_notes(tickets):
    """Find a ticket and display its notes."""

    if not tickets:
        print("\nNo tickets available.")
        return

    ticket_id = input("Enter the ticket ID: ").strip()

    ticket = next(
        (item for item in tickets if item["id"] == ticket_id),
        None,
    )

    if ticket is None:
        print("Ticket ID not found.")
        return

    try:
        notes = view_notes(ticket)

    except ValueError as error:
        print(f"Could not display notes: {error}")
        return

    if not notes:
        print(f"\nTicket {ticket_id} has no notes.")
        return

    print(f"\n=== NOTES FOR TICKET {ticket_id} ===")

    for note in notes:
        print("------------------------------")
        print(f"Note ID: {note['note_id']}")
        print(f"Author: {note['author']}")
        print(f"Message: {note['message']}")


def main():
    """Run the CampusFlow command-line application."""

    while True:
        print("\n==== CAMPUS FLOW ====")
        print("1. Create a ticket")
        print("2. View Tickets")
        print("3. Update ticket status")
        print("4. Assign ticket")
        print("5. Search ticket by ID")
        print("6. Add a note")
        print("7. View ticket notes")
        print("8. Search ticket by title")
        print("9. Engineering understanding Check")
        print("10. Exit")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            create_new_ticket()

        elif choice == "2":
            view_tickets(tickets)

        elif choice == "3":
            update_ticket_status(tickets)

        elif choice == "4":
            assign_ticket(tickets)

        elif choice == "5":
            search_ticket(tickets)

        elif choice == "6":
            add_ticket_note(tickets)

        elif choice == "7":
            view_ticket_notes(tickets)

        elif choice == "8":
            search_tickets_by_title(tickets)

        elif choice == "9":
            run_understanding_check()

        elif choice == "10":
            print("Thank you for using Learn2Earn CampusFlow!")
            break

        else:
            print("Invalid choice. Please select an option from 1 to 8.")


if __name__ == "__main__":
    main()