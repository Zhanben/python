import psutil

cpus = psutil.cpu_percent(interval=1, percpu=True)
print(cpus)