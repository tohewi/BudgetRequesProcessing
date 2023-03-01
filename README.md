# Budget Request Processing

## Overview
Simple event based Azure Budget upserter using Event Hub as event vehicle. Written in Python v3.10, runs on Azure Function with v2 programming model.

## Background
I have been using primarily PowerShell to write Cloud Automation. As a personal study/education project I wanted to look into using Python and Event based architecture to implement a simple Request Automation solution.

## Functionality
It is assumed that there is a Front End (ITSM portal, IT Budget Tool) that can be used by Solution owners to manage budget of their solution. To be able to se this Budgetin data, there needs to be a method to turn budget into Azure Budget to be able to perform cost management and receive alerts on actual or forecasted overspending.

This demo application has a small Python script to send test events and an Azure Function that is triggered when an event is received. Function then performs Azure Budget upsert per received event.

![image](https://user-images.githubusercontent.com/82122655/222145242-aefda5a9-fdda-4750-be79-d616c7548e28.png)


## Note
This is a tech study, not a production ready solution. It does not do "state transfer" and log events in the way it should. Nor does it send events based on end state of event processing back to triggering program.

