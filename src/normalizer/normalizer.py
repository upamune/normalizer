import hashlib
import os
import pyloudnorm as pyln
import soundfile as sf
import warnings

warnings.simplefilter('ignore')

class NormalizationResult:
    def __init__(self, loudness_normalized_audio, rate, output_file, input_loudness, output_loudness):
        self.loudness_normalized_audio = loudness_normalized_audio
        self.rate = rate
        self.output_file = output_file
        self.input_loudness = input_loudness
        self.output_loudness = output_loudness

def calculate_file_hash(uploaded_file):
    """アップロードされたファイルのハッシュ値を計算する"""
    file_hash = hashlib.sha256()
    file_hash.update(uploaded_file.getvalue())
    return file_hash.hexdigest()

def normalize(input_file, output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False):
  data, rate = sf.read(input_file)
  meter = pyln.Meter(rate, filter_class)
  input_loudness = meter.integrated_loudness(data)
  loudness_normalized_audio = pyln.normalize.loudness(data, input_loudness, lufs)

  if skip_normalize:
    return

  if output_file == "":
    if isinstance(input_file, str):
      name, ext = os.path.splitext(input_file)
      output_file = f"{name}_normalized{ext}"
    elif hasattr(input_file, 'name'):
      name, ext = os.path.splitext(input_file.name)
      output_file = f"{name}_normalized{ext}"
    else:
      output_file = "normalized.wav"

  output_loudness = meter.integrated_loudness(loudness_normalized_audio)
  return NormalizationResult(loudness_normalized_audio, rate, output_file, input_loudness, output_loudness)
