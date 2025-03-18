# LiveKit Voice Pipeline Agent with Audio Length Validation

This project implements a real-time voice assistant using the **LiveKit Voice Pipeline Agent**, integrated with Google’s Speech-to-Text (STT), Language Model (LLM), and Text-to-Speech (TTS) services. It features a **Flask server** that validates and trims text responses to ensure audio output fits within a 60-second limit, assuming a speech rate of 150 words per minute (0.4 seconds per word). The system is designed for seamless voice interaction, with text trimming handled via an asynchronous callback before TTS processing.

## Project Structure

- **`app.py`**: Flask server that handles text input, estimates audio length, and trims text if necessary.
- **`before_tts.py`**: LiveKit agent script that sets up the voice pipeline and integrates the trimming callback.
- **`requirements.txt`**: List of Python dependencies required to run the project.
- **`.env`**: Environment file for storing API keys and configuration (not included in the repository).
- **`templates/index.html`**: Simple HTML template for testing the Flask server (optional, not provided here).

## Setup Instructions

Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/harry-ninjatech/LiveKit-Voice-Pipeline.git
   cd LiveKit-Voice-Pipeline
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   Ensure you have `ngrok` installed globally to expose the Flask server:
   ```bash
   npm install -g ngrok  # Or use another package manager
   ```

3. **Set Environment Variables**:
   Create a `.env` file in the root directory with the following:
   ```
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   GOOGLE_CREDENTIALS_FILE=file.json  # Path to your Google credentials file
   GOOGLE_API_KEY=your_google_api_key   # For Gemini LLM
   ```
   Replace placeholders with your actual credentials.

4. **Run the Flask Server**:
   Start the Flask server:
   ```bash
   python app.py
   ```
   Expose it publicly using ngrok:
   ```bash
   ngrok http 5000
   ```
   Copy the ngrok URL (e.g., `https://your-ngrok-url.ngrok-free.app/`).

5. **Update the LiveKit Agent**:
   In `before_tts.py`, replace the `server_url` in the `before_tts_cb` function with your ngrok URL:
   ```python
   server_url = "https://your-ngrok-url.ngrok-free.app/"
   ```

6. **Run the LiveKit Agent**:
   Start the agent with the appropriate LiveKit credentials:
   ```bash
   python before_tts.py dev --url your_livekit_url --api-key your_api_key --api-secret your_api_secret
   ```

## Code Explanations

### `app.py` - Flask Server
- **Purpose**: Provides an endpoint to receive text, estimate its audio length, and trim it if it exceeds 60 seconds.
- **Key Functions**:
  - `get_target_words()`: Returns 150 words as the target for 60 seconds of audio.
  - `trim_text_to_middle_segment(text, target_words)`: Trims text to a middle segment of 150 words if it’s too long.
  - `/` Route: Handles GET/POST requests, processes text, and returns trimmed results.
- **Logic**: Assumes 0.4 seconds per word (150 words = 60 seconds). If the estimated time exceeds 60 seconds, it trims to the middle 150 words.

### `before_tts.py` - LiveKit Agent
- **Purpose**: Sets up a `VoicePipelineAgent` with STT, LLM, TTS, and a callback for text trimming.
- **Key Components**:
  - `prewarm(proc)`: Preloads the Silero Voice Activity Detection (VAD) model.
  - `before_tts_cb(text)`: Asynchronous callback that estimates audio length and sends text to the Flask server for trimming via `aiohttp`.
  - `entrypoint(ctx)`: Connects to a LiveKit room, configures the agent with Google services (Chirp STT, Gemini LLM, female TTS voice), and starts the pipeline.
- **Configuration**:
  - STT: Google Chirp model with spoken punctuation.
  - LLM: Google Gemini 2.0 Flash (experimental) with a temperature of 0.8.
  - TTS: Google TTS with a female voice (`en-US-Standard-H`).

## Usage

1. **Start the Flask Server and ngrok**:
   Ensure the server is running and accessible via the ngrok URL.

2. **Run the LiveKit Agent**:
   Launch the agent using the command above.

3. **Interact with the Agent**:
   - Connect to the LiveKit room using a client (e.g., a LiveKit React app or SDK).
   - Speak to the agent and provide long inputs to test the trimming functionality.
   - The agent will respond with trimmed audio if the original response exceeds 60 seconds.

4. **Test the System**:
   - Use the Flask server’s web interface (if `index.html` is implemented) to manually test text trimming.
   - Verify the agent trims responses appropriately in real-time voice interactions.
5. **Record a Demo**:
   [Demo video](https://drive.google.com/file/d/1S0yPOcDHUMouXWfFHUBMthUu_EYJWY-e/view?usp=sharing)   


---
