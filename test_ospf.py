"""
ospf test script
"""
from nornir import InitNornir
from nornir_scrapli.tasks import send_command

nr = InitNornir(config_file="config.yaml")

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



