# lufs-normalizer

<img src="https://i.gyazo.com/67b647636efc29fe2d469da6c7b62f2c.png" width="700px">

## Normalize

```bash
$ pdm run cli --input_file ./input.wav --lufs -26.0 --output_file normalized.wav
Input file loudness: -37.5792848899898
Output file loudness: -26.049041612979114
```

### Web

```bash
$ pdm run web
```

![screenshot](https://i.gyazo.com/3dfc9af82613d71bb95aaa4174d13a7b.jpg)

## Check Loudness

```bash
$ pdm run cli --input_file ./input.wav --skip_normalize
Input file loudness: -37.5792848899898
```
