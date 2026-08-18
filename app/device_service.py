from device_detector import DeviceDetector
from user_agents import parse as parse_fallback

def parse_device(user_agent_string: str) -> str:
    if not user_agent_string:
        return "Unknown Device"

    try:
        device = DeviceDetector(user_agent_string).parse()

        client_name = device.client_name() or "Unknown Browser"
        os_name = device.os_name() or "Unknown OS"
        device_brand = device.device_brand() or ""
        device_model = device.device_model() or ""

        device_label = f"{device_brand} {device_model}".strip()

        if device_label:
            return f"{client_name} on {device_label} ({os_name})"
        return f"{client_name} on {os_name}"

    except Exception:
        try:
            ua = parse_fallback(user_agent_string)
            browser = ua.browser.family or "Unknown Browser"
            os_name = ua.os.family or "Unknown OS"
            device = ua.device.family if ua.device.family and ua.device.family != "Other" else None
            if device:
                return f"{browser} on {device} ({os_name})"
            return f"{browser} on {os_name}"
        except Exception:
            return "Unknown Device"

def get_device_type(user_agent_string: str) -> str:
    if not user_agent_string:
        return "unknown"
    try:
        device = DeviceDetector(user_agent_string).parse()
        return device.device_type() or "unknown"
    except Exception:
        return "unknown"