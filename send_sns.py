#!/usr/bin/env python

# This python script allows any application to send sns alerts to any topic
# Make sure you create the topic though!
# Usage: printf <msg> | sms_notify.py <topic name> <subject>(optional, ignored if sms)

import boto
import sys
import logging

def send_sms(topic,msg,sub):
    # Enter your credentials here. Use a SNS restricted accout for security :)
    sns = boto.connect_sns("<ACCESS_KEY>","<AWS_SECRET>")
    
    arn = ""
    for topics in sns.get_all_topics()["ListTopicsResponse"]["ListTopicsResult"]["Topics"]:
        if topic in topics["TopicArn"]:
            arn = topics["TopicArn"]
        
    if arn == "":
        logging.error("topic not found!")
        exit(0)
    
    if "sms" in arn:
        sub = ""
    
    response = sns.publish(arn,msg,sub)
    print response
    
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        logging.error("Invalid number of argumennts.Usage: printf <msg> | sms_notify.py <topic name> <subject>(optional, ignored if sms)")
        exit(0)
    
    msg=""
    
    #message is piped in
    for line in sys.stdin.readlines():
        msg = msg+"\n"+line
    
    topic = sys.argv[1]

    if len(sys.argv) == 3:
        sub = sys.argv[3]
    else:
        sub = ""
    
    send_sms(topic,msg,sub)