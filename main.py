import os
import time
from PIL import Image
import cv2


def video_to_frames(video_path, output_folder):
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


def resize_images(folder_path):
    # Loop through all jpeg files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            file_path = os.path.join(folder_path, filename)

            # Read the image
            img = cv2.imread(file_path)

            # Resize the image to 640x480
            resized_img = cv2.resize(img, (80, 80))

            # Save the resized image back to the same file
            cv2.imwrite(file_path, resized_img)

            print(f"Resized {filename}")


def frames_to_arrays(folder_path):
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


def jpg_to_array(image_path):
    # Open the image using PIL
    img = Image.open(image_path)

    # Convert image to RGB (in case it's in another format like RGBA or Grayscale)
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

            average = (r + b + g) / 3
            average = round(average, 0)
            average = int(average)

            # Append the RGB tuple to the row
            row.append(average)

        # Append the row to the 2D array
        greyscale_image_array.append(row)

    return greyscale_image_array


def greyscale_to_ascii(frames_list):
    frame_count = 0
    for i in range(len(frames_list)):
        print(f"Processing frame {frame_count}")
        for j in range(len(frames_list[i])):
            for k in range(len(frames_list[i][j])):
                pixel = frames_list[i][j][k]
                if pixel < 32:
                    frames_list[i][j][k] = ' '
                elif 32 <= pixel < 64:
                    frames_list[i][j][k] = '.'
                elif 64 <= pixel < 96:
                    frames_list[i][j][k] = ':'
                elif 96 <= pixel < 128:
                    frames_list[i][j][k] = '-'
                elif 128 <= pixel < 160:
                    frames_list[i][j][k] = '+'
                elif 160 <= pixel < 192:
                    frames_list[i][j][k] = '='
                elif 192 <= pixel < 224:
                    frames_list[i][j][k] = '%'
                elif 224 <= pixel < 255:
                    frames_list[i][j][k] = '@'
                else:
                    frames_list[i][j][k] = "F"

        frame_count += 1

    return frames_list


if __name__ == "__main__":
    # video_to_frames('SpaceOddity.mp4', 'frames')
    # resize_images('frames')
    frames_list = frames_to_arrays('frames')
    frames_list = greyscale_to_ascii(frames_list)

    for frame in frames_list:
        for row in frame:
            print(row)
        time.sleep(0.033333333)
        os.system('cls' if os.name == 'nt' else 'clear')

    # Replace 'your_image_path_here.jpg' with the path to the image you'd like to convert

    # image_path = 'image.jpeg'

    # Convert the image to a 2D array of RGB values
    # greyscale_image_array = convert_to_array(image_path)

    # Print the 2D array
    # for row in greyscale_image_array:
    #   print(row)
