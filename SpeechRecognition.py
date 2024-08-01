import os
import io
import speech_recognition as sr
from google.cloud import texttospeech
import google.generativeai as genai
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env into os.environ

# Initialize the recognizer
recognizer = sr.Recognizer()  # Create a Recognizer instance
recognizer.energy_threshold = 4000  # Set the energy threshold for speech detection
recognizer.dynamic_energy_adjustment_damping = 0.15  # Set the damping for dynamic energy adjustment

# Initialize Generative AI client
genAI = genai.configure(api_key=os.environ["GENAI_KEY"])  # Configure Generative AI with API key from environment
model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize a generative model
chat = model.start_chat(history=[])  # Start a chat session with empty history

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:  # Use the microphone as the audio source
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise for 1 second
        audio = recognizer.listen(source)  # Capture the audio from the microphone
        print('Recognizing...')
        try:
            text = recognizer.recognize_google(audio)  # Use Google Web Speech API to recognize speech
            print(f"\nYou said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

# Function to generate AI response
def generate_response(prompt):
    try:
        response = chat.send_message(prompt)  # Send the user's prompt to the AI model
        clean_text = response.text.replace('*', '')  # Clean the response text
        print(f"\nBot: {clean_text}")
        return clean_text
    except:
        print('Something wrong!')

# Function to synthesize speech and play it directly from memory
def text_to_speech(text):
    client = texttospeech.TextToSpeechClient()  # Create a Text-to-Speech client

    input_text = texttospeech.SynthesisInput(text=text)  # Set the input text for synthesis

    # Specify the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # Set the audio encoding format
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # Handle the audio content in memory
    audio_content = io.BytesIO(response.audio_content)

    # Play the audio using pydub
    audio_segment = AudioSegment.from_file(audio_content, format="mp3")
    play(audio_segment)

# Main function
def main():
    while True:
        user_input = recognize_speech()  # Recognize speech from the user
        if user_input:
            ai_response = generate_response(user_input)  # Generate AI response to the recognized speech
            text_to_speech(ai_response)  # Synthesize and play the AI response
            if user_input in ['exit', 'close', 'goodbye']:
                break  # Exit the loop if the user says 'exit', 'close', or 'goodbye'

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
