from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(percent):
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(percent / 100, None)

def toggle_mute():
    volume = get_volume_interface()
    current_mute = volume.GetMute()
    volume.SetMute(not current_mute, None)
    return not current_mute

def toggle_mic_mute():
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
    volume = get_volume_interface()
    return int(volume.GetMasterVolumeLevelScalar() * 100)