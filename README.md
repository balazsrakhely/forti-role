# Forti VPN role

Input variables:

tunnel_name | string | required | Unique name to identify and group resources to be created
local_subnets | list of strings | required | The local subnets to be created as Firewall Address objects.
remote_subnets | list of strings | required | The remote subnets to be created as Firewall Address objects.