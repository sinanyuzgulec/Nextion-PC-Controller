import psutil
import socket
import time
import wmi
import pynvml


try:
    pynvml.nvmlInit()
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    has_gpu = True
except:
    has_gpu = False


try:
    w = wmi.WMI(namespace="root\\wmi")
except:
    w = None

def get_stats():
    try:
        cpu_usage = int(psutil.cpu_percent())
        cpu_freq_mhz = psutil.cpu_freq().current
        cpu_ghz = f"{round(cpu_freq_mhz / 1000, 1)} GHz"
        
        cpu_temp = "N/A"
        if w:
            try:
                temp = w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature
                cpu_temp = f"{int((temp / 10.0) - 273.15)} C"
            except:
                cpu_temp = "N/A"

        ram_usage = int(psutil.virtual_memory().percent)

        gpu_usage = 0
        gpu_temp = "N/A"
        gpu_ghz = "N/A"
        
        if has_gpu:
            try:
                util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
                gpu_usage = int(util.gpu)
                gpu_temp = f"{pynvml.nvmlDeviceGetTemperature(gpu_handle, 0)} C"
                gpu_mhz = pynvml.nvmlDeviceGetClockInfo(gpu_handle, 0)
                gpu_ghz = f"{round(gpu_mhz / 1000, 1)} GHz"
            except:
                pass

        ip_addr = socket.gethostbyname(socket.gethostname())
        uptime_seconds = time.time() - psutil.boot_time()
        d, h_rem = divmod(uptime_seconds, 86400)
        h, m_rem = divmod(h_rem, 3600)
        m, _ = divmod(m_rem, 60)
        uptime_str = f"{int(d)}d {int(h):02}:{int(m):02}"

        return {
            "j0": cpu_usage,    "j1": ram_usage,    "j2": gpu_usage,
            "t1": f"%{cpu_usage}", "t2": f"%{ram_usage}", "t5": f"%{gpu_usage}",
            "t12": cpu_temp, "t13": gpu_temp,
            "t14": cpu_ghz,  "t15": gpu_ghz,  
            "t0": ip_addr, "t4": uptime_str
        }
    except Exception as e:
        print(f"Hata: {e}")
        return {}