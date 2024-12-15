import tkinter as tk
import psutil
import time
import platform
import cpuinfo
import gpuinfo
from threading import Thread

# Funktion zum Abrufen von Systemdaten
def get_system_data():
    while True:
        # CPU-Informationen (mit cpuinfo)
        cpu_info = cpuinfo.get_cpu_info()
        cpu_name = cpu_info.get("cpu", "Unbekannt")  # Genauer CPU-Name

        # CPU-Auslastung
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # RAM-Informationen
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        total_ram = ram.total / (1024 * 1024 * 1024)  # in GB
        ram_available = ram.available / (1024 * 1024 * 1024)  # in GB

        # Festplattenspeicher
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        total_disk = disk.total / (1024 * 1024 * 1024 * 1024)  # in TB
        
        # Netzwerkdaten
        net = psutil.net_io_counters()
        net_sent = net.bytes_sent / (1024 * 1024)  # in MB
        net_recv = net.bytes_recv / (1024 * 1024)  # in MB

        # GPU-Informationen (mit gpuinfo)
        gpus = gpuinfo.get_info.GPUInfo.get_info()
        gpu_name = gpus[0].gpu if gpus else "Keine GPU gefunden"
        
        # GUI aktualisieren
        update_gui(cpu_name, cpu_usage, ram_usage, total_ram, ram_available, disk_usage, total_disk, net_sent, net_recv, gpu_name)

        time.sleep(1)

# Funktion zum Aktualisieren der GUI
def update_gui(cpu_name, cpu_usage, ram_usage, total_ram, ram_available, disk_usage, total_disk, net_sent, net_recv, gpu_name):
    cpu_label.config(text=f"CPU: {cpu_name} - Auslastung: {cpu_usage}%")
    ram_label.config(text=f"RAM: {total_ram:.2f} GB (Verfügbar: {ram_available:.2f} GB) - Auslastung: {ram_usage}%")
    disk_label.config(text=f"Festplatte: {total_disk:.2f} TB - Auslastung: {disk_usage}%")
    net_sent_label.config(text=f"Netzwerk gesendet: {net_sent:.2f} MB")
    net_recv_label.config(text=f"Netzwerk empfangen: {net_recv:.2f} MB")
    gpu_label.config(text=f"GPU: {gpu_name}")

# Funktion zum Zentrieren des Fensters auf dem Bildschirm
def center_window(window, width, height):
    # Bildschirmauflösung erhalten
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Berechnung der Position, um das Fenster zu zentrieren
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)

    # Position des Fensters festlegen
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Erstellen der GUI
root = tk.Tk()
root.title("Live Hardware-Daten")
root.configure(bg="#2e2e2e")  # Dark Mode Hintergrundfarbe

# Fenstergöße festlegen und zentrieren
center_window(root, 800, 600)

# GUI-Elemente
cpu_label = tk.Label(root, text="CPU: Laden...", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
cpu_label.pack(pady=10)

ram_label = tk.Label(root, text="RAM: Laden...", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
ram_label.pack(pady=10)

disk_label = tk.Label(root, text="Festplatte: Laden...", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
disk_label.pack(pady=10)

net_sent_label = tk.Label(root, text="Netzwerk gesendet: 0 MB", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
net_sent_label.pack(pady=10)

net_recv_label = tk.Label(root, text="Netzwerk empfangen: 0 MB", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
net_recv_label.pack(pady=10)

gpu_label = tk.Label(root, text="GPU: Laden...", font=("Helvetica", 12), fg="white", bg="#2e2e2e")
gpu_label.pack(pady=10)

# Starten des Threads zum Abrufen der Daten
thread = Thread(target=get_system_data, daemon=True)
thread.start()

# Hauptloop der GUI
root.mainloop()
