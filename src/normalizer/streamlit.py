import io
import normalizer
import numpy as np


def run_with_web():
  import streamlit as st
  st.title("WAV normalizer")
  lufs = st.number_input("LUFS", min_value=-60, max_value=0, value=-26)
  # 複数ファイル対応にできるが、ダウンロードボタンを押すたびに全体のスクリプトが再実行されてしまって使いづらいので1ずつに制限する
  uploaded_files = st.file_uploader("Choose file",type=["wav"], accept_multiple_files=False)
  with st.spinner('Wait for normalizing...'):
    is_processed = False
    # 後で複数対応したらこのコードは削除できる
    uploaded_files = [uploaded_files]
    for uploaded_file in uploaded_files:
      if uploaded_file is None:
        continue

      result = None
      # キャッシュがあるときはキャッシュを使う
      file_hash = normalizer.calculate_file_hash(uploaded_file)
      if file_hash in st.session_state:
        result = st.session_state[file_hash]
      if result is None:
        result = normalizer.normalize(input_file=uploaded_file, output_file="", lufs=lufs)
        st.session_state[file_hash] = result

      st.text(f"Input file loudness: {result.input_loudness}")
      st.text(f"Output file loudness: {result.output_loudness}")
      st.audio(result.loudness_normalized_audio, format='audio/wav', sample_rate=result.rate)

      # audioファイルをdonwload_buttonで利用できるように変換する
      buffer = io.BytesIO()
      np.save(buffer, result.loudness_normalized_audio)
      buffer.seek(0)

      st.download_button(
        label=f"Download {result.output_file}",
        data=buffer,
        file_name=result.output_file,
        mime="audio/wav"
      )
      st.toast("Done: " + uploaded_file.name, icon="✅")
      is_processed = True
    if is_processed:
      st.success("All done!")

if __name__ == "__main__":
    run_with_web()