from dapr.clients import DaprClient
import json
import time
import logging
import uuid

logging.basicConfig(level=logging.INFO)

with DaprClient() as client:
    # for i in range(1, 10):
    logging.info('Publishing only 1 heavy order')

    order = {'orderId': str(uuid.uuid4())}
    # Publish an event/message using Dapr PubSub
    result = client.publish_event(
        pubsub_name='orderpubsub',
        topic_name='orders',
        data=json.dumps(order),
        data_content_type='application/json',
    )
    logging.info('Published data: ' + json.dumps(order))
    # time.sleep(1)
