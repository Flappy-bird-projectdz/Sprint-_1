import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess, json, os
from controller.thum_controller import AuthController
from utilis import load_scores

CONFIG_FILE = "config.json"
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

# ==== Giao diện chính ====
root = tk.Tk()
root.title("Flappy Bird - Menu")
root.geometry("400x600")
root.resizable(False, False)

# ==== Background ====
bg_img = Image.open("assets/background-night.png").resize((400, 600))
bg = ImageTk.PhotoImage(bg_img)
tk.Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

# ==== Title ====
tk.Label(root, text="Flappy Bird", font=("Arial", 28, "bold"), fg="yellow", bg="#87CEEB").place(x=100, y=50)

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

# ==== Khung đăng nhập ====
frame_login = tk.Frame(root, bg="#87CEEB")
frame_login.place(x=0, y=120, width=400, height=400)

tk.Label(frame_login, text="Tên đăng nhập", font=("Arial", 12), bg="#87CEEB").place(x=50, y=30)
entry_username = tk.Entry(frame_login, font=("Arial", 12))
entry_username.place(x=170, y=30)

tk.Label(frame_login, text="Mật khẩu", font=("Arial", 12), bg="#87CEEB").place(x=50, y=80)
entry_password = tk.Entry(frame_login, show="*", font=("Arial", 12))
entry_password.place(x=170, y=80)

def login():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    user = auth.xu_ly_dang_nhap(username, password)
    if user:
        save_config(username=username)
        messagebox.showinfo("Đăng nhập", f"Chào mừng {user['username']}!\nEmail: {user['email']}")
        show_play_skin()
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

btn_login = tk.Button(frame_login, text="Đăng nhập", command=login, **button_style)
btn_login.place(x=140, y=140)

# Nút chuyển sang đăng ký
def show_register_form():
    frame_login.place_forget()
    frame_register.place(x=0, y=120, width=400, height=400)

btn_to_register = tk.Button(frame_login, text="Chưa có tài khoản?", command=show_register_form,
                            font=("Arial", 10, "italic"), bg="#87CEEB", fg="blue", cursor="hand2", bd=0)
btn_to_register.place(x=140, y=200)

# ==== Khung đăng ký ====
frame_register = tk.Frame(root, bg="#87CEEB")

tk.Label(frame_register, text="Tên đăng nhập", font=("Arial", 12), bg="#87CEEB").place(x=50, y=30)
entry_reg_user = tk.Entry(frame_register, font=("Arial", 12))
entry_reg_user.place(x=170, y=30)

tk.Label(frame_register, text="Mật khẩu", font=("Arial", 12), bg="#87CEEB").place(x=50, y=80)
entry_reg_pass = tk.Entry(frame_register, show="*", font=("Arial", 12))
entry_reg_pass.place(x=170, y=80)

tk.Label(frame_register, text="Email", font=("Arial", 12), bg="#87CEEB").place(x=50, y=130)
entry_reg_email = tk.Entry(frame_register, font=("Arial", 12))
entry_reg_email.place(x=170, y=130)

def register():
    username = entry_reg_user.get().strip()
    password = entry_reg_pass.get().strip()
    email = entry_reg_email.get().strip()
    result = auth.xu_ly_dang_ky(username, password, email)
    if result == "Đăng ký thành công!":
        messagebox.showinfo("Đăng ký", result)
        show_login_form()
    else:
        messagebox.showerror("Lỗi", result)

btn_register = tk.Button(frame_register, text="Đăng ký", command=register, **button_style)
btn_register.place(x=140, y=190)

# Nút quay lại đăng nhập
def show_login_form():
    frame_register.place_forget()
    frame_login.place(x=0, y=120, width=400, height=400)

btn_back = tk.Button(frame_register, text="⬅ Quay lại", command=show_login_form,
                     font=("Arial", 10, "italic"), bg="#87CEEB", fg="blue", cursor="hand2", bd=0)
btn_back.place(x=160, y=250)

# ==== Chọn skin + chơi ====
def show_play_skin():
    frame_login.place_forget()
    frame_register.place_forget()
    frame_play = tk.Frame(root, bg="#87CEEB")
    frame_play.place(x=0, y=120, width=400, height=400)

    tk.Label(frame_play, text="Chọn màu Bird", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=20)

    # Load hình ảnh skin
    skin_files = {
        "red": "assets/redbird-midflap.png",
        "blue": "assets/bluebird-downflap.png",
        "yellow": "assets/yellowbird-midflap.png"
    }

    images_skin = {}
    for color, path in skin_files.items():
        img = Image.open(path).resize((68, 48))
        images_skin[color] = ImageTk.PhotoImage(img)

    # Hàm bắt click
    def select_skin(color):
        save_config(bird_color=color)
        root.destroy()
        subprocess.run(["python", "flappy.py"])

    # Hiển thị hình và bắt click
    frame_skins = tk.Frame(frame_play, bg="#87CEEB")
    frame_skins.pack(pady=20)

    for color, img in images_skin.items():
        lbl = tk.Label(frame_skins, image=img, bg="#87CEEB", cursor="hand2")
        lbl.image = img
        lbl.pack(side="left", padx=15)
        lbl.bind("<Button-1>", lambda e, c=color: select_skin(c))

root.mainloop()
