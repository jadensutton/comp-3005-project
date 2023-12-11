from service.staff_service import StaffService

def login_or_signup():
    menu = """Health and Fitness Club Management System
            Staff Portal

            Please login or sign up
            [1] Login
            [2] Sign up

            """
    valid_options = {'1', '2'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        status_code, response = staff_service.login(username, password)
        if status_code == 200:
            print(f"Welcome, {staff_service.get_name()}\n")
        else:
            print(f"Error logging in: {response}\n")
    elif user_input == '2':
        username = input("Please enter your username: ")
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        password = input("Please enter your password: ")
        confirm_password = input("Please confirm your password: ")
        status_code, response = staff_service.signup(username, password, confirm_password, first_name, last_name)
        if status_code == 200:
            print(f"You have successfully registered. Welcome, {staff_service.get_name()}\n")
        else:
            print(f"Error signing up: {response}\n")
    else:
        print("Invalid input!\n")

def dashboard():
    menu = """Health and Fitness Club Management System
            Staff Dashboard

            Please select a portal
            [1] Create Class
            [2] Add Personal Training Client
            [3] Log Personal Training Session
            [4] Bill Client
            [5] Log out

            """
    valid_options = {'1', '2', '3', '4', '5'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        title = input("Enter class title: ")
        description = input("Enter class description: ")
        schedule = input("Enter class schedule: ")
        capacity = input("Enter class capacity: ")

        status_code, response = staff_service.create_class(title, description, schedule, capacity)
        if status_code == 200:
            print("Successfully created class.\n")
        else:
            print(f"Error creating class: {response}\n")
    
    elif user_input == '2':
        client = input("Enter client username: ")

        status_code, response = staff_service.add_personal_training_client(client)
        if status_code == 200:
            print(f"Successfully added {client} as a personal training client\n")
        else:
            print(f"Error adding personal training client: {response}\n")

    elif user_input == '3':
        client = input("Enter client username: ")
        progress_notes = input("Enter progress notes: ")

        status_code, response = staff_service.log_personal_training_session(client, progress_notes)
        if status_code == 200:
            print(f"Successfully logged personal training session\n")
        else:
            print(f"Error logging personal training session: {response}\n")

    elif user_input == '4':
        client = input("Enter client to bill: ")
        amount = input("Enter $ amount: ")
        reason = input("Reason for billing: ")

        status_code, response = staff_service.bill_client(client, amount, reason)
        if status_code == 200:
            print("Successfully billed client\n")
        else:
            print(f"Error billing client: {response}\n")

    elif user_input == '5':
        status_code, response = staff_service.logout()
        if status_code == 200:
            print("Successfully logged out. Bye for now!\n")
        else:
            print(f"Error logging out: {response}\n")

def prompt_user(menu: str, valid_options: set[str]) -> str:
    print(menu)
    while 1:
        user_input = input(">>> ")
        if user_input in valid_options:
            return user_input
        
        print("Invalid input!\n")

if __name__ == "__main__":
    staff_service = StaffService()
    while 1:
        if staff_service.is_authorized():
            dashboard()
        else:
            login_or_signup()