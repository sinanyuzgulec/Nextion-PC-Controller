import serial
import serial.tools.list_ports
import threading
import time
import sys

import system_monitor 
import media_control

class NextionKernel:
    def __init__(self, baudrate=9600):
        self.current_page = "mainPage"
        self.running = True
        self.ser = self.auto_find_port(baudrate)
        
        if not self.ser:
            print("[!] Nextion bulunamadı. Kabloyu kontrol et.")
            sys.exit()

    def auto_find_port(self, baudrate):
        ports = list(serial.tools.list_ports.comports())
        # COM1'i ele, USB olanlara öncelik ver
        for port in sorted(ports, key=lambda x: "USB" in x.description, reverse=True):
            if "COM1" == port.device: continue
            try:
                s = serial.Serial(port.device, baudrate, timeout=0.1)
                print(f"[+] {port.device} üzerine bağlandı.")
                return s
            except: continue
        return None

    def send(self, cmd):
        """Donanım seviyesinde veri gönderimi"""
        try:
            self.ser.write(cmd.encode('ascii') + b'\xff\xff\xff')
        except: pass

    def worker_loop(self):
        """Sayfalara göre ilgili modülü çalıştıran ana döngü"""
        while self.running:
            # 1. Sistem Sayfası
            if self.current_page == "cputempPage":
                data = system_monitor.get_stats()
                for obj, val in data.items():
                    if obj.startswith('j'): # Progressbar
                        self.send(f"{obj}.val={val}")
                    else: # Text
                        self.send(f'{obj}.txt="{val}"')
            
            # 2. Borsa Sayfası (Eklendiğinde aktif edilecek)
            # elif self.current_page == "currencyPage":
            #     data = currency_monitor.get_rates()
            #     ...
            
            time.sleep(2)

    def listener(self):
        """Nextion'dan gelen sayfa değişimlerini yakalar"""
        buffer = b""
        while self.running:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                buffer += data
                if b'\xff\xff\xff' in buffer:
                    parts = buffer.split(b'\xff\xff\xff')
                    for part in parts[:-1]:
                        msg = part.decode('utf-8', errors='ignore').strip()
                        if msg.startswith("page:"):
                            self.current_page = msg.split(":")[1]
                            print(f"[*] Aktif Ekran: {self.current_page}")
                    buffer = parts[-1]
            time.sleep(0.01)

    def start(self):
        threading.Thread(target=self.worker_loop, daemon=True).start()
        self.listener()

def worker_loop(self):
        while self.running:
            if self.current_page == "systemPage": # Sayfa ismini kontrol et
                vol = media_control.get_current_volume()
                self.send(f"h0.val={vol}")      # Slider'ı güncelle
                self.send(f"t3.txt=\"{vol}\"")  # Texti güncelle
            
            # ... (Diğer sayfa kontrolleri)
            time.sleep(1)

def handle_incoming(self, msg):
        # Slider'dan gelen değer (Örn: "h0:75")
        if ":" in msg and msg.startswith("h0"):
            val = int(msg.split(":")[1])
            media_control.set_volume(val)
            
        # Mikrofon Butonu (p1)
        elif msg == "p1_press":
            media_control.toggle_mic_mute()
            
        # Hoparlör Butonu (p0)
        elif msg == "p0_press":
            media_control.toggle_mute()
            
        # Sayfa Değişimi
        elif msg.startswith("page:"):
            self.current_page = msg.split(":")[1]

if __name__ == "__main__":
    kernel = NextionKernel()
    kernel.start()