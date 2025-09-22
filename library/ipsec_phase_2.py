from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

def main():
    module_args = {
        'device': {'required': True, 'type': 'str'},
        'vdom': {'required': True, 'type': 'str'},
        'vpn_ipsec_phase2': {
            'type': 'dict',
            'required': True,
            'options': {
                'name': {'required': True, 'type': 'str'},
                'phase1name': {'required': True, 'type': 'str'},
                'src-name': {'required': True, 'type': 'str'},
                'dst-name': {'required': True, 'type': 'str'},
                'proposal': {'required': False, 'type': 'list', 'default': ['aes256-sha256']},
                'auto-negotiate': {'required': False, 'type': 'str', 'choices': ['enable', 'disable'], 'default': 'enable'},
                'dhgrp': {'required': False, 'type': 'list', 'choices': ['1', '2', '5', '14', '15', '16', '17', '18', '19', '20', '21', '27', '28', '29', '30', '31', '32'], 'default': ['16']},
            }
        },
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not module._socket_path:
        module.fail_json(msg='MUST RUN IN HTTPAPI MODE')

    connection = Connection(module._socket_path)

    device = module.params["device"]
    vdom = module.params["vdom"]
    data = module.params["vpn_ipsec_phase2"]
    url = f'pm/config/device/{device}/vdom/{vdom}/vpn/ipsec/phase2-interface'

    proposal = data["proposal"]
    allowed_proposal = ['aes128-sha256','aes128-sha512','aes256-sha256','aes256-sha512']
    proposal = [p.lower() for p in proposal]
    proposal = list(set(proposal))
    if len(proposal) == 0:
        module.fail_json(msg=f"At least one value is required for proposal. Allowed values are: {allowed_proposal}")
    invalid_proposal = [p for p in proposal if p not in allowed_proposal]
    if invalid_proposal:
        module.fail_json(msg=f"Invalid proposal value(s): {invalid_proposal}. Allowed values are: {allowed_proposal}")
    data["proposal"] = proposal

    if len(data["dhgrp"]) == 0:
        module.fail_json(msg=f"At least one value is required for dhgrp.")

    data['src-addr-type'] = 3
    data['dst-addr-type'] = 3

    params = [{
        'url': url,
        'data': data
    }]

    response_raw = connection.send_request("add", params)
    if not response_raw:
        module.fail_json(msg="No response from FortiManager. Check connection or API formatting.")

    if (not isinstance(response_raw, list) and not isinstance(response_raw, tuple)) or len(response_raw) < 2:
        module.fail_json(msg="Unexpected FortiManager response", response=response_raw)

    response_obj = response_raw[1]
    response_data = response_obj.get('data', {})
    response_status = response_obj.get('status')
    response_status_code = response_status.get('code')
    response_status_message = response_status.get('message')
    request_url = response_obj.get('url', url)

    if response_status_code < 0:
        module.fail_json(msg=f"FortiManager API error {response_status_code}: {response_status_message}")

    module.exit_json(
        rc = response_status_code,
        meta={
            'request_url': request_url,
            'response_code': response_status_code,
            'response_data': response_data,
            'response_message': response_status_message,
        }
    )


if __name__ == '__main__':
    main()