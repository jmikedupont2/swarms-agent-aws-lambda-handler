#!/usr/bin/env python3
import os

from aws_cdk import App, Environment
from boto3 import client

from cdk.service.service_stack import CreateAgentApiStack

account = client('sts').get_caller_identity()['Account']
region = 'us-east-1'  # session.Session().region_name
environment = os.getenv('ENVIRONMENT', 'dev')
app = App()

swarms_stack = CreateAgentApiStack(
    scope=app,
    #    id=get_stack_name(),
    construct_id='swarms',
    env=Environment(account=os.environ.get('AWS_DEFAULT_ACCOUNT', account), region=os.environ.get('AWS_DEFAULT_REGION', region)),
    #   is_production_env=True if environment == 'production' else False,
)

# my_stack = ServiceStack(
#     scope=app,
#     id=get_stack_name(),
#     env=Environment(account=os.environ.get('AWS_DEFAULT_ACCOUNT', account), region=os.environ.get('AWS_DEFAULT_REGION', region)),
#     is_production_env=True if environment == 'production' else False,
# )

app.synth()
