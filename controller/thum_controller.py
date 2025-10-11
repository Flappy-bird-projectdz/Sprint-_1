import json, os, re
from entities import User

class AuthController:
    USERS_FILE = "users.json"

    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.USERS_FILE):
            with open(self.USERS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.USERS_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def xu_ly_dang_ky(self, username, password, email):
        if username in self.users:
            return "Tên tài khoản đã tồn tại!"
        if not username or not password or not email:
            return "Không được để trống!"
        if not self.is_valid_email(email):
            return "Email không hợp lệ!"
        self.users[username] = {"password": password, "email": email}
        self.save_users()
        return "Đăng ký thành công!"

    def xu_ly_dang_nhap(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            user_data = self.users[username]
            return User(username, password, user_data.get("email", ""))
        return None
