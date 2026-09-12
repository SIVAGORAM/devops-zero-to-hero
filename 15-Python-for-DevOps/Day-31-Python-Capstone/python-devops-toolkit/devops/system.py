import platform, os

def get_system_info():
    return {'OS': platform.system(), 'OS Version': platform.version(), 'Machine': platform.machine(), 'Processor': platform.processor(), 'CPU Count': os.cpu_count()}
