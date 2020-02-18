import argparse
import googleapiclient.discovery
import json

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

def main(project, zone='europe-west1-b'):
    compute = googleapiclient.discovery.build('compute', 'v1')
    instances = list_instances(compute, project, zone)
    instances_file = 'instances.json'
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

    args = parser.parse_args()

    main(args.project_id, args.zone)