import fire
import normalizer
import soundfile as sf
import warnings

warnings.simplefilter('ignore')

def run_with_cli(input_file, output_file="", lufs=-26, filter_class="K-weighting", skip_normalize=False):
  result = normalizer.normalize(input_file, output_file, lufs, filter_class, skip_normalize)
  print("Input file loudness:", result.input_loudness)
  print("Output file loudness:", result.output_loudness)
  sf.write(file=result.output_file, data=result.loudness_normalized_audio, samplerate=result.rate)
  print("Output file:", result.output_file)

if __name__ == '__main__':
  fire.Fire(run_with_cli)