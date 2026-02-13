from openai import AsyncOpenAI
import speech_recognition as sr
from .graph import graph
from .mem_config import mem_client
import asyncio
from dotenv import load_dotenv
import tempfile
import os
from elevenlabs.client import ElevenLabs
from playsound import playsound

load_dotenv()

client = AsyncOpenAI()
eleven_client = ElevenLabs()

#speech to text 
async def openai_stt(audio_data):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_data.get_wav_data())
        tmp_filename = tmp_file.name

    try:
        with open(tmp_filename, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
            )
        return transcript.text
    finally:
        os.remove(tmp_filename)

# Text to speech
async def tts(text: str):
    audio = eleven_client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_flash_v2_5",
        text=text
    )

    filename = "response.mp3"

    with open(filename, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    playsound(filename)
    os.remove(filename)



def main():
  
    r = sr.Recognizer()

    mode = "voice"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        while True:
            if mode == "voice":
                try:
                    print("Speak something...")
                    audio = r.listen(source)
                    print("Processing audio with OpenAI STT...")
                    user_query = asyncio.run(openai_stt(audio))
                    print(f"You : {user_query}")
                except Exception as e:
                    print("Bot : Error processing voice:", str(e))
                    continue

            if user_query.lower() == "exit":
                print("Exiting app...")
                break

            _state = {"messages": [{"role": "user", "content": user_query}]}

            graph_result = graph.invoke(_state)
            output = graph_result["messages"][-1].content

            print("Bot :", output)
            mem_client.add(
                [
                    {"role": "user", "content": user_query},
                    {"role": "assistant", "content": output},
                ],

                user_id="raj", # graph realtion db user id 
                )

            asyncio.run(tts(text=output))

if __name__ == "__main__":
    main()