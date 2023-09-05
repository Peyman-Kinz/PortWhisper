import tkinter as tk
import socket
import threading

def open_tools_page():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tools_label = tk.Label(main_frame, text="Tools", font=("Helvetica", 24))
    tools_label.grid(row=0, column=0, pady=20)
    back_button = tk.Button(main_frame, text="Zurück", command=main_frame)
    back_button.grid(row=1, column=0, pady=20)

def cancel_scan():
    global scan_cancelled
    scan_cancelled = True
    result_text.insert(tk.END, "Scan beendet.\n")

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
root.title("PortGhost")
root.geometry("800x600")

main_frame = tk.Frame(root)
main_frame.pack(side="left", fill="both", expand=True)

background_color1 = (100, 100, 255)
background_color2 = (255, 100, 100)

tools_button = tk.Button(main_frame, text="Tools", bg="red", command=open_tools_page)
tools_button.pack()

button = tk.Button(main_frame, text="Help", bg="red")
button.pack(side="left")

label = tk.Label(main_frame, text="PortGhost", font=("Helvetica", 24))
label.pack(pady=20)

entry = tk.Entry(main_frame, font=("Helvetica", 14))
entry.pack(padx=20, pady=10)

scan_button = tk.Button(main_frame, text="Scan starten", command=scan_ports)
scan_button.pack()

cancel_button = tk.Button(main_frame, text="Scan beenden", command=cancel_scan)
cancel_button.pack()

result_text = tk.Text(main_frame, font=("Helvetica", 14))
result_text.pack(padx=20, pady=20, fill='both', expand=True)

root.mainloop()
