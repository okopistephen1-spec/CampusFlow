def find_ticket(tickets, ticket_id):
    """
    Find a ticket in the list of tickets by its ID.

    Args:
        tickets (list): A list of ticket dictionaries.
        ticket_id (str): The ID of the ticket to find.

    Returns:
        dict or None: The ticket dictionary if found, otherwise None.
    """
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            return ticket
    raise ValueError(f"Ticket {ticket_id} was not found.")

def assign_ticket(tickets, ticket_id, staff_name):
    """
    Assign a ticket to a staff member.

    Args:
        tickets (list): A list of ticket dictionaries.
        ticket_id (str): The ID of the ticket to assign.
        staff_name (str): The name of the staff member to assign the ticket to.

    Returns:
        None
    """
    ticket = find_ticket(tickets, ticket_id)
    if ticket['status'] == 'open':
        ticket['assigned_to'] = staff_name
        ticket['status'] = 'in progress'
    else:
        raise ValueError(f"Ticket {ticket_id} is not open and cannot be assigned.")
    ticket['assigned_to'] = staff_name.strip()  # Ensure no leading/trailing whitespace in staff name   

    return ticket
