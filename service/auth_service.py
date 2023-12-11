from .db_client import DBClient

class AuthService:
    def __init__(self, table: str):
        self._table = table
        self._username = None
        self.db_client = DBClient()

    def me(self) -> str:
        return self._username

    def login(self, username: str, password: str) -> tuple[int, str]:
        query = f"""SELECT username FROM {self._table}
                       WHERE username='{username}' AND password='{password}';
                       """
        
        status_code, members = self.db_client.get(query)

        if status_code != 200:
            return status_code, "Unknown internal error"

        if len(members) == 0:
            # User does not exist in DB
            return 400, "No member account was found with that username and password combination"
        elif len(members) > 1:
            # More than one member found in DB
            return 400, "Unknown internal error"

        self._username = members[0][0]

        return 200, "Success"

    def signup(self, username: str, password: str, confirm_password: str, first_name: str, last_name: str) -> tuple[int, str]:
        # Validate that password matches confirm password
        if password != confirm_password:
            return 400, "Confirm password does not match password"
        
        query = f"""INSERT INTO {self._table}
                    VALUES ('{username}', '{first_name}', '{last_name}', '{password}');"""
        status_code, response = self.db_client.insert(query)
        
        # Validate that insert was successful
        if status_code != 200:
            if response == "UniqueViolation":
                return 400, f"User already exists with username {username}"

        self._username = username

        return 200, "Success"
    
    def logout(self) -> tuple[int, str]:
        if self._username != None:
            self._username = None
            return 200, "Logged out successfully"
        
        return 400, "Not currently logged in"