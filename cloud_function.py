import pandas as pd
from datetime import timedelta
from google.cloud import storage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def select_topic_and_send_email(event, context):
    # Get the GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket('gs://moustafa-ml/')
    blob = bucket.blob('ML_Topics - Revisions.csv')
    
    # Download the CSV file
    blob.download_to_filename('/tmp/ML_Topics - Revisions.csv')
    
    # Load the data
    df = pd.read_csv('/tmp/ML_Topics - Revisions.csv')
    
    # Convert date strings to datetime objects and ensure Practice_Count is int
    df['Last_Practiced'] = pd.to_datetime(df['Last_Practiced'], errors='coerce')
    df['Next_Practice'] = pd.to_datetime(df['Next_Practice'], errors='coerce')
    df['Practice_Count'] = df['Practice_Count'].astype(int)
    
    # Get current date
    today = pd.Timestamp.now().normalize()
    
    # Filter topics that are due for practice
    due_topics = df[df['Next_Practice'].isnull() | (df['Next_Practice'] <= today)]
    
    if due_topics.empty:
        message = "No topics due for practice today. Good job!"
    else:
        # Randomly select a topic
        selected_topic = due_topics.sample(n=1).iloc[0]
        
        # Update practice information
        df.loc[selected_topic.name, 'Last_Practiced'] = today
        df.loc[selected_topic.name, 'Practice_Count'] += 1
        
        # Calculate next practice date
        practice_count = int(df.loc[selected_topic.name, 'Practice_Count'])
        next_practice = today + timedelta(days=max(1, 2 ** (practice_count - 1)))
        df.loc[selected_topic.name, 'Next_Practice'] = next_practice
        
        # Save updated DataFrame
        df.to_csv('/tmp/ML_Topics - Revisions.csv', index=False)
        
        # Upload the updated CSV back to GCS
        blob.upload_from_filename('/tmp/ML_Topics - Revisions.csv')
        
        # Prepare the message
        message = f"""Today's topic for practice:
                    Category: {selected_topic['Category']}
                    Subcategory: {selected_topic['Subcategory']}
                    Topic: {selected_topic['Topic']}
                    Subtopic: {selected_topic['Subtopic']}
                    Details: {selected_topic['Details']}
                    Practice Count: {selected_topic['Practice_Count']}
                    Next practice date: {next_practice.date()}"""

    # Send email
    message = Mail(
        from_email='your-sender-email@example.com',
        to_emails='mosafehashf@gmail.com',
        subject='Your Daily Spaced Repetition Topic',
        html_content=message.replace('\n', '<br>'))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

    return 'Email sent successfully'