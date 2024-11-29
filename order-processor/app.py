from flask import Flask, request, jsonify
from cloudevents.http import from_http
import json
import os
import time

app = Flask(__name__)

app_port = os.getenv('APP_PORT', '6002')

# Register Dapr pub/sub subscriptions
@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{
        'pubsubname': 'orderpubsub',
        'topic': 'orders',
        'route': 'orders'
    }]
    print('Dapr pub/sub is subscribed to: ' + json.dumps(subscriptions))
    return jsonify(subscriptions)


# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/orders', methods=['POST'])
def orders_subscriber():
    event = from_http(request.headers, request.get_data())
    print('Subscriber received : %s' % event.data['orderId'], flush=True)

    steps = 0

    while steps < 100:
        print('Order %s processing step: %s' % (event.data['orderId'], steps), flush=True)
        steps = steps + 1
        time.sleep(1)

    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}


app.run(port=app_port)
