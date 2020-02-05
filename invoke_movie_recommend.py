import logging
logger = logging.getLogger('dt')
logger.setLevel(logging.DEBUG)
import json
import boto3

class RunTask:
    def __init__(self):
        pass
    def run_task(self, container_overrides, task_definition_arn, cluster_name="MovieRecommend", run_count=10):
        ecs_client = boto3.client('ecs')
        result = ecs_client.run_task(
            cluster=cluster_name,
            taskDefinition=task_definition_arn,
            overrides={
                'containerOverrides': container_overrides
            },
            count=run_count,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        "subnet-0180624149acf31e2",
                        "subnet-0180624149acf31e2"
                    ],
                    'securityGroups': [
                        "sg-0d6ff5a21e30ab387"
                    ],
                    'assignPublicIp': 'ENABLED'
                }
            }
        )
        return result
    def get_container_overrides(self):
        container_overrides_input = {}
        container_overrides_input["result"] = [
            {
                "name": "movierecommend",
                "command": [
                    "python",
                    "movie_recommend.py"

                ]
            }
        ]

        return container_overrides_input.get("result")

    def main(self, event, context):

        task_definition_arn = event.get("task_definition_arn", "arn:aws:ecs:ap-northeast-2:249842155296:task-definition/movieRecommendTask:1")
        cluster_name = event.get("cluster_name", "MovieRecommend")

        logger.info("task_definition_arn : %s", task_definition_arn)
        logger.info("cluster_name : %s", cluster_name)

        container_overrides_input = self.get_container_overrides()
        if not container_overrides_input:
            return {"result": "Error", "message": "Invalid Parameters"}
        logger.info("[container_overrides_input] %s", json.dumps(container_overrides_input))
        response = self.run_task(
            container_overrides=container_overrides_input,
            run_count=1,
            task_definition_arn=task_definition_arn,
            cluster_name=cluster_name
        )
        result = {}
        result["result"] = "OK"
        result["tasks_count"] = len(response["tasks"])
        result["failures_count"] = len(response["failures"])
        return result


def run(event, context):
    logger.info("[event] %s", json.dumps(event))
    obj = RunTask()
    result = obj.main(event, context)
    response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(result)
        }

    return response


if __name__ == '__main__':
    param = {}
    # param = {
    #     "payload": {
    #         "task_definition_arn": "arn:aws:ecs:ap-northeast-2:412412730148:task-definition/MatsScoreMakerTask:1",
    #         "cluster_name": "MatsScoreMakerCluster",
    #         "run_count": 2,
    #         "analysis_type": "taste"
    #     }
    # }
    param = {
        "payload": {

        }
    }

    run({}, [])