import fire
import os
import pyloudnorm as pyln
import soundfile as sf
import warnings

warnings.simplefilter('ignore')

def normalize(input_file, output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False):
  data, rate = sf.read(input_file)
  meter = pyln.Meter(rate, filter_class)
  loudness = meter.integrated_loudness(data)
  loudness_normalized_audio = pyln.normalize.loudness(data, loudness, lufs)

  print("Input file loudness:", loudness)

  if skip_normalize:
    return

  if output_file == "":
    name, ext = os.path.splitext(input_file)
    output_file = f"{name}_normalized{ext}"

  output_loudness = meter.integrated_loudness(loudness_normalized_audio)
  print("Output file loudness:", output_loudness)
  sf.write(file=output_file, data=loudness_normalized_audio, samplerate=rate)
  print("Output file:", output_file)

if __name__ == '__main__':
  fire.Fire(normalize)