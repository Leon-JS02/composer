### Composer v1.0.1

Composer is a command-line tool for musical analysis and operations on audio files. It supports key signature classification, tempo estimation, and more.

**Dependencies**

- **Librosa**
- **SciPy**
- **NumPy**
- **Pandas**
- **Matplotlib**
- **Soundfile**

## **Note:** Ensure to set the audio library path using the `-s/--set` command before using Composer. The recommended path relative to the project's root is `Library/Audio`.

Example usage:

```bash
python composer.py --help
python composer.py --set 'C:/.../Composer/Library/Audio'
python composer.py --list
python composer.py --key prelude_in_cmaj.wav
```

#### *Accepted file formats: .MP3, .WAV, .OGG, .FLAC, .M4A*
