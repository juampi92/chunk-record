# Chunk Whisper

This is a simple whisper CLI application that instead of streaming whisper, it will only run the model after a 3 second pause.

## Installation

```bash
pipenv install
```

## Usage

```bash
pipenv run python record.py
```

It will first prompt you to select a microphone, and after that it will start recording.
Pressing enter will stop the recording and run the model on the recorded audio.

If your audio has 3 seconds of silence, it will run the model on the audio and count that as a paragraph.

### Configuration

| Argument | Description | Default |
| --- | --- | --- |
| --model | The whisper model to use. [list](https://pypi.org/project/openai-whisper/) | `small` |
| --microphone | Microphone name. The first match that contains this string will be picked. Special options: `pick` will prompt you to pick one. `default` will figure out the first valid one. | `pick` (`default` if --silent is used) |
| --silent | Don't write anything in the console except for the translated audio, and a "Start" to know when to start talking. | `False` |
| --pause-seconds | Seconds of silence to wait for making a new chunk (paragraph). | `3` |
| --debug | Print debug information. | `False` |

## Example usages

Useful to simply get started with the model.

```bash
pipenv run python record.py --silent
```

To try different models. [Check them all here](https://pypi.org/project/openai-whisper/).

```bash
pipenv run python record.py --silent --model=base
```

To use a fixed microphone. Note that `--microphone=pick` does not work with `--silent`.

```bash
pipenv run python record.py --silent --microphone="MacBook Pro Microphone"
```

To add the content to a file after running the model. (you won't see the "start" prompt)

```bash
pipenv run python record.py --microphone="default" >> file.txt
```

## To-do

- [ ] Fix the Ctrl+D exit. Make it gracefully exit.