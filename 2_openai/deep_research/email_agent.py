import os
import asyncio
from typing import Annotated
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from agents import Agent, function_tool, Runner

# Load environment variables
load_dotenv()

# 1. Function: send_email
@function_tool
def send_email(
    subject: Annotated[str, "The subject line of the email"],
    body: Annotated[str, "The HTML content of the email"]
) -> bool:
    """
    Send an email with the given subject and HTML body.
    """
    api_key = os.environ.get("SENDGRID_API_KEY")
    if not api_key:
        print("Error: SENDGRID_API_KEY not found in environment.")
        return False

    message = Mail(
        from_email='a.thomas.kurian@gmail.com',
        to_emails='a.thomas.kurian@gmail.com',
        subject=subject,
        html_content=body
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print(f"Email sent successfully! Status Code: {response.status_code}")
            return True
        else:
            print(f"Failed to send email. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# 2. Agent: email_agent
INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="email_agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)

async def main():
    # Test the agent if run directly
    print("Testing email_agent with a sample report...")
    report = "The research shows that AI is growing fast. It is being adopted in many industries including healthcare and finance."
    
    # Run the agent using Runner from openai-agents
    result = await Runner.run(email_agent, f"Send an email with this report: {report}")
    print(f"Final output: {result.final_output}")

if __name__ == "__main__":
    # Test send_email directly first
    # send_email("Test Subject", "<h1>Test Body</h1>")
    
    # Run the full agent test
    asyncio.run(main())
