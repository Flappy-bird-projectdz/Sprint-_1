import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess, json, os
from controller.thum_controller import AuthController
from utilis import load_scores

CONFIG_FILE = "config.json"

# ==== Khởi tạo bộ điều khiển xác thực ====
auth = AuthController()

# ==== Lưu config (màu chim + username) ====
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
        json.dump(cfg, f, indent=4)

# ==== Chọn màu chim ====
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

# ==== Đăng nhập ====
def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    user = auth.xu_ly_dang_nhap(username, password)

    if user:
        save_config(username=username)
        messagebox.showinfo("Đăng nhập", f"Chào mừng {user.username}!\nEmail: {user.email}")
        btn_play.place(x=150, y=510)
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

# ==== Đăng ký ====
def register():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    email = entry_email.get().strip()
    result = auth.xu_ly_dang_ky(username, password, email)
    if result == "Đăng ký thành công!":
        messagebox.showinfo("Đăng ký", result)
    else:
        messagebox.showerror("Lỗi", result)

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

# ==== Nhập user/pass/email ====
tk.Label(root, text="Tên đăng nhập", font=("Arial", 12), bg="#87CEEB").place(x=50, y=150)
entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.place(x=170, y=150)

tk.Label(root, text="Mật khẩu", font=("Arial", 12), bg="#87CEEB").place(x=50, y=200)
entry_password = tk.Entry(root, show="*", font=("Arial", 12))
entry_password.place(x=170, y=200)

tk.Label(root, text="Email", font=("Arial", 12), bg="#87CEEB").place(x=50, y=250)
entry_email = tk.Entry(root, font=("Arial", 12))
entry_email.place(x=170, y=250)

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
btn_login.place(x=140, y=320)

btn_register = tk.Button(root, text="Đăng ký", command=register, **button_style)
btn_register.place(x=140, y=380)

btn_play = tk.Button(root, text="Chơi", command=choose_color, **button_style)
btn_leaderboard = tk.Button(root, text="Leaderboard", command=show_leaderboard, **button_style)
btn_leaderboard.place(x=140, y=440)

def choose_color():
    color_win = tk.Toplevel(root)
    color_win.title("Chọn màu Bird")
    color_win.geometry("400x400")
    color_win.resizable(False, False)

    # ==== Background (dùng đường dẫn tuyệt đối) ====
    bg_path = os.path.join(os.path.dirname(__file__), "assets", "background-night.png")
    if not os.path.exists(bg_path):
        messagebox.showerror("Lỗi", f"Không tìm thấy ảnh nền:\n{bg_path}")
        return

    bg_img = Image.open(bg_path).resize((400, 400))
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(color_win, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ==== Tiêu đề ====
    title_label = tk.Label(color_win,
                           text="🐤 Chọn màu cho Bird 🐤",
                           font=("Arial", 16, "bold"),
                           fg="yellow",
                           bg="#3C9BD0")  # màu gần giống nền bầu trời
    title_label.pack(pady=10)

    # ==== Vùng xem trước ====
    preview_label = tk.Label(color_win, text="Xem trước", font=("Arial", 12, "italic"), bg="#3C9BD0")
    preview_label.pack(pady=5)

    # Ảnh xem trước ban đầu (đỏ)
    bird_path = os.path.join(os.path.dirname(__file__), "assets", "redbird-midflap.png")
    bird_img = Image.open(bird_path).resize((68, 48))
    bird_photo = ImageTk.PhotoImage(bird_img)
    preview_canvas = tk.Label(color_win, image=bird_photo, bg="#3C9BD0")
    preview_canvas.image = bird_photo
    preview_canvas.pack(pady=10)

    # ==== Hàm cập nhật ảnh preview ====
    def update_preview(color):
        bird_files = {
            "red": "redbird-midflap.png",
            "blue": "bluebird-downflap.png",
            "yellow": "yellowbird-midflap.png"
        }
        new_path = os.path.join(os.path.dirname(__file__), "assets", bird_files[color])
        new_img = Image.open(new_path).resize((68, 48))
        new_photo = ImageTk.PhotoImage(new_img)
        preview_canvas.config(image=new_photo)
        preview_canvas.image = new_photo

    # ==== Hàm chọn màu ====
    def select_color(color):
        save_config(bird_color=color)
        color_win.destroy()
        root.destroy()
        subprocess.run(["python", "flappy.py"])

    # ==== Khung chứa các nút màu ====
    frame = tk.Frame(color_win, bg="#3C9BD0")
    frame.pack(pady=20)

    button_style = {
        "font": ("Arial", 14, "bold"),
        "fg": "white",
        "width": 10,
        "height": 1,
        "bd": 0,
        "highlightthickness": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    btn_red = tk.Button(frame, text="Red", bg="#ff3333", activebackground="#ff6666",
                        command=lambda: select_color("red"), **button_style)
    btn_red.pack(pady=5)
    btn_red.bind("<Enter>", lambda e: update_preview("red"))

    btn_blue = tk.Button(frame, text="Blue", bg="#3399ff", activebackground="#66b3ff",
                         command=lambda: select_color("blue"), **button_style)
    btn_blue.pack(pady=5)
    btn_blue.bind("<Enter>", lambda e: update_preview("blue"))

    btn_yellow = tk.Button(frame, text="Yellow", bg="#ffcc00", activebackground="#ffdb4d",
                           command=lambda: select_color("yellow"), **button_style)
    btn_yellow.pack(pady=5)
    btn_yellow.bind("<Enter>", lambda e: update_preview("yellow"))

    # ==== Nút quay lại ====
    def go_back():
        color_win.destroy()

    back_btn = tk.Button(color_win,
                         text="⬅ Quay lại",
                         command=go_back,
                         font=("Arial", 12, "bold"),
                         fg="white",
                         bg="#6666ff",
                         activebackground="#3333ff",
                         width=12,
                         height=1,
                         bd=0,
                         relief="flat",
                         cursor="hand2")
    back_btn.pack(pady=15)



root.mainloop()
