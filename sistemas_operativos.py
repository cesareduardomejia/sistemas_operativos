# IMPORTAMOS LIBRERIAS.
from flask import jsonify
import psutil
import platform
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json as js


cred = credentials.Certificate(
    'sistemas-operativos-4532d-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sistemas-operativos-4532d-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')

ref = db.reference('pc`s_manager')
pc_ref = ref.child('pc1_manager')

# FUNCION PARA REPRESENTAR TAMAÑOS EN BITS.


def get_size(bytes, suffix='B'):
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor


# INFORMACIÓN BÁSICA DEL SISTEMA.
print('='*40, 'System Information', '='*40)
uname = platform.uname()
print(f'System: {uname.system}')
print(f'Node Name: {uname.node}')
print(f'Release: {uname.release}')
print(f'Version: {uname.version}')
print(f'Machine: {uname.machine}')
print(f'Processor: {uname.processor}')

# INFORMACIÓN DE LA CPU
print('='*40, 'CPU Info', '='*40)
# Nº NUCLEOS
print('Physical cores:', psutil.cpu_count(logical=False))
print('Total cores:', psutil.cpu_count(logical=True))
# FRECUENCIAS CPU
cpufreq = psutil.cpu_freq()
print(f'Max Frequency: {cpufreq.max:.2f}Mhz')
print(f'Min Frequency: {cpufreq.min:.2f}Mhz')
print(f'Current Frequency: {cpufreq.current:.2f}Mhz')
# USO DE CPU


def CPU_usage():
    cpus = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpus[i] = float(percentage)

    return cpus


print(f'Total CPU Usage: {psutil.cpu_percent()}%')
# MEMORIA
print('='*40, 'Memory Information', '='*40)
svmem = psutil.virtual_memory()
print(f'Total: {get_size(svmem.total)}')
print(f'Available: {get_size(svmem.available)}')
print(f'Used: {get_size(svmem.used)}')
print(f'Percentage: {svmem.percent}%')

if(svmem.percent >= 40):
    print('*******Alerta de Memoria ***********')

print('='*20, 'SWAP', '='*20)
swap = psutil.swap_memory()
print(f'Total: {get_size(swap.total)}')
print(f'Free: {get_size(swap.free)}')
print(f'Used: {get_size(swap.used)}')
print(f'Percentage: {swap.percent}%')


# INFORMACIÓN DEL DISCO DURO
print('='*40, 'Disk Information', '='*40)
print('Partitions and Usage:')



partitions = psutil.disk_partitions()
devices = {}
device={}
for partition in partitions:
    
    device['Device'] = partition.device
    device['Mountpoint'] = partition.mountpoint
    device['File system type'] = partition.fstype
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    device['Total Size']= get_size(partition_usage.total)
    device['Used']= get_size(partition_usage.used)
    device['Free']= get_size(partition_usage.free)
    device['Percentage']= partition_usage.percent
    
    

    if(partition_usage.percent >= 50):
        print('************ Alerta de disco lleno  *****************')
disk_io = psutil.disk_io_counters()
device['Total read']= get_size(disk_io.read_bytes)
device['Total write']= get_size(disk_io.write_bytes)
devices.update(device)  


# INFORMACIÓN DE REDES
print('='*40, 'Network Information', '='*40)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f'=== Interface: {interface_name} ===')
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f'  IP Address: {address.address}')
            print(f'  Netmask: {address.netmask}')
            print(f'  Broadcast IP: {address.broadcast}')
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f'  MAC Address: {address.address}')
            print(f'  Netmask: {address.netmask}')
            print(f'  Broadcast MAC: {address.broadcast}')
net_io = psutil.net_io_counters()
print(f'Total Bytes Sent: {get_size(net_io.bytes_sent)}')
print(f'Total Bytes Received: {get_size(net_io.bytes_recv)}')


print(CPU_usage())

cpu_count_f = psutil.cpu_count(logical=False)
cpu_count_t = psutil.cpu_count(logical=True)
cpu_freq_max = cpufreq.max
cpu_freq_min = cpufreq.min
pc_ref.push({
    'System Information': {
        'System': uname.system,
        'Node Name': uname.node,
        'Release': uname.release,
        'Version': uname.version,
        'Processor': uname.processor,
        'Machine': uname.machine
    },
    'get size': {
        'Total Size': get_size(partition_usage.total),
        'Used': get_size(partition_usage.used),
        'Free': get_size(partition_usage.free),
        'Percentage': partition_usage.percent
    },
    'CPU Info': {
        'Physical cores': cpu_count_f,
        'Total cores': cpu_count_t,
        'Max Frequency': cpu_freq_max,
        'Min Frequency': cpu_freq_min,
        'Current Frequency': cpufreq.current,
        'CPU Usage Per Core': CPU_usage(),
        'Total CPU Usage': psutil.cpu_percent()
    },
    'Memory Information': {
        'Total': get_size(svmem.total),
        'Available': get_size(svmem.available),
        'Used': get_size(svmem.used),
        'Percentage': svmem.percent
    },
    'SWAP': {
        'Total': get_size(swap.total),
        'Free': get_size(swap.free),
        'Used': get_size(swap.used),
        'Percentage': swap.percent,
    },
    'Disk Information': {
        'Partitions and Usage': devices
    }


})
print(partitions)
print(devices)