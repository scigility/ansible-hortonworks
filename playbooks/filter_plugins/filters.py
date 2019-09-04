from ansible.errors import AnsibleError

# TODO can we access the inventory groups globally, so not to require it as a function ARG ?!

def get_groups(blueprint_dict, groups, services_list):
    if blueprint_dict is None:
        raise AnsibleError('blueprint_dict not defined')
    if groups is None:
        raise AnsibleError('groups not defined')
    if services_list is None:
        raise AnsibleError('services_list not defined')
    #print "get_groups() blueprint_dict={}".format(blueprint_dict)
    #print "get_groups() services_list={}".format(services_list)

    groups_matched = []
    for item in blueprint_dict:
        group_id = item['host_group']
        #print "  get_groups group_id={}".format(group_id)
        if group_id in groups  and len(groups[group_id]) > 0 and len(intersection(services_list, item['services']) ) > 0 :
            groups_matched.append(group_id)
    return groups_matched


def get_hosts(blueprint_dict, groups, services_list):
    group_ids = get_groups(blueprint_dict, groups, services_list)
    return group_hosts(groups, group_ids)


# collect all hosts in the groups defined by the given group_ids
def group_hosts(groups, group_ids):
    #print "  group_hosts group_ids:"+str(group_ids)

    # use a set to avoid duplicates
    group_hosts = set()
    for group_id in group_ids:
        #print "  group_hosts group_id={}".format(group_id)
        #print "  group_hosts groups for group_id={}: {}".format(group_id, groups[group_id])
        group_hosts.update( groups[group_id] )

    return list(group_hosts)


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

class FilterModule(object):
    ''' Blueprint Filter Desc section '''

    def filters(self):
        return {
            'get_groups': get_groups,
            'get_hosts': get_hosts,
            'group_hosts': group_hosts
    }
