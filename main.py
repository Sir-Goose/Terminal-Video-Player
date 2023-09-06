import os

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
def convert_to_array(image_path):
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

            # Append the RGB tuple to the row
            row.append(average)

        # Append the row to the 2D array
        greyscale_image_array.append(row)

    return greyscale_image_array






if __name__ == "__main__":
    # Replace 'your_image_path_here.jpg' with the path to the image you'd like to convert
    image_path = 'image.jpeg'

    # Convert the image to a 2D array of RGB values
    greyscale_image_array = convert_to_array(image_path)

    # Print the 2D array
    for row in greyscale_image_array:
        print(row)

