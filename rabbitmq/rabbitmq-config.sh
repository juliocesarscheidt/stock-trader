#!/bin/bash

sleep 10

while true; do
  sleep 5
  rabbitmq-diagnostics -q ping > /dev/null 2>&1
  test $? == 0 && break
done

rabbitmqctl add_user dev dev

rabbitmqctl set_user_tags dev administrator
rabbitmqctl set_permissions -p / dev ".*" ".*" ".*"
rabbitmqctl set_permissions -p / guest ".*" ".*" ".*"

# setup
rabbitmqadmin declare --vhost=/ queue name=stocks_queue auto_delete=false durable=true
rabbitmqadmin declare exchange name=stocks_queue_exchange type=direct auto_delete=false durable=true
rabbitmqadmin declare binding source=stocks_queue_exchange destination=stocks_queue routing_key="stocks_queue" destination_type=queue
