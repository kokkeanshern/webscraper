from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter
import numpy as np
import pytesseract
from constants import Captcha

def solve_captcha(raw_image_file):
    # Thresholds and blurring sigma
    th1 = 100
    th2 = 140
    sig = 1.4

    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\shern\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    # Load and save the original image
    original = Image.open(raw_image_file)
    # Convert to black and white
    black_and_white = original.convert("L")
    black_and_white.save(Captcha.bnw_image_file)

    # Apply the first threshold
    first_threshold = black_and_white.point(lambda p: p > th1 and 255)
    first_threshold.save(Captcha.first_threshold_file)

    # Apply Gaussian blur
    blur = np.array(first_threshold)  # Create an image array
    blurred = gaussian_filter(blur, sigma=sig)
    blurred = Image.fromarray(blurred)
    blurred.save(Captcha.blurred_image_file)

    # Apply the final threshold
    final = blurred.point(lambda p: p > th2 and 255)
    final = final.filter(ImageFilter.EDGE_ENHANCE_MORE)
    final = final.filter(ImageFilter.SHARPEN)
    final.save(Captcha.final_image_file)

    # Perform OCR using Tesseract
    result = pytesseract.image_to_string(final, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')

    return result
