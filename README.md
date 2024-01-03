# normalizer


## Normalize

```bash
$ pdm run normalizer --input_file ./input.wav --lufs -26.0 --output_file normalized.wav
Input file loudness: -37.5792848899898
Output file loudness: -26.049041612979114
```

## Check Loudness

```bash
$ pdm run normalizer --input_file ./input.wav --skip_normalize
Input file loudness: -37.5792848899898
```
