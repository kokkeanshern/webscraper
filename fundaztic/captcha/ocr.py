import os
import pytesseract
import numpy as np
from constants import Captcha
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

def solve_captcha(raw_image_file: str) -> str:
    """
    Processes the captcha image and returns the solved captcha text.
    Args:
        raw_image_file (str): Path to the raw captcha image file.
    Returns:
        result (str): The solved captcha text.
    """

    # Keep these values constant for now.
    th1, th2, sig = 100, 140, 1.4

    pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_EXECUTABLE_PATH"]

    original = Image.open(raw_image_file)
    
    # Convert the image to black and white.
    black_and_white = original.convert("L")
    black_and_white.save(Captcha.bnw_image_file)

    # Apply the first threshold.
    first_threshold = black_and_white.point(lambda p: p > th1 and 255)
    first_threshold.save(Captcha.first_threshold_file)

    # Apply Gaussian blur.
    blur = np.array(first_threshold)
    blurred = gaussian_filter(blur, sigma=sig)
    blurred = Image.fromarray(blurred)
    blurred.save(Captcha.blurred_image_file)

    # Apply the final threshold.
    final = blurred.point(lambda p: p > th2 and 255)
    final = final.filter(ImageFilter.EDGE_ENHANCE_MORE)
    final = final.filter(ImageFilter.SHARPEN)
    final.save(Captcha.final_image_file)

    # Perform OCR using Tesseract
    result = pytesseract.image_to_string(final, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')

    return result
