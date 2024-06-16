import json


def read_actions_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def format_terraform_output(actions):
    actions_to_return = {}
    for action in actions:
        prefix, action_name = action.split(':', 1)
        if prefix not in actions_to_return:
            actions_to_return[prefix] = {}
            actions_to_return[prefix]["AllActions"] = f"{prefix}:*"
        actions_to_return[prefix][action_name] = action

    return actions_to_return


def generate_terraform_file(service_actions):
    with open('outputs.tf', 'w') as file:
        file.write('output "effects" {\n')
        file.write('  description = "All effects allowed in an AWS Policy"\n')
        file.write('  value       = {\n')
        file.write('    Allow = "Allow"\n')
        file.write('    Deny  = "Deny"\n')
        file.write('  }\n')
        file.write('}\n\n')
        file.write('output "actions" {\n')
        file.write('  description = "An object with all AWS policy actions separated by service"\n')
        file.write('  value       = {\n')
        for service, actions in service_actions.items():
            file.write(f'    {service} = {{\n')
            for action_name, full_action in actions.items():
                file.write(f'      {action_name} = "{full_action}"\n')
            file.write('    }\n')
        file.write('  }\n')
        file.write('}\n')


if __name__ == "__main__":
    json_actions = read_actions_from_json('aws-iam-actions.json')
    formatted_actions = format_terraform_output(json_actions)
    generate_terraform_file(formatted_actions)
