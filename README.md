# Python EC2 GitHub Actions

This project is designed to send scheduled notifications to a Mattermost channel using a Python script. It utilizes the APScheduler library to manage the scheduling of messages and is set up to be deployed on an AWS EC2 instance using GitHub Actions.

## Project Structure

```
python-ec2-github-actions
├── src
│   └── main.py          # Contains the main logic for sending messages and scheduling notifications
├── .github
│   └── workflows
│       └── deploy.yml   # GitHub Actions workflow for deploying the application to AWS EC2
├── requirements.txt      # Lists the required Python dependencies
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/python-ec2-github-actions.git
   cd python-ec2-github-actions
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS EC2**
   - Set up an AWS EC2 instance.
   - Ensure that the instance has access to the internet and the necessary permissions to send requests to the Mattermost webhook.

4. **Set Up GitHub Actions**
   - Create a GitHub repository and push your code.
   - Configure the `deploy.yml` file in the `.github/workflows` directory with your AWS credentials and instance details.

## Usage

- Modify the `src/main.py` file to customize the messages and scheduling times as needed.
- Once the GitHub Actions workflow is set up, any push to the main branch will trigger the deployment to your AWS EC2 instance.

## License

This project is licensed under the MIT License - see the LICENSE file for details.