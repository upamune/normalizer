import fire
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

def run(input_file="", output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False, web=False):
  if web:
    run_with_web()
  else:
    run_with_cli(input_file, output_file, lufs, filter_class, skip_normalize)

def run_with_web():
  import streamlit as st
  st.title("normalizer")
  lufs = st.number_input("LUFS", min_value=-60, max_value=0, value=-26)
  uploaded_files = st.file_uploader("Choose file", accept_multiple_files=True)
  with st.spinner('Wait for normalizing...'):
    is_processed = False
    for uploaded_file in uploaded_files:
      uploaded_file.name
      result = normalize(input_file=uploaded_file, output_file="", lufs=lufs)
      st.text(uploaded_file.name)
      st.audio(result.loudness_normalized_audio, format='audio/wav', sample_rate=result.rate)
      st.download_button(
        label=f"Download {result.output_file_name}",
        data=result.loudness_normalized_audio,
        file_name=result.output_file_name,
        mime="audio/wav"
      )
      st.toast("Done: " + uploaded_file.name, icon="✅")
      is_processed = True
    if is_processed:
      st.balloons()
      st.success("All done!")

def run_with_cli(input_file, output_file, lufs, filter_class, skip_normalize):
  result = normalize(input_file, output_file, lufs, filter_class, skip_normalize)
  print("Input file loudness:", result.input_loudness)
  print("Output file loudness:", result.output_loudness)
  sf.write(file=result.output_file, data=result.loudness_normalized_audio, samplerate=result.rate)
  print("Output file:", result.output_file)

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

if __name__ == '__main__':
  fire.Fire(run)