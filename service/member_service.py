from .db_client import DBClient
from .auth_service import AuthService
from datetime import date

class MemberService:
    def __init__(self):
        self.db_client = DBClient()
        self.auth_service = AuthService("Members")

    def is_authorized(self) -> bool:
        return self.auth_service.me() != None

    def login(self, username: str, password: str) -> tuple[int, str]:
        return self.auth_service.login(username, password)

    def signup(self, username: str, password: str, confirm_password: str, first_name: str, last_name: str) -> tuple[int, str]:
        return self.auth_service.signup(username, password, confirm_password, first_name, last_name)
    
    def logout(self) -> tuple[int, str]:
        return self.auth_service.logout()
    
    def get_name(self) -> str:
        query = f"""SELECT first_name, last_name FROM Members
                    WHERE username='{self.auth_service.me()}';"""
        status_code, usernames = self.db_client.get(query)
        return f"{usernames[0][0]} {usernames[0][1]}"

    def add_health_metrics_report(self, weight: str, bmi: str, ffmi: str) -> tuple[int, str]:
        # Validate that the metrics provided are numeric
        if not weight.isnumeric() or not bmi.isnumeric() or not ffmi.isnumeric():
            return 400, "Weight, BMI, and FFMI must be numeric values"
        
        query = f"""INSERT INTO HealthMetrics
                       VALUES ('{self.auth_service.me()}', '{date.today()}', {weight}, {bmi}, {ffmi});
                       """
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            if response == "UniqueViolation":
                return 400, f"User already submitted a health metric report today"

        return 200, "Success"
    
    def add_routine(self, title: str, description: str, weekly_frequency: str) -> tuple[int, str]:
        # Validate that the metrics provided are numeric
        if not weekly_frequency.isnumeric():
            return 400, "Weekly frequnecy must be a numeric value"
        
        query = f"""INSERT INTO Routines
                       VALUES ('{self.auth_service.me()}', '{title}', '{description}', {weekly_frequency});
                       """
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            if response == "UniqueViolation":
                return 400, f"User already created a routine with that name"

        return 200, "Success"
    
    def add_personal_record(self, exercise: str, weight: str, reps: str) -> tuple[int, str]:
        # Validate that weight and reps are numeric values
        if not weight.isnumeric() or not reps.isnumeric():
            return 400, "Weight and reps must be numeric"
        
        query = f"""INSERT INTO PersonalRecords
                       VALUES ('{self.auth_service.me()}', '{date.today()}', '{exercise}', {weight}, {reps});
                       """
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            if response == "UniqueViolation":
                return 400, f"User already submitted a personal record for {exercise} today"

        return 200, "Success"
    
    def enroll_in_class(self, class_id: int) -> tuple[int, str]:
        if not self._validate_class_exists(class_id):
            return 400, f"Class does not exist"

        query = f"""INSERT INTO ClassRegistration
                    VALUES ({class_id}, '{self.auth_service.me()}');"""
        
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            if response == "UniqueViolation":
                return 400, f"User is already registered for this class"

        return 200, "Success"
    
    def drop_class(self, class_id: int) -> tuple[int, str]:
        if not self._validate_class_exists(class_id):
            return 400, f"Class does not exist"

        query = f"""SELECT * FROM ClassRegistration
                    WHERE class_id={class_id} AND username='{self.auth_service.me()}';"""
        status_code, response = self.db_client.get(query)

        if len(response) == 0:
            return 400, "You are not currently registered for this class"
    
        query = f"""DELETE FROM ClassRegistration
                    WHERE class_id={class_id} AND username='{self.auth_service.me()}';"""
        status_code, response = self.db_client.delete(query)

        return 200, "Success"
    
    def get_health_metric_logs(self) -> list[tuple]:
        query = f"""SELECT * FROM HealthMetrics
                    WHERE username='{self.auth_service.me()}'"""
        status_code, health_metric_logs = self.db_client.get(query)

        return health_metric_logs
    
    def get_routines(self) -> list[tuple]:
        query = f"""SELECT * FROM Routines
                    WHERE created_by='{self.auth_service.me()}'"""
        status_code, routines = self.db_client.get(query)

        return routines
    
    def get_personal_records(self) -> list[tuple]:
        query = f"""SELECT * FROM PersonalRecords
                    WHERE username='{self.auth_service.me()}'"""
        status_code, personal_records = self.db_client.get(query)

        return personal_records
    
    def get_all_classes(self) -> list[tuple]:
        query = f"""SELECT * FROM Classes;"""
        status_code, classes = self.db_client.get(query)    
        return classes
    
    def get_registered_classes(self) -> tuple[tuple]:
        query = f"""SELECT class_id FROM ClassRegistration
                    WHERE username='{self.auth_service.me()}';"""
        status_code, registered_class_ids = self.db_client.get(query)

        if len(registered_class_ids) == 0:
            return tuple()

        query = """SELECT * FROM Classes
                    WHERE class_id IN ({});""".format(','.join(str(tup[0]) for tup in registered_class_ids))
        status_code, classes = self.db_client.get(query)

        return classes
    
    def delete_routine(self, title) -> tuple[int, str]:
        query = f"""SELECT * FROM Routines
                    WHERE created_by='{self.auth_service.me()}' AND title='{title}';"""
        status_code, routines = self.db_client.get(query)
        if len(routines) == 0:
            return 400, f"No routine found with title {title}"
        
        query = f"""DELETE FROM Routines
                    WHERE created_by='{self.auth_service.me()}' AND title='{title}';"""
        
        return self.db_client.delete(query)
    
    def get_personal_trainers(self) -> list[str]:
        query = f"""SELECT trainer FROM PersonalTraining
                    WHERE client='{self.auth_service.me()}'"""
        status_code, trainers = self.db_client.get(query)

        return trainers
    
    def get_personal_training_session_logs(self) -> list[tuple]:
        query = f"""SELECT trainer, date, progress_notes FROM PersonalTrainingSession
                    WHERE client='{self.auth_service.me()}'"""
        status_code, sessions = self.db_client.get(query)

        return 200, sessions
    
    def get_outstanding_bills(self) -> list[tuple]:
        query = f"""SELECT date, amount, reason FROM Billing
                    WHERE client='{self.auth_service.me()}' AND paid={False};"""
        status_code, bills = self.db_client.get(query)

        return 200, bills
    
    def _validate_class_exists(self, class_id: str) -> bool:
        query = f"""SELECT * FROM Classes
                    WHERE class_id={class_id}"""
        status_code, classes = self.db_client.get(query)

        if len(classes) == 0:
            return False
        
        return True