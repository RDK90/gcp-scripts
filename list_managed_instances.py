import argparse
import googleapiclient.discovery
import json

def list_managed_instances(compute, project, zone, instance_group):
    result = compute.instanceGroupManagers().listManagedInstances(
        project=project,
        zone=zone,
        instanceGroupManager=instance_group)
    instances_list = []
    if ['managedInstance'] in result:
        for instance in result['managedInstance']:
            instances_list.append(instance['instance'].rsplit('/',1)[:1])
        return instances_list
    else:
        return result

def main(project, zone, instance_group):
    compute = googleapiclient.discovery.build('compute', 'v1')
    instances = list_managed_instances(compute, project, zone, instance_group)
    instances_file = 'managed_instances.json'
    print('Instances found in {}'.format(instances_file))
    with open(instances_file, 'w+') as instance:
        instance.write(json.dumps(instances, indent=4, sort_keys=True))
        instance.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('zone', help='Zone to list instances in')
    parser.add_argument('instance_group', help='Managed Instance Group')

    args = parser.parse_args()

    main(args.project_id, args.zone, args.instance_group)