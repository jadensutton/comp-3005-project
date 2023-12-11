from .db_client import DBClient
from .auth_service import AuthService
from datetime import date

class StaffService:
    def __init__(self):
        self.db_client = DBClient()
        self.auth_service = AuthService("Staff")

    def is_authorized(self) -> bool:
        return self.auth_service.me() != None

    def login(self, username: str, password: str) -> tuple[int, str]:
        return self.auth_service.login(username, password)

    def signup(self, username: str, password: str, confirm_password: str, first_name: str, last_name: str) -> tuple[int, str]:
        return self.auth_service.signup(username, password, confirm_password, first_name, last_name)
    
    def logout(self) -> tuple[int, str]:
        return self.auth_service.logout()
    
    def get_name(self) -> str:
        query = f"""SELECT first_name, last_name FROM Staff
                    WHERE username='{self.auth_service.me()}';"""
        status_code, usernames = self.db_client.get(query)
        return f"{usernames[0][0]} {usernames[0][1]}"

    def create_class(self, title: str, description: str, schedule: str, capacity: str) -> tuple[int, str]:
        # Validate that the capacity provided is numeric
        if not capacity.isnumeric():
            return 400, "Capacity must be numeric"
        
        query = f"""INSERT INTO Classes (instructor, title, description, schedule, capacity)
                       VALUES ('{self.auth_service.me()}', '{title}', '{description}', '{schedule}', '{capacity}');
                       """
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            return 400, f"Unknown internal error"

        return 200, "Success"
    
    def add_personal_training_client(self, client: str) -> tuple[int, str]:
        query = f"""SELECT username FROM Members
                    WHERE username='{client}';"""
        status_code, response = self.db_client.get(query)

        if len(response) == 0:
            # Member does not exist
            return 400, "User does not exist."
        
        query = f"""INSERT INTO PersonalTraining
                    VALUES ('{self.auth_service.me()}', '{client}');"""
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            return 400, f"Unknown internal error"

        return 200, "Success"
        
    def log_personal_training_session(self, client: str, progress_notes: str) -> tuple[int, str]:
        query = f"""SELECT client FROM PersonalTraining
                    WHERE client='{client}' AND trainer='{self.auth_service.me()}';"""
        status_code, response = self.db_client.get(query)

        if len(response) == 0:
            # This staff memeber is not registered to train the client
            return 400, "You are not registered to train this client."
        
        query = f"""INSERT INTO PersonalTrainingSession
                    VALUES ('{self.auth_service.me()}', '{client}', '{date.today()}', '{progress_notes}');"""
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            return 400, f"Unknown internal error"

        return 200, "Success"
    
    def bill_client(self, client: str, amount: str, reason: str) -> tuple[int, str]:
        if not amount.isnumeric():
            return 400, "Amount must be numeric"
        
        query = f"""SELECT username FROM Members
                    WHERE username='{client}';"""
        status_code, response = self.db_client.get(query)

        if len(response) == 0:
            # Member does not exist
            return 400, "User does not exist."
        
        query = f"""INSERT INTO Billing (client, date, amount, reason, paid)
                    VALUES ('{client}', '{date.today()}', {amount}, '{reason}', {False});"""
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            return 400, f"Unknown internal error"

        return 200, "Success"