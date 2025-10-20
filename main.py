import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
import time

# ASCII chars from dark to light
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def enhance_sharpness(image, factor=1.8):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  # adjust height ratio for terminal
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)

def to_grayscale(image):
    return image.convert("L")

def pixel_to_ascii(pixel_value):
    return ASCII_CHARS[pixel_value * len(ASCII_CHARS) // 256]

def frame_to_ascii(frame, new_width=100):
    image = Image.fromarray(frame)
    image = resize_image(image, new_width)
    image = enhance_sharpness(image, 20)
    gray_image = to_grayscale(image)

    pixels = gray_image.getdata()
    ascii_str = "".join([pixel_to_ascii(p) for p in pixels])
    
    # format to lines
    ascii_image = ""
    for i in range(0, len(ascii_str), image.width):
        ascii_image += ascii_str[i:i + image.width] + "\n"

    return ascii_image

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def output_to_console(frame, ascii_frame):
    clear_terminal()

    # Output the ASCII
    print(ascii_frame)

    # Output the WebCam
    # cv2.imshow("Webcam Feed", frame)

def webcam_to_ascii(real_time=False, new_width=100):
    # Open webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to ASCII
        ascii_frame = frame_to_ascii(frame, new_width)

        output_to_console(frame, ascii_frame)

        time.sleep(0.033)  # ~30 frames per second (adjust this value to change frame rate)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    webcam_to_ascii(real_time=True, new_width=120)  # Adjust width as needed
