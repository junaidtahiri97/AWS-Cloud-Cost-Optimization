import boto3
import json

def lambda_handler(event, context):

    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Retrieve all EBS snapshots owned by the account
    snapshots_response = ec2.describe_snapshots(OwnerIds=['self'])
    snapshots = snapshots_response['Snapshots']

    # Retrieve active EC2 instance IDs
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = {instance['InstanceId'] for reservation in instances_response['Reservations'] for instance in reservation['Instances']}

    # Iterate through each snapshot
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Delete the snapshot if it's not attached to any volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume.")
        elif volume_id not in active_instance_ids:
            # Delete the snapshot if the volume is not attached to a running instance
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")

if __name__ == "__main__":
    delete_stale_snapshots()
