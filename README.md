# Terminal Video Player

This Python script converts a regular video file into ASCII art and plays it back in the terminal. It processes each frame of the video by converting it to grayscale, resizes it, and maps each pixel to an ASCII character based on its brightness.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Pillow (`PIL`)
- curses

## Installation

1. Clone this repository or download the script.
2. Install the required dependencies:
   ```
   pip install opencv-python Pillow
   ```
   Note: `curses` is typically included in Python standard library on Unix-based systems. For Windows, ew, you may need to install `windows-curses`.

## Usage

Run the script with the path to your video file as an argument:

```
python3 main.py path/to/your/video.mp4
```

## How It Works

1. **Video to Frames**: The script extracts individual frames from the video.
2. **Resize**: Each frame is resized to fit the terminal window.
3. **Greyscale Conversion**: Frames are converted to grayscale.
4. **ASCII Mapping**: Each pixel is mapped to an ASCII character based on its brightness.
5. **Playback**: The ASCII frames are displayed in the terminal in rapid succession.

## ASCII Character Mapping

The script uses the following mapping for converting brightness to ASCII characters:

- 0-31: ' ' (space)
- 32-63: '.'
- 64-95: ':'
- 96-127: '-'
- 128-159: '+'
- 160-191: '='
- 192-223: '%'
- 224-255: '@'

## Customization

You can adjust the following parameters in the script:

- Frame rate (in `play_video` function)
- Output resolution (in `resize_images` function)
- ASCII character mapping (in `greyscale_to_ascii` function)


## Demo

https://github.com/user-attachments/assets/05858362-6ad4-4f5c-9aa8-d01dda1515a0


## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes.
