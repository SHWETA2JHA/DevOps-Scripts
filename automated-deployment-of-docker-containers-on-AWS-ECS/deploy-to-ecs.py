import boto3
import json
import sys

def register_task_definition(client, family, container_name, image_uri, memory, cpu):
    """Register a new task definition with ECS."""
    response = client.register_task_definition(
        family=family,
        containerDefinitions=[
            {
                'name': container_name,
                'image': image_uri,
                'memory': memory,
                'cpu': cpu,
                'essential': True,
            }
        ]
    )
    print(f"Task definition registered: {response['taskDefinition']['taskDefinitionArn']}")
    return response['taskDefinition']['taskDefinitionArn']

def update_service(client, cluster, service, task_definition_arn):
    """Update the ECS service to use the new task definition."""
    response = client.update_service(
        cluster=cluster,
        service=service,
        taskDefinition=task_definition_arn
    )
    print(f"Service update initiated: {response['service']['serviceArn']}")

def main():
    if len(sys.argv) != 6:
        print("Usage: python deploy_to_ecs.py <family> <container_name> <image_uri> <memory> <cpu>")
        sys.exit(1)

    # Configuration
    FAMILY = sys.argv[1]
    CONTAINER_NAME = sys.argv[2]
    IMAGE_URI = sys.argv[3]
    MEMORY = int(sys.argv[4])
    CPU = int(sys.argv[5])
    CLUSTER = 'your-cluster-name'
    SERVICE = 'your-service-name'

    ecs_client = boto3.client('ecs')

    # Register new task definition
    task_definition_arn = register_task_definition(
        ecs_client, FAMILY, CONTAINER_NAME, IMAGE_URI, MEMORY, CPU
    )

    # Update ECS service
    update_service(ecs_client, CLUSTER, SERVICE, task_definition_arn)

if __name__ == "__main__":
    main()
