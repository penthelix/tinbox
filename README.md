# Tinbox

Fetch YouTube videos from RSS feeds in your terminal.

![Tinbox help message](./assets/help-message.png)

Tinbox is a terminal program that displays the latest YouTube videos from your subscriptions in your terminal. You can set your subscriptions by adding their RSS feeds.

I made this to be able to check in on my subscriptions without having to open a browser window or interact with thumbnails and other distracting parts of the YouTube UI.

Tinbox is still in early development. Future releases will add video details and the option to mark videos as watched, similar to how you'd mark podcast episodes as watched on [AntennaPod](https://antennapod.org/).

## Installation

### Linux

Tinbox is available as an executable for Linux.

1. Download the latest release from [GitHub releases](https://github.com/penthelix/tinbox/releases/latest).
2. Make the executable executable.

```bash
chmod +x tinbox
```

3. Move the executable to a directory in your PATH. Skip this step if you just want to try out the program.

```bash
mv tinbox ~/.local/bin
```

3. Run the executable from the command line.

```bash
tinbox
```

### Others

On Windows and MacOS, you can build from source.

1. Clone this repository.

```bash
git clone https://github.com/penthelix/tinbox.git
```

2. Build the executable using [PyInstaller](https://pyinstaller.org/) or a tool of your choice.

```bash
pyinstaller --onefile src/__main__.py
```

3. Move the executable to a folder in your PATH. This could be `/usr/local/bin` on MacOS.

```bash
mv dist/__main__ /usr/local/bin/tinbox # MacOS
```

On Windows, `C:\Windows` is in your PATH by default, though it is recommended to put the executable in `C:\Program Files\tinbox` and subsequently, add that folder to your PATH. [Here](https://stackoverflow.com/q/44272416) is a guide on that.

4. Run the executable from the command line.

```bash
tinbox
```

## Tech Stack

- Python 3
- [uv](https://docs.astral.sh/uv/) for dependency management
- [feedparser](https://feedparser.readthedocs.io/en/latest/) for parsing RSS feeds
- [argparse](https://docs.python.org/3/library/argparse.html) for parsing CLI arguments

## Dev Setup

1. Check if you have uv installed. If not, install [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv --version
```

2. Create virtual environment and install dependencies.

```bash
uv sync
```

3. Run the CLI.

```bash
uv run tinbox
```

## Compatibility

Tinbox has been tested on the following operating systems.

1. Debian 13

## AI Usage Disclosure

In-line code completion was used in coding this project. Chat was used sparingly to debug. No agents were used.
