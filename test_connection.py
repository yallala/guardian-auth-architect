import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# Let's print what we are sending (without showing the full secret key)
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

print(f"Connecting to: {endpoint}")
print(f"Using Deployment: {deployment}")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=endpoint
)

try:
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("\n✅ SUCCESS! Response received:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\n❌ STILL ERROR: {e}")