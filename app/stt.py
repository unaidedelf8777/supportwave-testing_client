import logging
import os
import shutil
import time
import uuid
import requests 
import ffmpeg
import openai
import json
from app.util import delete_file

LANGUAGE = os.getenv("LANGUAGE", "en")


async def transcribe(audio):
    start_time = time.time()
    initial_filepath = f"/tmp/{uuid.uuid4()}{audio.filename}"

    with open(initial_filepath, "wb+") as file_object:
        shutil.copyfileobj(audio.file, file_object)

    converted_filepath = f"/tmp/ffmpeg-{uuid.uuid4()}{audio.filename}"

    logging.debug("running through ffmpeg")
    (
        ffmpeg
        .input(initial_filepath)
        .output(converted_filepath, loglevel="error")
        .run()
    )
    logging.debug("ffmpeg done")

    delete_file(initial_filepath)

    read_file = open(converted_filepath, "rb")

    # Send a POST request to your API
    response = requests.post('https://supportwave.app/predict', files={'file': read_file})

    if response.status_code != 200:
        raise ValueError(f"Your API returned status code {response.status_code}. Response: {response.text}")
    
    # Assume your API returns a json response where the transcription is stored under the key "transcription"
    transcription1 = response.json()
    transcription = json.dumps(transcription1)
    print(transcription)
    logging.info("STT response received from whisper in %s %s", time.time() - start_time, 'seconds')
    logging.info('user prompt: %s', transcription)

    delete_file(converted_filepath)

    return transcription
