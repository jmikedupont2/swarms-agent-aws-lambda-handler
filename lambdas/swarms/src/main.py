# import os
import json
import logging

from swarms import Agent

logger = logging.getLogger()
logger.setLevel(logging.INFO)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT)


def handler(event, context):
    try:
        logger.info(f'Event: {event}')
        body = json.loads(event['body'])

        agent = Agent(agent_name='you are a helpful assistant', model_name='gpt-4o-mini')

        response = agent.run(body['question'])

        return {'statusCode': 200, 'body': response}

    except ValueError as e:
        logger.error(f'Validation error: {str(e)}')
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)}),
        }
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Internal server error'}),
        }
