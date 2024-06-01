# Import necessary modules and functions
import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI


# Section 1: Load Environment Variables
# Load environment variables from .env file
load_dotenv()

# Ensure the OPENAI_API_KEY environment variable is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set")


# Section 2: Set Up Gmail Credentials and Toolkit
# Set up Gmail credentials
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)

# Build API resource service for Gmail
api_resource = build_resource_service(credentials=credentials)

# Initialize Gmail toolkit with the API resource
toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()


# Section 3: Configure OpenAI API Key
# Use the environment variable for the API key
os.environ["OPENAI_API_KEY"] = api_key


# Section 4: Create Prompt and Language Model
# Define instructions for the assistant
instructions = """You are an assistant."""

# Pull the base prompt template
base_prompt = hub.pull("langchain-ai/openai-functions-template")

# Customize the base prompt with specific instructions
prompt = base_prompt.partial(instructions=instructions)

# Initialize the language model with specified temperature
llm = ChatOpenAI(temperature=0)


# Section 5: Create and Configure the Agent
# Create an agent using OpenAI functions and the Gmail toolkit
agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

# Initialize the AgentExecutor with the agent and tools
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=False,  # Set to False to prevent sensitive email information from being displayed
)


# Section 6: Invoke the Agent to Send an Email
# Define the input command to send an email
input_command = {
    "input": "How many emails did I receive today?"
}

# Invoke the agent with the input command
agent_executor.invoke(input_command)