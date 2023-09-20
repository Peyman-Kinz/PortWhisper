import tkinter as tk
from tkinter import ttk
import socket
import threading
import paramiko
import http.client

def cancel_scan():
    global scan_cancelled
    scan_cancelled = True
    result_text.insert(tk.END, "Scan beendet.\n")

def scan_ports():
    target = entry.get()
    result_text.delete("1.0", tk.END)
    port_range = port_entry.get().split('-')

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        result_text.insert(tk.END, "Ungültiger Hostname")
        return

    def do_scan(port, scan_type):
        try:
            if scan_type == "TCP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
            elif scan_type == "UDP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                result = sock.connect_ex((target_ip, port))
            elif scan_type == "HTTP":
                conn = http.client.HTTPConnection(target_ip, port, timeout=1)
                conn.request("GET", "/")
                response = conn.getresponse()
                result = response.status
                conn.close()
            else:
                result_text.insert(tk.END, "Ungültiger Scan-Typ")
                return

            if result == 0:
                result_text.insert(tk.END, f"(Port {port} ist offen.)\n", "open")
            elif result == 200:
                result_text.insert(tk.END, f"(Port {port} ist ein HTTP-Server und geöffnet.)\n", "open")
            else:
                result_text.insert(tk.END, f"(Port {port} ist geschlossen.)\n", "closed")
        except socket.timeout:
            result_text.insert(tk.END, f"(Port {port} hat nicht geantwortet.)\n", "timeout")

    start_port = int(port_range[0])
    end_port = int(port_range[1]) if len(port_range) > 1 else start_port

    selected_scan = scan_type_var.get()
    scan_name = scan_types[selected_scan]

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=do_scan, args=(port, scan_name))
        thread.start()


def show_help():
    help_text.set("")

def on_tab_change(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 1:
        show_help()

def enable_dark_mode():
    style = ttk.Style()
    style.configure("TFrame", background="grey")
    style.configure("TEntry", foreground="black", fieldbackground="grey", bordercolor="grey")
    style.configure("TText", foreground="black", fieldbackground="grey", bordercolor="grey")
    style.configure("TButton", background="grey", foreground="black")
    dark_button.configure(state=tk.DISABLED)
    white_button.configure(state=tk.NORMAL)
    scan_button.configure(bg="grey", fg="white")

def enable_white_mode():
    main_frame_canvas.configure(bg="white")
    help_frame_canvas.configure(bg="white")
    settings_frame_canvas.configure(bg="white")
    about_frame_canvas.configure(bg="white")
    entry.configure(bg="white", fg="black", highlightbackground="white")
    port_entry.configure(bg="white", fg="black", highlightbackground="white")
    result_text.configure(bg="white", fg="black")
    scan_button.configure(bg="white", fg="black")
    cancel_button.configure(bg="white", fg="black")
    dark_button.configure(state=tk.NORMAL)
    white_button.configure(state=tk.DISABLED)
    style = ttk.Style()
    style.configure("TFrame", background="white")
    style.configure("TEntry", foreground="black", fieldbackground="white", bordercolor="white")
    style.configure("TText", foreground="black", fieldbackground="white", bordercolor="white")
    style.configure("TButton", background="white", foreground="black")

root = tk.Tk()
root.title("PortGhost")
root.geometry("800x600")
root.configure(bg="white")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

main_frame = ttk.Frame(notebook)
help_frame = ttk.Frame(notebook)
settings_frame = ttk.Frame(notebook)
about_frame = ttk.Frame(notebook)

notebook.add(main_frame, text="Hauptseite")
notebook.add(settings_frame, text="Einstellungen")

style = ttk.Style()
style.configure("open.TLabel", foreground="green")
style.configure("closed.TLabel", foreground="red")

label = tk.Label(main_frame, text="PortGhost", font=("Helvetica", 24))
label.pack(pady=20)

entry = tk.Entry(main_frame, font=("Helvetica", 14))
entry.pack(padx=20, pady=10)

port_label = tk.Label(main_frame, text="Portbereich (bsp. 80-100):", font=("Helvetica", 14))
port_label.pack(padx=20, pady=10)

port_entry = tk.Entry(main_frame, font=("Helvetica", 14))
port_entry.pack(padx=20, pady=10)

scan_button = tk.Button(main_frame, text="Scan starten", command=scan_ports)
scan_button.pack()

cancel_button = tk.Button(main_frame, text="Scan beenden", command=cancel_scan)
cancel_button.pack()

result_text = tk.Text(main_frame, font=("Helvetica", 14))
result_text.pack(padx=20, pady=20, fill='both', expand=True)

result_text.tag_configure("open", foreground="green")
result_text.tag_configure("closed", foreground="red")
result_text.tag_configure("timeout", foreground="orange")

help_text = tk.StringVar()
help_label = tk.Label(help_frame, textvariable=help_text, font=("Helvetica", 14))
help_label.pack()

main_frame_canvas = tk.Canvas(main_frame, bg="white")
main_frame_canvas.pack(fill="both", expand=True)
help_frame_canvas = tk.Canvas(help_frame, bg="white")
help_frame_canvas.pack(fill="both", expand=True)
settings_frame_canvas = tk.Canvas(settings_frame, bg="white")
settings_frame_canvas.pack(fill="both", expand=True)
about_frame_canvas = tk.Canvas(about_frame, bg="white")
about_frame_canvas.pack(fill="both", expand=True)

settings_label = tk.Label(settings_frame, text="Einstellungen", font=("Helvetica", 24))
settings_label.pack(pady=20)

scan_type_var = tk.IntVar()
scan_type_var.set(0)  # Default: TCP-Scan
scan_types = {0: "TCP", 1: "UDP", 2: "HTTP"}

scan_type_label = tk.Label(settings_frame, text="Scan-Typ:", font=("Helvetica", 14))
scan_type_label.pack(padx=20, pady=10)

tcp_scan_radio = tk.Radiobutton(settings_frame, text="TCP", variable=scan_type_var, value=0)
udp_scan_radio = tk.Radiobutton(settings_frame, text="UDP", variable=scan_type_var, value=1)
http_scan_radio = tk.Radiobutton(settings_frame, text="HTTP", variable=scan_type_var, value=2)

tcp_scan_radio.pack(padx=20, pady=5, anchor="w")
udp_scan_radio.pack(padx=20, pady=5, anchor="w")
http_scan_radio.pack(padx=20, pady=5, anchor="w")

dark_button = tk.Button(settings_frame, text="Dark Modus", command=enable_dark_mode)
dark_button.pack(pady=10)

white_button = tk.Button(settings_frame, text="White Modus", command=enable_white_mode)
white_button.pack(pady=10)

crack_button = tk.Button(main_frame, text="Start Password Cracking", command=perform_password_cracking)
crack_button.pack()

root.mainloop()
