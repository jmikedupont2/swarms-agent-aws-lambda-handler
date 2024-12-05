# import os

from aws_cdk import Aspects, CfnOutput, Duration, Stack, Tags
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda  # Stack,
from cdk_nag import AwsSolutionsChecks, NagSuppressions
from constructs import Construct

from cdk.service.api_construct import ApiConstruct
from cdk.service.configuration.configuration_construct import ConfigurationStore
from cdk.service.constants import CONFIGURATION_NAME, ENVIRONMENT, OWNER_TAG, SERVICE_NAME, SERVICE_NAME_TAG
from cdk.service.utils import get_construct_name, get_username


class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, is_production_env: bool, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._add_stack_tags()

        # This construct should be deployed in a different repo and have its own pipeline so updates can be decoupled
        # from running the service pipeline and without redeploying the service lambdas. For the sake of this blueprint
        # example, it is deployed as part of the service stack
        self.dynamic_configuration = ConfigurationStore(
            self,
            get_construct_name(stack_prefix=id, construct_name='DynamicConf'),
            ENVIRONMENT,
            SERVICE_NAME,
            CONFIGURATION_NAME,
        )
        self.api = ApiConstruct(
            self,
            get_construct_name(stack_prefix=id, construct_name='Crud'),
            self.dynamic_configuration.app_name,
            is_production_env=is_production_env,
        )

        # add security check
        self._add_security_tests()

    def _add_stack_tags(self) -> None:
        # best practice to help identify resources in the console
        Tags.of(self).add(SERVICE_NAME_TAG, SERVICE_NAME)
        Tags.of(self).add(OWNER_TAG, get_username())

    def _add_security_tests(self) -> None:
        Aspects.of(self).add(AwsSolutionsChecks(verbose=True))
        # Suppress a specific rule for this resource
        NagSuppressions.add_stack_suppressions(
            self,
            [
                {'id': 'AwsSolutions-IAM4', 'reason': 'policy for cloudwatch logs.'},
                {'id': 'AwsSolutions-IAM5', 'reason': 'policy for cloudwatch logs.'},
                {'id': 'AwsSolutions-APIG2', 'reason': 'lambda does input validation'},
                {'id': 'AwsSolutions-APIG1', 'reason': 'not mandatory in a sample blueprint'},
                {'id': 'AwsSolutions-APIG3', 'reason': 'not mandatory in a sample blueprint'},
                {'id': 'AwsSolutions-APIG6', 'reason': 'not mandatory in a sample blueprint'},
                {'id': 'AwsSolutions-APIG4', 'reason': 'authorization not mandatory in a sample blueprint'},
                {'id': 'AwsSolutions-COG4', 'reason': 'not using cognito'},
                {'id': 'AwsSolutions-L1', 'reason': 'False positive'},
            ],
        )


class CreateAgentApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # agent_lambda = _lambda.DockerImageFunction(
        #     self,
        #     'aiResearchAgent',
        #     code=_lambda.DockerImageCode.from_image_asset('./lambdas/swarms'),
        #     memory_size=1024 * 2,
        #     timeout=Duration.seconds(90),
        #     architecture=_lambda.Architecture.X86_64,
        #     #            environment={'OPENAI_API_KEY': os.environ['OPENAI_API_KEY']},
        #     description='Generic Agent',
        # )

        swarms_lambda = _lambda.DockerImageFunction(
            self,
            'swarmsAgent',
            code=_lambda.DockerImageCode.from_image_asset('./lambdas/swarms'),
            memory_size=1024 * 8,
            timeout=Duration.seconds(90),
            architecture=_lambda.Architecture.X86_64,
            #            environment={'OPENAI_API_KEY': os.environ['OPENAI_API_KEY']},
            description='Swarms Agent',
        )

        # Create REST API Gateway
        api = apigw.RestApi(self, 'AgentApi', rest_api_name='Agent Service API', description='API for the AI Agent service')

        # Create API Gateway integrations
        #        agent_integration = apigw.LambdaIntegration(agent_lambda)
        swarms_integration = apigw.LambdaIntegration(swarms_lambda)

        # Add resources and POST methods
        #        agent_resource = api.root.add_resource('agent')
        #        agent_resource.add_method('POST', agent_integration)

        swarms_resource = api.root.add_resource('swarms')
        swarms_resource.add_method('POST', swarms_integration)

        # Output the API URL
        CfnOutput(self, 'ApiUrl', value=api.url, description='URL of the API Gateway endpoint')
