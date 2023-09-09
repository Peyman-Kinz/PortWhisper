import tkinter as tk
from tkinter import ttk
import socket
import threading

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

    def do_scan(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            result_text.insert(tk.END, f"(Port {port} ist offen.)\n", "open")
        else:
            result_text.insert(tk.END, f"(Port {port} ist geschlossen.)\n", "closed")
        sock.close()

    start_port = int(port_range[0])
    end_port = int(port_range[1]) if len(port_range) > 1 else start_port

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=do_scan, args=(port,))
        thread.start()

def show_help():
    help_text.set("PortGhost ist ein einfaches Tool zum Scannen von Ports auf einem \nZielrechner.\n "
                  "Du kannst einen Hostnamen oder eine IP-Adresse eingeben und einen \nPortbereich definieren.\n "
                  "PortGhost wird dann versuchen, die angegebenen Ports auf Erreichbarkeit \nzu überprüfen und\n "
                  "dir mitteilen, welche Ports offen oder geschlossen sind. Du kannst die \nErgebnisse in Echtzeit \nauf dem Bildschirm sehen.\n")

def on_tab_change(event):
    current_tab = notebook.index(notebook.select())
    if current_tab == 1:
        show_help()

root = tk.Tk()
root.title("PortGhost")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

main_frame = ttk.Frame(notebook)
help_frame = ttk.Frame(notebook)

notebook.add(main_frame, text="Hauptseite")
notebook.add(help_frame, text="Hilfe")

style = ttk.Style()
style.configure("open.TLabel", foreground="green")
style.configure("closed.TLabel", foreground="red")

label = tk.Label(main_frame, text="PortGhost", font=("Helvetica", 24))
label.pack(pady=20)

entry = tk.Entry(main_frame, font=("Helvetica", 14))
entry.pack(padx=20, pady=10)

port_label = tk.Label(main_frame, text="Portbereich (z.B. 80-100):", font=("Helvetica", 14))
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

help_text = tk.StringVar()
help_label = tk.Label(help_frame, textvariable=help_text, font=("Helvetica", 14))
help_label.pack()

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

root.mainloop()
