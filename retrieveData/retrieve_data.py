import boto3
import json

orgs = boto3.client('organizations')

def get_children(node_id):
    account_children = orgs.list_children(ParentId=node_id, ChildType='ACCOUNT')
    orgs_children = orgs.list_children(ParentId=node_id, ChildType='ORGANIZATIONAL_UNIT')
    return account_children['Children'] + orgs_children['Children']

def get_ou_name(ou_id):
    ou_name = orgs.describe_organizational_unit(
    OrganizationalUnitId=ou_id
    )
    return ou_name['OrganizationalUnit']['Name']

def get_account_name(account_id):
    account_name = orgs.describe_account(
        AccountId=account_id
    )
    return account_name['Account']['Name']

def get_tags(resource_id):
    tags = orgs.list_tags_for_resource(
        ResourceId=resource_id
    )
    return tags['Tags']

def draw_nodes(node, node_id, inherited_policies):
    children = get_children(node_id)

    # print(node_id)
    # print(children)
    for child in children:
        child['SCPs'] = get_policies(child['Id'], 'SERVICE_CONTROL_POLICY')
        child['Inherited'] = inherited_policies
        child['Tags'] = get_tags(child['Id'])
        child['parentNodeId'] = node_id
        if child['Type'] == 'ORGANIZATIONAL_UNIT':
            child['Name'] = get_ou_name(child['Id'])
            draw_nodes(child, child['Id'], inherited_policies + child['SCPs'])
        else:
            child['Name'] = get_account_name(child['Id'])
        if 'children' not in node:
            node['children'] = []
        node['children'].append(child)
    return node

def get_policies(target_id, policy_type):
    policies = orgs.list_policies_for_target(
        TargetId = target_id,
        Filter = policy_type
    )
    return  policies['Policies']


def get_root():
    # accounts = orgs.list_accounts()

    # print(accounts)
    root_node = {}
    root = orgs.list_roots()
    root_node['nodeId'] = root['Roots'][0]['Id']
    root_node['Type'] = 'ORGANIZATIONAL_UNIT'
    root_node['Name'] = 'Root'
    root_node['children'] = []
    root_node['parentNodeId'] = None
    root_node['SCPS'] = get_policies(root['Roots'][0]['Id'], 'SERVICE_CONTROL_POLICY')
    root_node['Tags'] = get_tags(root['Roots'][0]['Id'])
    return draw_nodes(root_node, root['Roots'][0]['Id'],root_node['SCPS'])

def main():
    nodes = get_root()
    with open('../website/orgs_data.json', 'w') as f:
        json.dump(nodes, f)

main()