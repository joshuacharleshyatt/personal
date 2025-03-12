"""
Systme/Platform Config Information
"""

import json
import platform
import psutil

def get_size(nbytes):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    suffix = ["B", "KB", "MB", "GB", "TB"]
    factor = 1024
    for unit in suffix:
        if nbytes < factor:
            return f"{nbytes:.2f}{unit}"
        nbytes /= factor
    return f"{nbytes:.2f}PB"

def system_info():
    """Gets machine, python, and compiler system info

    Returns:
        Dict: system information
    """
    info = {
        "architecture" : platform.architecture(),
        "machine type" : platform.machine(),
        "machine name" : platform.node(),
        "platform" : platform.platform(),
        "processor" : platform.processor(),
        "cpu count": psutil.cpu_count(logical=True),
        "cpu frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "memory": get_size(psutil.virtual_memory().total),
        "swap": get_size(psutil.swap_memory().total),
        "system" : platform.system(),
        "release" : platform.release(),
        "release version" : platform.version(),
        "python build" : platform.python_build(),
        "compiler" : platform.python_compiler(),
        "python version" : platform.python_version(),
        "python implement" : platform.python_implementation()
    }
    return info

def save_system(filepath = "machine-config.json", encoding='utf-8'):
    """Save system information to file

    Args:
        filepath (str, optional): File to save information to. Defaults to "machine-config.json".
        encoding (str, optional): Character encoding to use. Defaults to 'utf-8'.
    """
    with open(filepath, "w", encoding=encoding) as file:
        machine_config = system_info()
        json.dump(machine_config, file, indent=4) 
