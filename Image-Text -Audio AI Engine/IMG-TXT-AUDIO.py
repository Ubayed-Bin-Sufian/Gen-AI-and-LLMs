# Import necessary libraries
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from transformers import pipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# Load environment variables from a .env file
load_dotenv()

# Function to convert image to text using HuggingFace's image-to-text model
def img2text(url):
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(url)[0]['generated_text']
    print(text)
    return text

# Function to generate a short story based on a given scenario using OpenAI's GPT model
def generate_story(scenario):
    template = """
    You are a storyteller. You can generate a short story based on a simple narrative. The story should be no more than 200 words;
    CONTEXT: {scenario}
    STORY:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["scenario"])
    story_llm = LLMChain(
        llm=ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=1, openai_api_key=os.getenv("OPENAI_API_KEY")
        ),
        prompt=prompt,
        verbose=True,
    )
    
    story = story_llm.predict(scenario=scenario)
    print(story)
    return story

# Function to convert text to speech using HuggingFace's TTS model
def text2speech(message):
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACEHUB_API_TOKEN')}"}
    payloads = {
        "inputs": message
    }

    response = requests.post(API_URL, headers=headers, json=payloads)

    # Save the audio response to a file
    with open("audio.flac", "wb") as file:
        file.write(response.content)

# Main Streamlit app function
def main():
    st.set_page_config(page_title="Image to Audio Story", page_icon="🎨")
    st.header("Turn Image into Audio Story")

    # Upload image file
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()

        # Save uploaded file locally
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)

        # Display uploaded image
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

        # Convert image to text (scenario)
        scenario = img2text(uploaded_file.name)

        # Generate story from scenario
        story = generate_story(scenario)

        # Convert story to speech
        text2speech(story)

        # Display scenario and story with audio
        with st.expander("Scenario"):
            st.write(scenario)
        with st.expander("Story"):
            st.write(story)
        st.audio("audio.flac")

# Run the main function
if __name__ == "__main__":
    main()
