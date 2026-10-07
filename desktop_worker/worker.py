"""Host-session desktop worker. Importable on non-Windows hosts for capability reporting."""
import platform


def capabilities() -> dict:
    return {"platform": platform.system(), "available": platform.system() == "Windows",
            "automation": "UI Automation", "requires_interactive_session": True}


class DesktopWorker:
    def __init__(self):
        if platform.system() != "Windows":
            raise RuntimeError("Desktop worker requires a Windows interactive user session")
        from pywinauto import Desktop
        self.desktop = Desktop(backend="uia")

    def inspect_window(self, title_re: str) -> dict:
        window = self.desktop.window(title_re=title_re)
        window.wait("exists ready", timeout=5)
        controls = []
        for index, control in enumerate(window.descendants()):
            info = control.element_info
            controls.append({"index": index, "name": info.name[:120], "control_type": info.control_type,
                             "automation_id": info.automation_id, "enabled": bool(info.enabled)})
        return {"title": window.window_text(), "controls": controls}
