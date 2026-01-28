from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_interface():
    """Sistem hoparlör kontrol arayüzüne bağlanır."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(percent):
    """Sistem ses seviyesini %0-100 arası ayarlar."""
    volume = get_volume_interface()
    # pycaw 0.0 ile -65.25 dB arası çalışır, 0.0 tam sestir.
    # Yüzdelik değeri lineer scalar değere çeviriyoruz.
    volume.SetMasterVolumeLevelScalar(percent / 100, None)

def toggle_mute():
    """Hoparlörü sessize alır veya sesi açar (Toggle)."""
    volume = get_volume_interface()
    current_mute = volume.GetMute()
    volume.SetMute(not current_mute, None)
    return not current_mute

def toggle_mic_mute():
    """Varsayılan mikrofonu sessize alır veya açar."""
    try:
        devices = AudioUtilities.GetMicrophone()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        mic_volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_mute = mic_volume.GetMute()
        mic_volume.SetMute(not current_mute, None)
        return not current_mute
    except:
        return None

def get_current_volume():
    """Mevcut ses seviyesini % olarak döner."""
    volume = get_volume_interface()
    return int(volume.GetMasterVolumeLevelScalar() * 100)