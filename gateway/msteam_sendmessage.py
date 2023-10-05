import requests
import json

def send_teams_notification(webhook_url,subject, body):
    try:
        payload = {
            '@type': 'MessageCard',
            '@context': 'http://schema.org/extensions',
            'themeColor': '0072C6',
            'title': subject,
            'text': body,
            'summary': body,
            'sections': [
                {
                    'activityTitle': subject,
                    'activitySubtitle': 'OPENAI-GATEWAY'
                }
            ]
        }
        
        # Send a POST request to the webhook URL with the message payload
        response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(f"Message sent: {response.text}")
        else:
            print(f"Error sending message: {response.text}")
    
    except Exception as ex:
        print(f"Something went wrong when sending teams notifications... {str(ex)}")

# Example usage
#send_teams_notification("Title for the message", "Sample text")
