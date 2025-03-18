import asyncio
import logging
from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import google, silero
import aiohttp

load_dotenv()
logger = logging.getLogger("voice-assistant")
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
async def before_tts_cb(text: str) -> str:
    """
    Callback before TTS processing to estimate audio length and get trimmed text from server.
    """
    num_words = len(text.split())
    estimated_time = num_words * 0.4  # Assuming 0.4 seconds per word (150 words/min)
    server_url = "https://your-ngrok-url.ngrok-free.app/"
    # Replace with actual ngrok URL
    async with aiohttp.ClientSession() as session:
        async with session.post(server_url, json={"text": text, "estimate": estimated_time}) as response:
            trimmed_text = await response.json()
            return trimmed_text["text"]

async def entrypoint(ctx: JobContext):
    """
    Entry point for the agent, setting up and starting the VoicePipelineAgent.
    """
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()
    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=google.STT(model="chirp",
  spoken_punctuation=True,),
        llm=google.LLM( model="gemini-2.0-flash-exp",
  temperature="0.8",),
        tts=google.TTS(gender="female",
  voice_name="en-US-Standard-H",),
        before_tts_cb=before_tts_cb,
    )
    await agent.start(room=ctx.room, participant=participant)

if __name__ == "__main__":
    cli.run_app( WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),)