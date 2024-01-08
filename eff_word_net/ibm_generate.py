"""
Needs to be run directly in cli via
`python -m eff_word_net.ibm_generate`

Can be used to artificially synthesize audio samples for a given hotword
Uses ibm's demo of cloud neural voice , hence try to use it as low as possible
"""

import requests
import json
import shutil
from os.path import isdir, join
from os import mkdir
from time import sleep

apiKey = "GzqW0TNhPpKp8WBjAyJCFzOqvn6L6vMjYvt6hK4V0gnn"
url = "https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/f29e3601-1d3c-4ee8-805e-663ceb5ff534"


def _getSoundFile(word: str, voice: str, out_dir: str):
    assert isdir(out_dir), "Not a valid output directory"

    out_dir = join(out_dir, word.replace(" ", "_"))
    headers = {
        "Content-Type": "application/json",
        "Accept": "audio/wav",
    }

    params = {
        "voice": voice,
    }

    json_data = {
        "text": word,
    }

    audio_response = requests.post(
        f"{url}/v1/synthesize",
        params=params,
        headers=headers,
        json=json_data,
        auth=("apikey", f"{apiKey}"),
    )
    print(audio_response.status_code)
    if audio_response.status_code == 200:
        audio_response.raw.decode_content = True
        if not isdir(out_dir):
            mkdir(out_dir)
        with open(join(out_dir, f"{word}_{voice}.wav"), "wb") as f:
            f.write(audio_response.content)
        return True
    else:
        print(audio_response.json())
    return False


USA_VOICES = [
    "en-US_OliviaV3Voice",
    "en-US_HenryV3Voice",
    "en-US_MichaelV3Voice",
    "en-US_AllisonV3Voice",
]
UK_VOICES = ["en-GB_CharlotteV3Voice", "en-GB_KateV3Voice", "en-GB_JamesV3Voice"]

if __name__ == "__main__":
    WORD = str(input("Enter your wakeword:"))
    PATH = str(input("Enter location where audio files will be saved:"))
    for voice in [*USA_VOICES, *UK_VOICES]:
        print(voice)
        if _getSoundFile(WORD, voice, PATH):
            print("success")
        else:
            print("failed")
        sleep(2)
