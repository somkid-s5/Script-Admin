from paramiko import SSHClient, AutoAddPolicy
from tabulate import tabulate

# VM details
vm_details = [
    {'hostname': 'host-ip', 'port': 22, 'username': 'your username', 'password': 'your password'},
    {'hostname': 'host-ip', 'port': 22, 'username': 'your username', 'password': 'your password'},
    {'hostname': 'host-ip', 'port': 22, 'username': 'your username', 'password': 'your password'},
]

def parse_memory_info(memory_line):
    parts = memory_line.split()
    memory_info = {
        'Total Memory': parts[1],
        'Used Memory': parts[2],
        'Free Memory': parts[3],
        'Shared Memory': parts[4],
        'Buffer/Cache Memory': parts[5],
        'Available Memory': parts[6]
    }
    return memory_info

def get_free_memory(hostname, port, username, password):
    try:
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("free -h")
        output = stdout.read().decode('utf-8')

        client.close()

        lines = output.strip().splitlines()
        for line in lines:
            if "Mem:" in line:
                return parse_memory_info(line)

    except Exception as e:
        return f"Failed to connect to {hostname}: {e}"

# Collect memory information from all VMs
mem_info = []
for vm in vm_details:
    memory = get_free_memory(vm['hostname'], vm['port'], vm['username'], vm['password'])
    if isinstance(memory, dict):
        # Add the hostname to the memory info dictionary
        memory['Hostname'] = vm['hostname']
        mem_info.append(memory)

# Display memory information as a table
if mem_info:
    print(tabulate(mem_info, headers="keys", tablefmt="pretty"))
else:
    print("No memory information available.")
