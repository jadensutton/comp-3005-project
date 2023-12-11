from service.member_service import MemberService

def login_or_signup():
    menu = """Health and Fitness Club Management System

            Please login or sign up
            [1] Login
            [2] Sign up

            """
    valid_options = {'1', '2'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        status_code, response = member_service.login(username, password)
        if status_code == 200:
            print(f"Welcome, {member_service.get_name()}\n")
        else:
            print(f"Error logging in: {response}\n")
    elif user_input == '2':
        username = input("Please enter your username: ")
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        password = input("Please enter your password: ")
        confirm_password = input("Please confirm your password: ")
        status_code, response = member_service.signup(username, password, confirm_password, first_name, last_name)
        if status_code == 200:
            print(f"You have successfully registered. Welcome, {member_service.get_name()}\n")
        else:
            print(f"Error signing up: {response}\n")
    else:
        print("Invalid input!\n")

def dashboard():
    menu = """Health and Fitness Club Management System
            Member Dashboard

            Please select a portal
            [1] Health Metrics
            [2] Routines
            [3] Personal Records
            [4] Classes
            [5] Personal Training
            [6] Billing
            [7] Log out

            """
    valid_options = {'1', '2', '3', '4', '5', '6', '7'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        health_metrics_portal()
    elif user_input == '2':
        routines_portal()
    elif user_input == '3':
        personal_records_portal()
    elif user_input == '4':
        classes_portal()
    elif user_input == '5':
        personal_training_portal()
    elif user_input == '6':
        billing_portal()
    elif user_input == '7':
        status_code, response = member_service.logout()
        if status_code == 200:
            print("Successfully logged out. Bye for now!\n")
        else:
            print(f"Error logging out: {response}\n")

def health_metrics_portal():
    menu ="""Health Metrics Portal

        Please select an option
        [1] View Health Metrics Logs
        [2] New Health Metrics Log
        [3] Back

        """
    valid_options = {'1', '2', '3'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        health_metrics_logs = member_service.get_health_metric_logs()
        if len(health_metrics_logs) == 0:
            print("You currently have no saved health metrics logs.\n")
            return
        
        print("Health metrics logs:")
        for _, date, weight, bmi, ffmi in health_metrics_logs:
            print(f"Date: {date} - Weight: {weight} lbs - BMI: {bmi} - FFMI: {ffmi}")

    elif user_input == '2':
        weight = input("Enter weight (lbs): ")
        bmi = input("Enter BMI: ")
        ffmi = input("Enter FFMI: ")
        status_code, response = member_service.add_health_metrics_report(weight, bmi, ffmi)
        if status_code == 200:
            print("Health metrics log saved successfully\n")
        else:
            print(f"Error saving health metrics log: {response}\n")

    elif user_input == '3':
        pass

def routines_portal():
    menu = """Routines Portal

        Please select an option
        [1] View Routines
        [2] New Routine
        [3] Delete Routine
        [4] Back

        """
    
    valid_options = {'1', '2', '3', '4'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        routines = member_service.get_routines()
        if len(routines) == 0:
            print("You have not created any routines\n")
            return
        
        print("Routines:")
        for _, title, description, weekly_frequency in routines:
            print(f"Title: {title}\nDescription: {description}\nFrequency: {weekly_frequency}x/week\n")

    elif user_input == '2':
        title = input("Enter routine title: ")
        description = input("Enter routine description: ")
        weekly_frequency = input("Enter weekly frequency: ")
        status_code, response = member_service.add_routine(title, description, weekly_frequency)
        if status_code == 200:
            print("Routine saved successfully\n")
        else:
            print(f"Error saving routine: {response}\n")
    
    elif user_input == '3':
        title = input("Enter title of routine to delete: ")
        status_code, response = member_service.delete_routine(title)
        if status_code == 200:
            print("Routine deleted successfully\n")
        else:
            print(f"Error deleting routine: {response}\n")

    elif user_input == '4':
        pass

def personal_records_portal():
    menu ="""Personal Records Portal

        Please select an option
        [1] View Personal Records
        [2] Log New Personal Record
        [3] Back

        """
    valid_options = {'1', '2', '3'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        personal_records = member_service.get_personal_records()
        if len(personal_records) == 0:
            print("You currently have no saved personal records.\n")
            return
        
        print("Personal records:")
        for _, date, exercise, weight, reps in personal_records:
            print(f"Date: {date} - Exercise: {exercise} - Weight: {weight} lbs - Reps: {reps}")

    elif user_input == '2':
        exercise = input("Enter exercise: ")
        weight = input("Enter weight (lbs): ")
        reps = input("Enter number of repititions: ")
        status_code, response = member_service.add_personal_record(exercise, weight, reps)
        if status_code == 200:
            print("Personal record saved successfully\n")
        else:
            print(f"Error saving personal record: {response}\n")

    elif user_input == '3':
        pass

def classes_portal():
    menu = """Classes Portal

        Please select an option
        [1] View all Classes
        [2] View my Classes
        [3] Enroll in Class
        [4] Drop Class
        [5] Back

        """
    
    valid_options = {'1', '2', '3', '4', '5'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        classes = member_service.get_all_classes()
        if len(classes) == 0:
            print("There are currently no classes available\n")
            return
        
        print("Classes:")
        for id, instructor, title, description, schedule, capacity in classes:
            print(f"ID: {id}\nTitle: {title}\nInstructor: {instructor}\nDescription: {description}\nSchedule: {schedule}\nCapacity: {capacity}\n")
    
    elif user_input == '2':
        classes = member_service.get_registered_classes()
        if len(classes) == 0:
            print("You are not currently registered in any classes\n")
            return
        
        print("Your classes:")
        for id, instructor, title, description, schedule, capacity in classes:
            print(f"ID: {id}\nTitle: {title}\nInstructor: {instructor}\nDescription: {description}\nSchedule: {schedule}\nCapacity: {capacity}\n")
    
    elif user_input == '3':
        id = input("Enter class ID: ")
        status_code, response = member_service.enroll_in_class(id)
        if status_code == 200:
            print("Successfully enrolled in class\n")
        else:
            print(f"Error enrolling in class: {response}\n")
    
    elif user_input == '4':
        id = input("Enter ID of class to drop: ")
        status_code, response = member_service.drop_class(id)
        if status_code == 200:
            print("Class successfully dropped\n")
        else:
            print(f"Error dropping class: {response}\n")

    elif user_input == '5':
        pass

def personal_training_portal():
    menu = """Personal Training Portal

        Please select an option
        [1] My personal trainers
        [2] View session logs
        [3] Back

        """
    
    valid_options = {'1', '2', '3'}
    user_input = prompt_user(menu, valid_options)

    if user_input == '1':
        trainers = member_service.get_personal_trainers()
        if len(trainers) == 0:
            print("You do not have any trainers\n")
            return
        
        print("Trainers: {}".format(','.join([tup[0] for tup in trainers])))

    elif user_input == '2':
        status_code, logs = member_service.get_personal_training_session_logs()
        if len(logs) == 0:
            print("No trainers have provided you any feedback yet\n")

        print("Logs:")
        for trainer, date, progress_notes in logs:
            print(f"Trainer: {trainer}\nDate: {date}\nProgress notes: {progress_notes}\n")

    elif user_input == '3':
        pass

def billing_portal():
    status, bills = member_service.get_outstanding_bills()
    if len(bills) == 0:
        print("You have no outstanding bills\n")

    total_bill = 0
    print("Bills: ")
    for date, amount, reason in bills:
        print(f"Date: {date}\nAmount: ${amount}\nReason: {reason}\n")
        total_bill += amount

    print(f"You owe ${total_bill} in total\n")

def prompt_user(menu: str, valid_options: set[str]) -> str:
    print(menu)
    while 1:
        user_input = input(">>> ")
        if user_input in valid_options:
            return user_input
        
        print("Invalid input!\n")

if __name__ == "__main__":
    member_service = MemberService()
    while 1:
        if member_service.is_authorized():
            dashboard()
        else:
            login_or_signup()