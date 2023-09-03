import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageDraw
import socket
import threading

def scan_ports():
    target = entry.get()
    result_text.delete("1.0", tk.END)
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        result_text.insert(tk.END, "Ungültiger Hostname")
        return

    def do_scan(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            result_text.insert(tk.END, f"Port {port} ist offen.\n")
        sock.close()

    for port in range(1, 1025):
        thread = threading.Thread(target=do_scan, args=(port,))
        thread.start()

root = tk.Tk()
root.title("Portscanner")
root.geometry("800x600")

background_image = Image.new("RGB", (800, 600))
draw = ImageDraw.Draw(background_image)

background_color1 = (100, 100, 255)
background_color2 = (255, 100, 100)

for y in range(600):
    r, g, b = (
        int(background_color1[0] * (1 - y / 600) + background_color2[0] * (y / 600)),
        int(background_color1[1] * (1 - y / 600) + background_color2[1] * (y / 600)),
        int(background_color1[2] * (1 - y / 600) + background_color2[2] * (y / 600)),
    )
    draw.line([(0, y), (800, y)], fill=(r, g, b))

background_image.save("temp_background.png")

background_photo = PhotoImage(file="temp_background.png")

background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

label = tk.Label(root, text="Portscanner", font=("Helvetica", 24))
label.pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack(padx=20, pady=10)

scan_button = tk.Button(root, text="Scan starten", command=scan_ports)
scan_button.pack()

result_text = tk.Text(root, font=("Helvetica", 14))
result_text.pack(padx=20, pady=20, fill='both', expand=True)

root.mainloop()
