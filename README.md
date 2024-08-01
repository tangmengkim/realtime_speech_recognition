# Real-Time Speech Recognition and Synthesis

This project implements a real-time speech recognition and synthesis system using various APIs and libraries. The system recognizes speech from a microphone, generates responses using an AI model, and synthesizes the responses into speech.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Features
- Real-time speech recognition using Google Web Speech API
- AI response generation using Google Generative AI
- Text-to-speech synthesis using Google Cloud Text-to-Speech
- Dynamic adjustment for ambient noise

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd REALTIME_SPEECH_RECOGNITION
    ```

2. **Create and activate a virtual environment**:
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install ffmpeg for Windows**:
    - Download `ffmpeg` from the following link:
      [ffmpeg-git-full.7z](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
    - Extract the contents to a directory (e.g., `C:\ffmpeg`).
    - Run Command Prompt as an administrator and set the PATH environment variable:
      ```bash
      setx /m PATH "C:\<ffmpeg-path>\bin;%PATH%"
      ```
      Replace `<ffmpeg-path>` with the actual path where `ffmpeg` was extracted.

5. **Set up environment variables**:
    - Create a `.env` file in the project root directory.
    - Add your API keys and other environment variables to the `.env` file. For example:
      ```plaintext
        # Suppress logging warnings
        GRPC_VERBOSITY = "ERROR"
        GLOG_minloglevel = "2"
        # Set up Google Cloud credentials
        GENAI_KEY=your_google_generative_ai_api_key
        GOOGLE_APPLICATION_CREDENTIALS="./service_credential.json"
      ```

6. **Download Google Cloud service credentials**:
    - Download the service account JSON file from the Google Cloud Console.
    - Save it as `service_credential.json` in the project root directory.

## Usage

1. **Run the application**:
    ```bash
    python SpeechRecognition.py
    ```

2. **Interact with the system**:
    - Speak into your microphone.
    - The system will recognize your speech, generate an AI response, and synthesize the response into speech.

3. **Exit the application**:
    - Say "exit", "close", or "goodbye" to exit the application.

## Project Structure

