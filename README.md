# aws-rds-auto-start-stop
Lambda can be used to stop/start RDS instance.
Pre-requisities:
RDS Instance should have below tags :
Scheduled     : True
ScheduleStart : 06:00 
ScheduleStop  : 08:00 

Post Steps:
After Lambda creation, cloudwatch events should be scheduled to run at ScheduleStart and ScheduleStop time.

Consideration:
As of now, Lambda is not considering maintenance window and backup window. Please put maintenance window and backup window out side of 
stop to start timeframe.
