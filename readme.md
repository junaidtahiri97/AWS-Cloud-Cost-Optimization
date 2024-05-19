
**AWS Cost Optimization Project**

The project is using a Lambda function to get a list of all active EC2 instances and all EBS snapshots. Then, it verifies that every snapshot's associated volume—if any—isn't connected to any running instances. 
It optimized storage costs by deleting these stale snapshots.
