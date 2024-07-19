import os
import sys
import time
from typing import List, Optional, Union, TypeVar
from PIL import Image
import cv2
import curses

class InsufficientArgumentsError(Exception):
    """Raised when insufficient arguments are provided."""
    pass

def video_to_frames(video_path: str, output_folder: str) -> None:
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the frame count
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Initialize frame number
    frame_no = 0

    while True:
        # Read a frame from the video file
        ret, frame = cap.read()

        # Break the loop if we have reached the end of the video file
        if not ret:
            break

        # Construct the output file path
        output_file_path = os.path.join(output_folder, f"frame_{frame_no:04d}.jpg")

        # Save the frame as a JPEG file
        cv2.imwrite(output_file_path, frame)

        # Print progress
        print(f"Saved {frame_no}/{frame_count}")

        # Increment frame number
        frame_no += 1

    # Release the video capture object
    cap.release()

    print(f"Saved {frame_no} frames to {output_folder}")


def resize_images(folder_path: str) -> None:
    # Loop through all jpeg files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            file_path = os.path.join(folder_path, filename)

            # Read the image
            img = cv2.imread(file_path)

            # Get the original aspect ratio
            height, width = img.shape[:2]
            aspect_ratio = width / height

            # Calculate new dimensions
            new_height = 55
            new_width = int(new_height * aspect_ratio * 2)  # Multiply by 2 to account for character aspect ratio

            # Resize the image
            resized_img = cv2.resize(img, (new_width, new_height))

            # Save the resized image back to the same file
            cv2.imwrite(file_path, resized_img)

            print(f"Resized {filename}")


def frames_to_arrays(folder_path: str) -> List[List[List[int]]]:
    # Initialize a list to hold 2D arrays
    frames_array_list = []

    # Loop through all jpeg files in the folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".jpg"):
            file_path = os.path.join(folder_path, filename)

            # Convert the JPEG file to a 2D array
            frame_array = jpg_to_array(file_path)

            # Append the 2D array to the list
            frames_array_list.append(frame_array)

            print(f"Processed {filename}")

    return frames_array_list


def jpg_to_array(image_path: str) -> List[List[int]]:
    # Open the image using PIL
    img = Image.open(image_path)

    # Convert image to RGB
    img = img.convert("RGB")

    # Get image dimensions
    width, height = img.size

    # Initialize a 2D array to store RGB values
    greyscale_image_array = []

    for y in range(height):
        row = []
        for x in range(width):
            # Get RGB values of each pixel
            r, g, b = img.getpixel((x, y))

            # Convert to greyscale
            average = (r + b + g) / 3
            average = round(average, 0)
            average = int(average)

            # Append brightness value
            row.append(average)

        # Append the row to the 2D array
        greyscale_image_array.append(row)

    return greyscale_image_array


def greyscale_to_ascii(frames_list: List[List[List[int]]]) -> List[List[List[str]]]:
    result: List[List[List[str]]] = []

    frame_count = 0
    for frame in frames_list:
        print(f"Processing frame {frame_count}")
        ascii_frame: List[List[str]] = []
        for row in frame:
            ascii_row: List[str] = []
            for pixel in row:
                if pixel < 32:
                    ascii_char = ' '
                elif 32 <= pixel < 64:
                    ascii_char = '.'
                elif 64 <= pixel < 96:
                    ascii_char = ':'
                elif 96 <= pixel < 128:
                    ascii_char = '-'
                elif 128 <= pixel < 160:
                    ascii_char = '+'
                elif 160 <= pixel < 192:
                    ascii_char = '='
                elif 192 <= pixel < 224:
                    ascii_char = '%'
                elif 224 <= pixel < 255:
                    ascii_char = '@'
                else: ascii_char = ' '
                ascii_row.append(ascii_char)
            ascii_frame.append(ascii_row)
        result.append(ascii_frame)
        frame_count += 1

    return result

def clear_screen() -> None:
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')


def play_video(frames_list: List[List[List[str]]]) -> None:
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)  # This line disables the cursor
    stdscr.keypad(True)

    try:
        for frame in frames_list:
            stdscr.clear()
            for y, row in enumerate(frame):
                stdscr.addstr(y, 0, ''.join(row))
            stdscr.refresh()
            time.sleep(0.03)

    finally:
        # Clean up curses
        curses.nocbreak()
        stdscr.keypad(False)
        #curses.echo()
        curses.endwin()

if __name__ == "__main__":
    try:
        video_title: Optional[str] = sys.argv[1] if len(sys.argv) > 1 else ''

        if video_title:
            video_to_frames(video_title, 'frames')
            resize_images('frames')
            frames_list_ints: List[List[List[int]]] = frames_to_arrays('frames')
            frames_list_strs: List[List[List[str]]] = greyscale_to_ascii(frames_list_ints)
        else:
            raise InsufficientArgumentsError("No video title provided. Please provide a video title as an argument.")


    except InsufficientArgumentsError as e:
        print(f"Error: {e}")
        sys.exit(1)


    play_video(frames_list_strs)
