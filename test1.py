"""
Python script to test
jenkins config build
"""
import os
import sys
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirExecutionError

"""
making the config file
dynamic using sys argument.
I.e., add after python3 "filename"
then "specify configfile name"
(example python3 test1.py config.yaml)
"""
config_file = sys.argv[1]
nr = InitNornir(config_file=config_file)
"""
binding nornir username/passord to variables
input on cli using export command
"""
nr.inventory.defaults.username = os.getenv("USERNAME")
nr.inventory.defaults.password = os.getenv("PASSWORD")

def pull_vars(task):
    """
    Pull host vars
    """
    result = task.run(task=load_yaml, file="group_vars/all.yaml")
    task.host["facts"] = result.result
    push_config(task)

def push_config(task):
    """
    Push config changes
    """
    ospf_configs = task.run(task=template_file, template="ospf.j2", path="templates")
    configurations = ospf_configs.result.splitlines()
    task.run(task=send_configs, configs=configurations)

results = nr.run(task=pull_vars)
print_result(results)
failures = nr.data.failed_hosts
if failures:
    raise NornirExecutionError("Nornir Failure Detected")
