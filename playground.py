import psutil, datetime


print("CPU Percent:", psutil.cpu_percent(interval=1))
print("RAM Percent:", psutil.virtual_memory()[2])
print("RAM Total:", round(psutil.virtual_memory()[0] / 1000000000, 2))
print("Boot Time:", datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
print("Processes running:", len(psutil.pids()))
