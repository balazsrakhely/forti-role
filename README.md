# Forti VPN role

Create an IPsec Tunnel with every necessary object and setting that it entails.

### Functionality

Each object that is created by the script will be identifiable by a name prefix with a value of the 'tunnel_name' input parameter, and a comment appendix with a value of 'Created by Ansible'

**1. Check if every required input parameter is present**

**2. Lock the adom**
    - It will be unlocked even if an error occurs during execution.

**3. Firewall object creation**
    - If the 'local_address_group' input string is provided, then the existing Address Group with that name will be used later on for local addresses and the 'local_subnets' input list will be ignored. No objects for local addresses and address groups will be created. If the 'local_address_group' input is not provided, then the 'local_subnets' input list must have at least one item which will create an Address object for each item, and after that, it will create an Address Group with the previosly created Address objects.
    - It is presumed that there are no Address and Address Group objects created for the remote side, so there is no option to provide a remote address group name. You must provide a list with at least one item under the 'remote_subnets' input parameter, and the script will create an Address object for each item, and after that, it will create an Address Group with the previously created Address objects.    

**4. Firewall policy creation**
    - Merge together the source and destination input interface list and use this merged list for both source and destination interfaces in the firewall policy.
    - Merge together the local and remote address group objects into a list and use that merged list for both source and destination addresses in the firewall policy.

**5. IPsec Phase 1**

**6. IPsec Phase 2**

**7. Static Routes**
    - Create a static route for each 'remote_subnets' list item as destination and the IPsec phase 1 name as device.

**8. Commit changes**
    - Without commiting, nothing will be persisted.

**9. Unlock the adom**
    - It will be unlocked even if an error occurs during any previos task execution.

### Input variables

| Parameter | Type | Flags | Default | Description |
| --- | --- | --- | --- | --- |
| adom | string | required | | The name of the ADOM to lock and work in. |
| forti_device | string | required | | The Forti Device the VDOM to work on is present on. |
| vdom | string | required | | The name of the VDOM on the specified Forti Device to work on. |
| tunnel_name | string | required | | Unique name to identify and group resources to be created. |
| firewall_policy_service_list | list of strings | required | | A list of services to be used in the firewall policy the script will create. |
| source_interface_list | list of strings | required | | A list of interface names to be used in the rules as source interfaces. This list will be merged with the dest_interface_list list and the merged list will be used as both source and destination interface in the rule the script will create. |
| dest_interface_list | list of strings | required | | A list of interface names to be used in the rules as destination interfaces. This list will be merged with the source_interface_list list and the merged list will be used as both source and destination interface in the rule the script will create. |
| phase1_local_interface | string | required | | The local interface name that will be used in the phase 1 section. |
| phase1_remote_gateway | string | required | | The remote gateway address that will be used in the phase 1 section. |
| phase1_psksecret | string | required | | The pre-shared key that will be used in the phase 1 section. |
| remote_subnets | list of strings | required | | The remote subnets to be created as Firewall Address objects. An Address Group of these Address objects will be created. |
| local_subnets | list of strings | optional | | The local subnets to be created as Firewall Address objects. Required if local_address_group input variable is not present. This list will only only be considered if local_address_group is not present, and then a new Address Group object will be created containing this list of Address objects. |
| local_address_group | string | optional | | The already present Address Group object that will be used later on as local addresses. If this field is not provided, then the 'local_subnets' input list must be present with at least 1 item. |
| policy_pkg | string | optional | ${vdom} | The policy package to use in the firewall section. If not provided, the VDOM name will be used as it is presumed that the package name is set to the related VDOM. |
| phase1_proposal | list of strings | optional | ['aes256-sha256'] | The proposal to be used in Phase 1. This defaults to a single item list with the value of 'aes256-sha256'. |
| phase2_proposal | list of strings | optional | ['aes256-sha256'] | The proposal to be used in Phase 2. This defaults to a single item list with the value of 'aes256-sha256'. |
| phase1_auto_negotiate | string of 'enable', 'disable' | optional | 'enable' | Auto-negotiation flag in Phase 1. |
| phase2_auto_negotiate | string of 'enable', 'disable' | optional | 'enable' | Auto-negotiation flag in Phase 2. |
| phase1_dhgrp | list of strings from '1', '2', '5', '14', '15', '16', '17', '18', '19', '20', '21', '27', '28', '29', '30', '31', '32' | optional | ['16'] | The DH groups to be used in Phase 1. Defaults to a single item list with a value of '16'. |
| phase2_dhgrp | list of strings from '1', '2', '5', '14', '15', '16', '17', '18', '19', '20', '21', '27', '28', '29', '30', '31', '32' | optional | ['16'] | The DH groups to be used in Phase 2. Defaults to a single item list with a value of '16'. |
| phase1_ike_version | string of '1', '2' | optinal | '2' | The ike version to be used in Phase 1. Defaults to 2. |
comment | string | optional | | A comment that will be put into each object the script creates. A static 'Created by Ansible' string will always be appended in the objects' comment section. |

