import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

EVENT_HUB_CONNECTION_STR = "Endpoint=sb://xxxxxxxxxxx.servicebus.windows.net/;SharedAccessKeyName=xxxxxxxxxxx;SharedAccessKey=xxxxxxx"
EVENT_HUB_NAME = "application"

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        test_message = '{"billing_profile_id": "2342345",
                    "subscription_id":"xxxx-xxxx-xxxx-xxxx",
                    "budget_name": "app-1010-monthly",
                    "budget_amount": 25,
                    "budget_time_grain": "Monthly",	
                    "budget_category": "Cost",
                    "currency": "EUR","start_date": "2023-02-01T00:00:00Z","end_date": "2023-12-31T23:59:59Z",
                    "budget_filter_value": "app-1010",
                    "email_addresses": ["foo@example.com", "bar@example.com"]}'
        
        # Add events to the batch.
       
        event_data_batch.add(EventData(test_message))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

asyncio.run(run())
