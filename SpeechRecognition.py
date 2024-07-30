import os
import io
import speech_recognition as sr
from google.cloud import texttospeech
import google.generativeai as genai
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()  # This line brings all environment variables from .env into os.environ


# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize Generative AI client
genAI = genai.configure(api_key=os.environ["GENAI_KEY"])
geminiAI = genai.GenerativeModel('gemini-1.5-flash')

# Function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


# Function to generate AI response
def generate_response(prompt):
    response = geminiAI.generate_content(prompt)
    print(f"Generated response: {response.text}")
    return response.text

# Function to synthesize speech and play it directly from memory
def text_to_speech(text):

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary. Use BytesIO to handle it in memory.
    audio_content = io.BytesIO(response.audio_content)

    # Use pydub to play the audio directly from memory
    audio_segment = AudioSegment.from_file(audio_content, format="mp3")
    play(audio_segment)

# Main function
def main():
    while True:
        user_input = recognize_speech()
        if user_input and user_input.lower() == 'exit':
            text_to_speech("Good bye!")
            break
        elif user_input:
            ai_response = generate_response(user_input)
            text_to_speech(ai_response)


if __name__ == "__main__":
    main()
