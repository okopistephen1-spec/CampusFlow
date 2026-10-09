from campusflow.tickets import (
    create_ticket,
    generate_ticket_id,
    validate_category,
    validate_urgency,
    validate_affected_users
)

from campusflow.storage import load_tickets, save_tickets

tickets = load_tickets("tickets.json")

while True:
    title = input("Enter ticket title: ").strip()

    if title:
        break

    print("Ticket title cannot be empty. Please try again")

while True:
    category = input(
        "Enter ticket category (Network/Hardware/Software/Other): "
    ).strip()

    if validate_category(category):
        break

    print("Invalid category. Please try again.")

while True:
    urgency = input(
        "Enter it's urgency (low/medium/high):"
    ).strip().lower()

    if validate_urgency(urgency):
        break

    print("Invalid urgency. Enter either low, medium or high.")

while True:
    try:
        affected_users = int(
            input("Enter the amount of users affected: ")
        )

        if validate_affected_users(affected_users):
            break

        print("The number must be correct and not zero!")

    except ValueError:
        print("Please enter a valid number!")

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
