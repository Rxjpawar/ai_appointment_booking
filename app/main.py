from openai import AsyncOpenAI
import speech_recognition as sr
from .graph import graph
from .mem_config import mem_client
import asyncio
from dotenv import load_dotenv
import tempfile
import os
from langchain_core.messages import HumanMessage
import sounddevice as sd
import soundfile as sf
import io

load_dotenv()

client = AsyncOpenAI()

#openai tts
async def tts(text: str):
    response = await client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # aaplya kde 4 voice aahet : alloy, aria, verse, breeze
        input=text
    )

    audio_bytes =response.read()

    data, samplerate = sf.read(io.BytesIO(audio_bytes))

    sd.play(data, samplerate)
    sd.wait()

#openai tts
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



async def main():

    recognizer = sr.Recognizer()

    while True:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 1.2

            try:
                print("Speak something...")
                audio = recognizer.listen(source)

                print("Processing audio with STT...")
                user_query = await openai_stt(audio)
                if not user_query or not user_query.strip():
                    print("No speech detected. Listening again...")
                    continue

                print(f"You : {user_query}")

            except Exception as e:
                print("Bot : Error processing voice:", str(e))
                continue

        if user_query.lower() == "exit":
            print("Exiting app...")
            break

        _state = {
            "messages": [HumanMessage(content=user_query)]
        }

        graph_result = await graph.ainvoke(_state)

        last_message = graph_result["messages"][-1]
        output = last_message.content

        print("Bot :", output)
        try:
            mem_client.add(
                [
                    {"role": "user", "content": user_query},
                    {"role": "assistant", "content": output},
                ],
                user_id="raj",
            )
        except Exception:
            pass

        # speak response
        await tts(output)


if __name__ == "__main__":
    asyncio.run(main())