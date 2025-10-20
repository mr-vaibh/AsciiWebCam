import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os
import time
import argparse

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

def frame_to_ascii(frame, new_width=100, sharpness=1.8):
    image = Image.fromarray(frame)
    image = resize_image(image, new_width)
    image = enhance_sharpness(image, sharpness)
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

def output_to_console(ascii_frame, show_cam=False, frame=None):
    clear_terminal()
    print(ascii_frame)
    
    if show_cam and frame is not None:
        cv2.imshow("Webcam Feed", frame)

def webcam_to_ascii(new_width=100, sharpness=1.8, fps=30, show_cam=False):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    frame_delay = 1.0 / fps

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_frame = frame_to_ascii(frame, new_width=new_width, sharpness=sharpness)
            output_to_console(ascii_frame, show_cam=show_cam, frame=frame)

            time.sleep(frame_delay)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description="Webcam to ASCII Art (Live Terminal Output)")
    parser.add_argument('--width', type=int, default=100, help='Output ASCII width')
    parser.add_argument('--sharpness', type=float, default=1.8, help='Sharpness enhancement factor')
    parser.add_argument('--fps', type=int, default=30, help='Frames per second')
    parser.add_argument('--show-cam', action='store_true', help='Show the raw webcam feed using OpenCV window')

    args = parser.parse_args()

    webcam_to_ascii(
        new_width=args.width,
        sharpness=args.sharpness,
        fps=args.fps,
        show_cam=args.show_cam
    )

if __name__ == "__main__":
    main()
