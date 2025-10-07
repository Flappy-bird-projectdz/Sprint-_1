import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess, os, json
from utilis import load_scores

USERS_FILE = "users.json"
CONFIG_FILE = "config.json"

# ==== Xử lý tài khoản ====
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ==== Lưu config màu Bird ====
def save_config(bird_color=None, username=None):
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
        except:
            pass
    if bird_color:
        cfg["bird_color"] = bird_color
    if username:
        cfg["username"] = username
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f)

# ==== Chọn màu chim và vào game ====
def choose_color():
    color_win = tk.Toplevel(root)
    color_win.title("Chọn màu Bird")
    color_win.geometry("300x200")

    tk.Label(color_win, text="Chọn màu cho Bird", font=("Arial", 14, "bold")).pack(pady=10)

    def select_color(color):
        save_config(bird_color=color)
        color_win.destroy()
        root.destroy()
        subprocess.run(["python", "flappy.py"])

    tk.Button(color_win, text="Red", width=10, command=lambda: select_color("red")).pack(pady=5)
    tk.Button(color_win, text="Blue", width=10, command=lambda: select_color("blue")).pack(pady=5)
    tk.Button(color_win, text="Yellow", width=10, command=lambda: select_color("yellow")).pack(pady=5)

# ==== Hiển thị leaderboard ====
def show_leaderboard():
    scores = load_scores()
    lb_win = tk.Toplevel(root)
    lb_win.title("Leaderboard")
    lb_win.geometry("300x400")

    tk.Label(lb_win, text="🏆 Top Scores 🏆", font=("Arial", 16, "bold")).pack(pady=10)

    if not scores:
        tk.Label(lb_win, text="Chưa có điểm nào!", font=("Arial", 12)).pack(pady=20)
    else:
        for i, s in enumerate(scores[:10], start=1):
            tk.Label(lb_win, text=f"{i}. {s['user']} - {s['score']}", font=("Arial", 12)).pack(anchor="w", padx=50)

# ==== Login/Register ====
def login():
    username = entry_username.get()
    password = entry_password.get()
    users = load_users()

    if username in users and users[username] == password:
        save_config(username=username)  # lưu tên user vào config
        messagebox.showinfo("Đăng nhập", f"Chào mừng {username}!")
        btn_play.place(x=150, y=450)  # hiện nút chơi sau khi login
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

def register():
    username = entry_username.get()
    password = entry_password.get()
    users = load_users()

    if username in users:
        messagebox.showerror("Lỗi", "Tên tài khoản đã tồn tại!")
    elif username == "" or password == "":
        messagebox.showerror("Lỗi", "Không được để trống!")
    else:
        users[username] = password
        save_users(users)
        messagebox.showinfo("Đăng ký", "Đăng ký thành công!")

# ==== Giao diện chính ====
root = tk.Tk()
root.title("Flappy Bird - Menu")
root.geometry("400x600")
root.resizable(False, False)

# ==== Background ====
bg_img = Image.open("assets/background-night.png")
bg_img = bg_img.resize((400, 600))
bg = ImageTk.PhotoImage(bg_img)
background_label = tk.Label(root, image=bg)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ==== Title ====
title = tk.Label(root, text="Flappy Bird", font=("Arial", 28, "bold"), fg="yellow", bg="#87CEEB")
title.place(x=100, y=50)

# ==== Nhập user/pass ====
tk.Label(root, text="Tên đăng nhập", font=("Arial", 12), bg="#87CEEB").place(x=50, y=150)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.place(x=170, y=150)

tk.Label(root, text="Mật khẩu", font=("Arial", 12), bg="#87CEEB").place(x=50, y=200)
entry_password = tk.Entry(root, show="*", font=("Arial", 12))
entry_password.place(x=170, y=200)

# ==== Style nút ====
button_style = {
    "font": ("Arial", 14, "bold"),
    "fg": "white",
    "bg": "#ff9933",
    "activebackground": "#ff6600",
    "activeforeground": "white",
    "width": 12,
    "height": 1,
    "bd": 0,
    "highlightthickness": 0,
    "relief": "flat",
    "cursor": "hand2"
}

btn_login = tk.Button(root, text="Đăng nhập", command=login, **button_style)
btn_login.place(x=140, y=270)

btn_register = tk.Button(root, text="Đăng ký", command=register, **button_style)
btn_register.place(x=140, y=330)

btn_play = tk.Button(root, text="Chơi", command=choose_color, **button_style)  # hiện sau login

btn_leaderboard = tk.Button(root, text="Leaderboard", command=show_leaderboard, **button_style)
btn_leaderboard.place(x=140, y=390)

root.mainloop()
