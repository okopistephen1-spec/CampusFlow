from campusflow.tickets import (
    create_ticket,
    generate_ticket_id,
    validate_category,
    validate_urgency,
    validate_affected_users
)

from campusflow.storage import load_tickets, save_tickets

tickets = load_tickets("tickets.json")

def create_new_ticket():
    while True:
        title = input("Enter ticket title: ").strip()

        if title:
            break

        print("Ticket title cannot be empty. Please try again.")

    while True:
        category = input(
            "Enter ticket category (Network/Hardware/Software/Other): "
        ).strip()

        if validate_category(category):
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

    ticket = create_ticket(
        ticket_id,
        title,
        category,
        urgency,
        affected_users
    )

    tickets.append(ticket)
    save_tickets(tickets, "tickets.json")

    print("\nTicket created successfully!")
    print(ticket)


def view_tickets(tickets):
    if not tickets:
        print("\nNo tickets found! You can add your new ticket")
        return

    print("\n=== ALL THE TICKETS IS BEING LISTED NOW ===")

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

# view_tickets(tickets)

def update_ticket_status(tickets):
    if not tickets:
        print("\nNo ticket found to update")
        return

    ticket_id = input("Enter the ticket ID you want to upadate: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print(f"\nCurrent status: {ticket['status']}")
            print("1. Open")
            print("2. In progress")
            print("3. Resolved")

            choice = input("Choose the new status of the issue: ").strip()

            if choice == "1":
                ticket["status"] = "open"
            
            elif choice == "2":
                ticket["status"] = "in_progress"

            elif choice == "3":
                ticket["status"] = "resolved"

            else:
                print("Invalid choice")
                return

            save_tickets(tickets, "tickets.json")
            print("Ticket status has been Successfully Updated🎉")

print("Ticket ID is not found or correct.")

def assign_ticket(tickets):
    if not tickets:
        print("\nNo tickets available to assign.")
        return

    ticket_id = input("Enter the ticket ID: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            name = input("Enter the team member's name: ").strip()

            if not name:
                print("Team members name cannot be empty")
                return

            ticket["assigned_to"] = name

            save_tickets(tickets, "tickets.json")

            print(f"Ticket {ticket_id} assigned to {name} successfully 🎉")
            return

    print("Ticket cannot be found!")

def search_ticket(tickets):
    if not tickets:
        print("\nNo tickets available to search.")
        return

    ticket_id = input("Enter the ticket ID to search for: ").strip()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print("\n===== TICKET FOUND =====")
            print(f"ID: {ticket['id']}")
            print(f"Title: {ticket['title']}")
            print(f"Category: {ticket['category']}")
            print(f"Urgency: {ticket['urgency']}")
            print(f"Affected Users: {ticket['affected_users']}")
            print(f"Priority: {ticket['priority']}")
            print(f"Status: {ticket['status']}")
            print(f"Assigned To: {ticket['assigned_to']}")
            return

    print("Ticket ID not found.")

while True:
    print("\n==== CAMPUS FLOW ====")
    print("1. Create a ticket")
    print("2. View all Tickets")
    print("3. Update ticket status")
    print("4. Assign ticket")
    print("5. Search ticket by ID")
    print("6. Exit")

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

    elif choice == "5":
        print("Thank you for using Learn2Earn Campus Flow")
        break
