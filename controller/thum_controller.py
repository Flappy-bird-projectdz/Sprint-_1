# thum_controller.py
import json
import os

USER_FILE = "users.json"

class AuthController:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except:
                self.users = []
        else:
            self.users = []

    def save_users(self):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)

    def xu_ly_dang_ky(self, username, password, email):
        # Kiểm tra username tồn tại
        if any(u["username"] == username for u in self.users):
            return "Tên đăng nhập đã tồn tại!"
        # Kiểm tra email tồn tại
        if any(u["email"] == email for u in self.users):
            return "Email đã tồn tại!"
        # Thêm user mới
        self.users.append({
            "username": username,
            "password": password,
            "email": email
        })
        self.save_users()
        return "Đăng ký thành công!"

    def xu_ly_dang_nhap(self, username, password):
        for u in self.users:
            if u["username"] == username and u["password"] == password:
                return u  # trả về dict user
        return None
