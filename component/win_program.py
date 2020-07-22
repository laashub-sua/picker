import psutil

for proc in psutil.process_iter():
    try:
        if proc.status() != 'running':
            continue
        print(proc)
        processName = proc.name()
        processID = proc.pid
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
