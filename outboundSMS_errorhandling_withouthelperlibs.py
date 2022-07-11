#https://www.twilio.com/docs/sms/api/message-resource#create-a-message-resource
import requests
from requests.auth import HTTPBasicAuth
import csv
import datetime
import os
#from twilio.rest import Client

base_url = 'https://api.twilio.com/2010-04-01'
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
from_number = '+12698831507'
message_text = 'Hello Twilio!'
message_api_url = f"{base_url}/Accounts/{account_sid}/Messages.json"

#list of mobile numbers to send sms to
mobile_numbers_list = ['+15719462715','+13649003666', '+13649003644', '+14142965678', '+14144007468']

try:

    new_session = f"Session started at {datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    #open successful_api_call.csv to write when the new session start and the headers, parameters can be used to search in twilio debug logs for errors
    with open(f"successful_api_call.csv", 'a', newline="") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([new_session])
        writer.writerow(["Datetime","To", "From", "Body", "sid"])
    #open request_error_log.csv to do the same as above but to log any errors that happen in the call
    with open(f"request_error_log.csv",'a', newline="") as g:
        request_error_writer = csv.writer(g, delimiter=',')
        request_error_writer.writerow([new_session])
        request_error_writer.writerow(["Datetime","To", "From", "Body", "Error"])
    #for loop to loop through the number and make calls through https request 
    for mobile_number in mobile_numbers_list:
        try:
            #post request
            send_sms_request_request = requests.post(message_api_url, auth=HTTPBasicAuth(account_sid, auth_token), data={"To": mobile_number, "From": from_number ,"Body": message_text})
            send_sms_request_response = send_sms_request_request.json()
            #logging successful call in csv
            with open(f"successful_api_call.csv", 'a', newline="") as h:
                successful_call_writer = csv.writer(h, delimiter=',')
                successful_call_writer.writerow([
                    send_sms_request_response['date_created'],
                    mobile_number,
                    '+12698831507',
                    send_sms_request_response['sid']
                ])
            #printing the sid as needed in the assignment
            print(send_sms_request_response['sid'])
        #handling errors and logging them i the request_error_log.csv
        except Exception as e:
            with open(f"request_error_log.csv",'a', newline="") as i:
                request_error_writer = csv.writer(i, delimiter=',')
                request_error_writer.writerow([datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'),mobile_number,'+12698831507',send_sms_request_request.json()])
                #additional code can be used to handle error here but do not see any error that is safe to retry the request to resend sms
#logging application errors that happen
except Exception as e:
    with open(f"application_error_log.csv",'a', newline="") as j:
        application_error_writer = csv.writer(j, delimiter=',')
        application_error_writer.writerow([datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'), e])