import azure.functions as func
from azure.identity import (DefaultAzureCredential)
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.consumption.models import (
    Budget, BudgetFilter, Notification, BudgetFilterProperties,BudgetComparisonExpression)
import json
import logging

app = func.FunctionApp()


@app.function_name(name="EventHubTrigger1")
@app.event_hub_message_trigger(arg_name="myhub", event_hub_name="application",
                               connection="EHNSCONNECTIONSTRING") 
@app.blob_output(arg_name="outputblob",
                path="budget/status.log",
                connection="AzureWebJobsStorage")

def test_function(myhub: func.EventHubEvent, outputblob: func.Out[str]) -> str:
    logging.info('Python EventHub trigger processed an event: %s',
                myhub.get_body().decode('utf-8'))

    try:
        req_body = json.loads(myhub.get_body().decode('utf8').replace("'", '"'))

        logging.info(req_body)

        credential = DefaultAzureCredential()
        
        # Get budget details from request body
        billing_profile_id = req_body['billing_profile_id']
        subscription_id = req_body['subscription_id']
        budget_name = req_body['budget_name']
        budget_amount = req_body['budget_amount']
        budget_time_grain = req_body['budget_time_grain']
        budget_category = req_body['budget_category']
        budget_currency = req_body['currency']
        budget_start_date = req_body['start_date']
        budget_end_date = req_body['end_date']
        budget_filter_value = req_body['budget_filter_value']
        email_addresses = req_body['email_addresses']

        # Connect Consumption Management Api
        consumption_client = ConsumptionManagementClient(
            credential, subscription_id)

        # Check if budget already exists
        budgets = consumption_client.budgets.list(
            "/subscriptions/"+subscription_id+"/")
        existing_budget = next(
            (b for b in budgets if b.name == budget_name), None)

        budget_filter = BudgetFilter(
            and_property = [
                BudgetFilterProperties(tags=BudgetComparisonExpression(name="application",operator="In",values=[budget_filter_value])),
                BudgetFilterProperties(tags=BudgetComparisonExpression(name="environment",operator="In",values=['dev','test','prod']))
            ]
        )

        budget_notification = {
            'actual-95-percent': Notification(
                enabled=True,
                operator="GreaterThan",
                threshold=95,
                contact_emails=email_addresses,
                contact_groups=None,
                threshold_type="Actual",
                locale="en-us"
                ),
            'actual-100-percent': Notification(
                enabled=True,
                operator="GreaterThan",
                threshold=100,
                contact_emails=email_addresses,
                contact_groups=None,
                threshold_type="Actual",
                locale="en-us"
                ),
            'forecast-100-percent': Notification(
                enabled=True,
                operator="GreaterThan",
                threshold=100,
                contact_emails=email_addresses,
                contact_groups=None,
                threshold_type="Forecasted",
                locale="en-us"
                )
            }


        if existing_budget:
            # Update existing budget
            existing_budget.amount = budget_amount
            existing_budget.time_grain = budget_time_grain
            existing_budget.category = budget_category
            existing_budget.filter = budget_filter
            existing_budget.notifications = budget_notification

            consumption_client.budgets.create_or_update("/subscriptions/"+subscription_id+"/", budget_name, existing_budget)
        else:
            # Create new budget
            budget = Budget(
                name=budget_name,
                amount=budget_amount,
                time_grain=budget_time_grain,
                time_period={
                    'start_date': budget_start_date,
                    'end_date': budget_end_date
                },
                category=budget_category,
                filter=budget_filter,
                notifications= budget_notification
            )
            consumption_client.budgets.create_or_update(
                "/subscriptions/"+subscription_id+"/", budget_name, budget)

        outputblob.set(f"Budget {budget_name} created or updated successfully.")
      
    except Exception as e:
        outputblob.set(f"Error creating or updating budget: {str(e)}")
