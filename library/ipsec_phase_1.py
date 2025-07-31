import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortimanager.plugins.module_utils.napi import NAPIManager, check_parameter_bypass
from ansible_collections.fortinet.fortimanager.plugins.module_utils.common import get_module_arg_spec

def main():
    # urls_list = [
    #     'pm/config/device/{device}/vdom/{vdom}/vpn/ipsec/phase1-interface'
    # ]
    # perobject_urls_list = [
    #     'pm/config/device/{device}/vdom/{vdom}/vpn/ipsec/phase1-interface/{phase1-interface}'
    # ]
    # url_params = ['device', 'vdom']
    # module_primary_key = 'name'
    # module_arg_spec = {
    #     'device': {'required': True, 'type': 'str'},
    #     'vdom': {'required': True, 'type': 'str'},
    #     'vpn_ipsec_phase1': {
    #         'type': 'dict',
    #         'options': {
    #             'name': {'required': True, 'type': 'str'},
    #             'interface': {'required': True, 'type': 'str'},
    #             'remote-gw': {'required': True, 'type': 'str'},
    #             'psksecret': {'required': True, 'type': 'str'},
    #             'proposal': {'required': False, 'type': 'str', 'default': 'aes256-sha256'},
    #             'peertype': {'required': False, 'type': 'str', 'default': 'any'},
    #             'net-device': {'required': False, 'type': 'str', 'default': 'disable'},
    #             'dhgrp': {'required': False, 'type': 'str', 'default': '16'},
    #             'ike-version': {'required': False, 'type': 'str', 'default': '2'},
    #             'comments': {'required': False, 'type': 'str'},
    #         }
    #     },
    # }
    # module_option_spec = get_module_arg_spec('full crud')
    # module_arg_spec.update(module_option_spec)
    # params_validation_blob = []
    # module = AnsibleModule(argument_spec=check_parameter_bypass(module_arg_spec, 'vpn_ipsec_phase1'),
    #                        supports_check_mode=True)
    # if not module._socket_path:
    #     module.fail_json(msg='MUST RUN IN HTTPAPI MODE')
    # connection = Connection(module._socket_path)
    # connection.set_option('access_token', module.params.get('access_token', None))
    # connection.set_option('enable_log', module.params.get('enable_log', False))
    # connection.set_option('forticloud_access_token', module.params.get('forticloud_access_token', None))
    # fmgr = NAPIManager(urls_list, perobject_urls_list, module_primary_key, url_params,
    #                    module, connection, top_level_schema_name='data')
    # fmgr.validate_parameters(params_validation_blob)
    # fmgr.process_curd(argument_specs=module_arg_spec)
    
    module_args = {
        'device': {'required': True, 'type': 'str'},
        'vdom': {'required': True, 'type': 'str'},
        'vpn_ipsec_phase1': {
            'type': 'dict',
            'required': True,
            'options': {
                'name': {'required': True, 'type': 'str'},
                'interface': {'required': True, 'type': 'str'},
                'remote-gw': {'required': True, 'type': 'str'},
                'psksecret': {'required': True, 'type': 'str'},
                'proposal': {'required': False, 'type': 'str', 'default': 'aes256-sha256'},
                'peertype': {'required': False, 'type': 'str', 'default': 'any'},
                'net-device': {'required': False, 'type': 'str', 'default': 'disable'},
                'dhgrp': {'required': False, 'type': 'str', 'default': '16'},
                'ike-version': {'required': False, 'type': 'str', 'default': '2'},
                'comments': {'required': False, 'type': 'str'},
            }
        },
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not module._socket_path:
        module.fail_json(msg='MUST RUN IN HTTPAPI MODE')

    connection = Connection(module._socket_path)

    device = module.params["device"]
    vdom = module.params["vdom"]
    data = module.params["vpn_ipsec_phase1"]

    api_body = {
        'method': 'set',
        'params': [{
            'url': f'pm/config/device/{device}/vdom/{vdom}/vpn/ipsec/phase1-interface',
            'data': [data]
        }],
        'id': 1,
    }

    response_raw = connection.send(json.dumps(api_body))
    if not response_raw:
        module.fail_json(msg="No response from FortiManager (empty string). Check connection or API formatting.")

    try:
        response = json.loads(response_raw)
    except json.JSONDecodeError as e:
        module.fail_json(msg=f"Failed to decode FortiManager response: {str(e)}", raw=response_raw)

    module.exit_json(
        changed=True,
        meta={
            "request": api_body,
            "response_data": response,
        }
    )


if __name__ == '__main__':
    main()