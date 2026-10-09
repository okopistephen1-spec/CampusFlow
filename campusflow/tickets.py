def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    
    elif urgency == "high" or affected_users >= 10:
        return "high" 
    
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    
    else:
        return "low"


def validate_ticket(title):
    if not title.strip():
        return False
    
    return True

def validate_urgency(urgency):
    if urgency == "high":
        return True
    elif urgency == "medium":
        return True
    elif urgency == "low":
        return True
    else:
        return False

def validate_category(category):
    return category in ["Network", "Hardware", "Software", "Other"]

def validate_affected_users(affected_users):
    return (
        isinstance(affected_users, int) 
        and not isinstance(affected_users, bool)
        and affected_users > 0
    )


def create_ticket(ticket_id, title, category, urgency, affected_users):
    if not validate_ticket(title):
        raise ValueError("Title cannot be empty")

    if not validate_category(category):
        raise ValueError("Invalid category")

    if not validate_urgency(urgency):
        raise ValueError("Invalid urgency")

    if not validate_affected_users(affected_users):
        raise ValueError("Affected users must be a positive integer")

    priority = calculate_priority(urgency, affected_users)

    ticket = {
        "id": ticket_id,
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }

    return ticket

def generate_ticket_id(tickets):
    existing_ids = {
        ticket["id"]
        for ticket in tickets
        if isinstance(ticket.get("id"), str)
    }

    number = 1

    while f"T{number:03d}" in existing_ids:
        number += 1

    return f"T{number:03d}"

# number = 1
# ticket_id = f"T{number:03d}"

# title = input("Enter ticket title: ")

# while True:
#     try:
#         category = input("Enter ticket category(Network/Hardware/Software/Other): ")

#         if validate_category(category):
#             break
        
#         print("Invalid category.Please try again")

#     except ValueError:
#         print("Please enter the right category")

# while True:
#     urgency = input("Enter your urgency (low/medium/high): ").lower().strip()

#     if validate_urgency(urgency):
#         break

#     print("Invalid urgency. Please enter low, medium, or high")

# while True:
#     try:
#         affected_users = int(input("Enter the number of affected users: "))

#         if validate_affected_users(affected_users):
#             break

#         print("The number must be greater than zero.")

#     except ValueError:
#         print("Please enter a valid whole number.")

# ticket = create_ticket(
#     ticket_id,
#     title=title,
#     category=category,
#     urgency=urgency,
#     affected_users=affected_users
# )

# print(ticket)