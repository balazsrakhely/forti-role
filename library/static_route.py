from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

def main():
    module_args = {
        'device': {'required': True, 'type': 'str'},
        'vdom': {'required': True, 'type': 'str'},
        'router_static': {
            'type': 'dict',
            'required': True,
            'options': {
                'dst': {'required': True, 'type': 'list'},
                'device': {'required': True, 'type': 'str'},
                'comment': {'required': False, 'type': 'str'},
            }
        },
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not module._socket_path:
        module.fail_json(msg='MUST RUN IN HTTPAPI MODE')

    connection = Connection(module._socket_path)

    device = module.params["device"]
    vdom = module.params["vdom"]
    data = module.params["router_static"]
    url = f'pm/config/device/{device}/vdom/{vdom}/router/static'

    params = [{
        'url': url,
        'data': data
    }]

    response_raw = connection.send_request("set", params)
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