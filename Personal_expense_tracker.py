import csv
from datetime import datetime

# Predefined list of categories
CATEGORIES = ['Food', 'Travel', 'Entertainment', 'Utilities', 'Healthcare', 'Other']

# Function to add an expense with multiple categories
def add_expense(expenses):
    # Function to validate date
    def validate_date(date_string, date_format='%Y-%m-%d'):
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            return False

    # Loop until a valid date is provided
    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        if validate_date(date):
            print(f"{date} is a valid date.")
            break
        else:
            print(f"{date} is not a valid date. Please enter a valid date in YYYY-MM-DD format.")

    # Display the category list and allow the user to select multiple categories
    print("Select one or more categories from the list (separate choices by commas):")
    for idx, category in enumerate(CATEGORIES, 1):
        print(f"{idx}. {category}")
    
    while True:
        try:
            category_choices = input("Enter the numbers corresponding to the categories (e.g., 1,3,5): ")
            selected_indexes = [int(choice.strip()) for choice in category_choices.split(',')]
            if all(1 <= index <= len(CATEGORIES) for index in selected_indexes):
                selected_categories = [CATEGORIES[index - 1] for index in selected_indexes]
                break
            else:
                print(f"Please enter valid numbers between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("Invalid input, please enter valid numbers separated by commas.")

    amount = float(input("Enter the amount spent: "))
    description = input("Enter a brief description: ")

    # Create the expense dictionary with multiple categories
    expense = {
        'date': date,
        'categories': ', '.join(selected_categories),  # Store categories as a comma-separated string
        'amount': amount,
        'description': description
    }

    # Append the expense to the list
    expenses.append(expense)
    print("Expense added successfully!")

# Function to view all expenses
def view_expenses(expenses):
    if not expenses:
        print("No expenses to display.")
        return

    for expense in expenses:
        if all(key in expense for key in ['date', 'categories', 'amount', 'description']):
            print(f"Date: {expense['date']}, Categories: {expense['categories']}, "
                  f"Amount: {expense['amount']}, Description: {expense['description']}")
        else:
            print("Incomplete expense entry found, skipping...")

# Function to set the monthly budget
def set_budget():
    budget = float(input("Enter your monthly budget: "))
    return budget

# Function to track the budget
def track_budget(expenses, budget):
    total_spent = sum(expense['amount'] for expense in expenses)
    print(f"Total spent so far: {total_spent}")

    if total_spent > budget:
        print("Warning: You have exceeded your budget!")
    else:
        print(f"You have {budget - total_spent} left for the month.")

# Function to save expenses to a CSV file
def save_expenses(expenses, filename='expenses.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'categories', 'amount', 'description'])
        writer.writeheader()
        writer.writerows(expenses)
    print("Expenses saved successfully!")

# Function to load expenses from a CSV file with backward compatibility
def load_expenses(filename='expenses.csv'):
    expenses = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if 'categories' exists in the row, if not, use an empty string as a fallback
                expense = {
                    'date': row['date'],
                    'categories': row.get('categories', ''),  # Use get() to avoid KeyError
                    'amount': float(row['amount']),
                    'description': row['description']
                }
                expenses.append(expense)
        print("Expenses loaded successfully!")
    except FileNotFoundError:
        print("No previous expenses found, starting fresh.")
    
    return expenses

# Function to display the interactive menu
def display_menu():
    print("\nPersonal Expense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Track Budget")
    print("4. Save Expenses")
    print("5. Exit")

# Main function to run the program
def main():
    expenses = load_expenses()  # Load expenses from file on start
    budget = 0  # Initialize budget

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            if budget == 0:
                budget = set_budget()
            track_budget(expenses, budget)
        elif choice == '4':
            save_expenses(expenses)
        elif choice == '5':
            save_expenses(expenses)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the main function
if __name__ == '__main__':
    main()
