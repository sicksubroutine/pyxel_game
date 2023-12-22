from dataclasses import dataclass


@dataclass
class ConfigManager:
    """Holds all the configuration for the game"""

    title: str = "Untitled 64x64 Shmup"
    window_width: int = 64
    window_height: int = 64
    full_screen: bool = False
    target_fps: int = 60
    debug: bool = False
    log_file_name: str = "shmup_log.txt"
    debug_to_file: bool = True
    debug_to_console: bool = False
    verbose_logging: bool = True
