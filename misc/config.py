from dataclasses import dataclass


@dataclass
class ConfigManager:
    """Holds all the configuration for the game"""

    title: str = "2D Game Engine"
    window_width: int = 1280
    window_height: int = 720
    full_screen: bool = False
    target_fps: int = 60
    debug: bool = False
    log_file_name: str = "engine_log.txt"
    debug_to_file: bool = True
    debug_to_console: bool = False
    verbose_logging: bool = True
