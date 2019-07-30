import boto3
import time
import logging

# Example RDS Instance tags:
# Scheduled     : True
# ScheduleStart : 06:00 UTC
# ScheduleStop  : 08:00 UTC


# Logger settings - CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#define boto3 the connection
rds = boto3.client('rds')

def lambda_handler(event, context):

    print "Check RDS's tags"

    # Get current time
    current_time = time.strftime("%H:%M")

    # Search all the instances which contains scheduled tag
    instances = rds.describe_db_instances()

    stopInstances = []
    startInstances = []
    toShutdown = 0
    toStartup = 0
    isScheduled = 0


    for instance in instances["DBInstances"]:
        tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
        InsStatus = instance["DBInstanceStatus"]
        # Filter all instances that are tagged to start or stop.
        for tag in tags["TagList"]:
			if (tag['Key'] == 'Scheduled' and tag['Value'] =='True'):
				isScheduled = 1
			else:
			    print "Instance is not scheduled for automatic start/stop"
			if (tag['Key'] == 'ScheduleStop'and tag['Value'] == current_time and InsStatus =='available'):
				toShutdown = 1
			else:
			    print "Instance is either not scheduled to stop at this time or not in available state"
			if (tag['Key'] == 'ScheduleStart' and tag['Value'] == current_time and InsStatus == 'stopped'):
				toStartup = 1
			else:
			    print "Instance is either not scheduled to start at this time or not in stopped state"

		# stop instances
        if (isScheduled == 1 and toShutdown == 1):
            stopInstances = instance["DBInstanceIdentifier"]
            rds.stop_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])
            print "Instance " + stopInstances +  " is going to shutdown"
        else:
            print "No rds instances to shutdown."

        # start instances
        if (isScheduled == 1 and toStartup == 1):
            startInstances = instance["DBInstanceIdentifier"]
            rds.start_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])
            print "Instance " + startInstances + " is going to start"
        else:
            print "No rds instances to start."

        #reset variable values
        toShutdown = 0
        toStartup = 0
        isScheduled = 0
