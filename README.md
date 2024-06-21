# Spaced Repetition Learning System

## Overview

This project implements a spaced repetition learning system using Google Cloud Platform (GCP) services. It automatically selects a daily topic for study from a CSV file, updates the study schedule, and sends an email notification with the day's topic.

## Features

- Daily topic selection based on spaced repetition algorithm
- Automatic email notifications with the day's topic
- Cloud-based storage of study materials and progress
- Automated deployment and scheduling using GitHub Actions

## Technologies Used

- Python 3.9
- Google Cloud Functions
- Google Cloud Storage
- Google Cloud Scheduler
- SendGrid for email notifications
- GitHub Actions for CI/CD

## Setup

### Prerequisites

1. A Google Cloud Platform account with billing enabled
2. A GitHub account
3. A SendGrid account for sending emails

### Google Cloud Platform Setup

1. Create a new GCP project or select an existing one
2. Enable the following APIs in your GCP project:
   - Cloud Functions API
   - Cloud Scheduler API
   - Cloud Storage API
   - Artifact Registry API
3. Create a service account with the following roles:
   - Cloud Functions Developer
   - Service Account User
   - Artifact Registry Writer
   - Pub/Sub Editor
   - Cloud Scheduler Admin
4. Generate and download a JSON key for this service account

### GitHub Repository Setup

1. Fork or clone this repository to your GitHub account
2. Go to your repository's Settings > Secrets and variables > Actions
3. Add the following secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: The content of the JSON key file for your service account
   - `SENDGRID_API_KEY`: Your SendGrid API key

### Local Development Setup

1. Clone the repository to your local machine
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `ML_Topics - Revisions.csv` file with your study topics

## Deployment

The project is set up to automatically deploy to Google Cloud Functions whenever changes are pushed to the main branch. The deployment process is managed by the GitHub Actions workflow defined in `.github/workflows/deploy.yml`.

To trigger a deployment:

1. Make your changes to the code
2. Commit and push to the main branch
3. GitHub Actions will automatically deploy the function and set up the Cloud Scheduler

## Usage

Once deployed, the system will automatically:

1. Select a topic daily based on the spaced repetition algorithm
2. Update the CSV file in Google Cloud Storage with the new study schedule
3. Send an email to your specified address with the day's topic

You don't need to manually trigger anything - the Cloud Scheduler will run the function daily at the specified time (default is 8:00 AM).

## Customization

- To change the email scheduling time, modify the cron expression in the `deploy.yml` file
- To adjust the spaced repetition algorithm, modify the `select_topic_and_send_email` function in `main.py`

## Troubleshooting

If you encounter issues during deployment:

1. Check the GitHub Actions logs for detailed error messages
2. Ensure all required APIs are enabled in your GCP project
3. Verify that the service account has the necessary permissions
4. Check that all required secrets are correctly set in your GitHub repository

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a new Pull Request
