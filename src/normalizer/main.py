import fire
import os
import pyloudnorm as pyln
import soundfile as sf
import warnings

warnings.simplefilter('ignore')

def run(input_file="", output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False, web=False):
  if web:
    run_with_web()
  else:
    normalize(input_file, output_file, lufs, filter_class, skip_normalize)

def run_with_web():
  import streamlit as st
  st.title("normalizer")
  lufs = st.number_input("LUFS", min_value=-60, max_value=0, value=-26)
  uploaded_files = st.file_uploader("Choose file", accept_multiple_files=True)
  with st.spinner('Wait for normalizing...'):
    is_processed = False
    for uploaded_file in uploaded_files:
      uploaded_file.name
      loudness_normalized_audio, rate = normalize(input_file=uploaded_file, output_file="", lufs=lufs)
      st.text(uploaded_file.name)
      st.audio(loudness_normalized_audio, format='audio/wav', sample_rate=rate)
      st.toast("Done: " + uploaded_file.name, icon="✅")
      is_processed = True
    if is_processed:
      st.balloons()
      st.success("All done!")

def normalize(input_file, output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False):
  data, rate = sf.read(input_file)
  meter = pyln.Meter(rate, filter_class)
  loudness = meter.integrated_loudness(data)
  loudness_normalized_audio = pyln.normalize.loudness(data, loudness, lufs)

  print("Input file loudness:", loudness)

  if skip_normalize:
    return

  if output_file == "":
    if type(input_file) is str:
      name, ext = os.path.splitext(input_file)
      output_file = f"{name}_normalized{ext}"
    elif hasattr(input_file, 'name'):
      name, ext = os.path.splitext(input_file.name)
      output_file = f"{name}_normalized{ext}"
    else:
      output_file = "normalized.wav"

  if not hasattr(input_file, 'name'):
    output_loudness = meter.integrated_loudness(loudness_normalized_audio)
    print("Output file loudness:", output_loudness)
    sf.write(file=output_file, data=loudness_normalized_audio, samplerate=rate)
    print("Output file:", output_file)

  return loudness_normalized_audio, rate

if __name__ == '__main__':
  fire.Fire(run)