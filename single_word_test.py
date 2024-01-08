import os
from eff_word_net.streams import SimpleMicStream
from eff_word_net.engine import HotwordDetector

from eff_word_net.audio_processing import Resnet50_Arc_loss

from eff_word_net import samples_loc

base_model = Resnet50_Arc_loss()

mycroft_hw = HotwordDetector(
    hotword="change_model",
    model=base_model,
    reference_file=os.path.join(os.getcwd(), "output", "change_model_ref.json"),
    threshold=0.7,
    relaxation_time=2,
)

mic_stream = SimpleMicStream(
    window_length_secs=1.5,
    sliding_window_secs=0.75,
)

mic_stream.start_stream()

print("Say Change Model ")
while True:
    frame = mic_stream.getFrame()
    result = mycroft_hw.scoreFrame(frame)
    if result == None:
        # no voice activity
        continue
    if result["match"]:
        print("Wakeword uttered", result["confidence"])
