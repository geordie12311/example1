"""
ospf test script
"""
import os
import sys
from nornir import InitNornir
from nornir_scrapli.tasks import send_command

"""
making the config file dynamic using sys argument.
I.e., add after python3 "filename" then "specify 
configfile name" (example python3 test1.py config.yaml)
"""
config_file = sys.argv[1]
nr = InitNornir(config_file=config_file)

"""
binding nornir username/passord to variables
input on cli using export command
"""
nr.inventory.defaults.username = os.getenv("USERNAME")
nr.inventory.defaults.password = os.getenv("PASSWORD")

def pull_info(task):
    """
    pulling info from
    hosts
    """
    result = task.run(task=send_command, command="show ip ospf neighbor")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interfaces"]
    for intf in interfaces:
        neighbors = interfaces[intf]["neighbors"]
        for neighbor in neighbors:
            state = neighbors[neighbor]["state"]
            return state

state_result = nr.run(task=pull_info)
for host in nr.inventory.hosts.values():
    state = state_result[f"{host}"][0].result
    assert "FULL" in state, "Failed"
    print("PASSED")



