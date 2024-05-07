import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionBuilder
import action
import pytesseract
from PIL import Image
import cv2
import numpy as np
from google.cloud import vision


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    text = [text.description for text in texts]
    print(text)

    # for text in texts:
    #     print(f'\n"{text.description}"')

    #     vertices = [
    #         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
    #     ]

    #     print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def detect_document(path):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    words = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                # print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    # print(
                    #     "Word text: {} (confidence: {})".format(
                    #         word_text, word.confidence
                    #     )
                    # )
                    words.append(word_text)

                    # for symbol in word.symbols:
                    #     print(
                    #         "\tSymbol: {} (confidence: {})".format(
                    #             symbol.text, symbol.confidence
                    #         )
                    #     )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
        
    return words

def yield_cards(cards):
    for i in range(len(cards)):
        try :
            cards[i] = int(cards[i])
        except:
            if cards[i] == 'A':
                cards[i] = 11
            else:
                cards[i] = 10
                

if __name__ == '__main__':
    
    # print('Hello World!')
    
    # actions = action.ActionInterface('actions(6).json')
    # actions.execute('start')
    # actions.execute('bet')
    # actions.execute('deal')
    # sleep(2)
    # actions.execute('hit')
    # actions.scan()
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Update this path

    # Perform OCR on the screenshot
    img = cv2.imread('element.png')

    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Increase contrast
    contrast = cv2.convertScaleAbs(blur, alpha=2.0, beta=50)

    # Sharpen the image
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, kernel)

    # # Thresholding to get a binary image
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                            cv2.THRESH_BINARY, 11, 2)

    # Convert to grayscale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Apply thresholding
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    
    cv2.imwrite('element.png', thresh)
    
    # Load the processed image with Pillow
    processed_img = Image.open('element.png')

    # Define cropping areas
    area_one = (720, 450, 1000, 660)  # Coordinates for the first crop
    area_two = (1450, 450, 1850, 550) # Coordinates for the second crop

    # Perform cropping
    cropped_img_one = processed_img.crop(area_one)
    cropped_img_two = processed_img.crop(area_two)

    # Save the cropped images
    cropped_img_one.save('cropped_img_one.png')
    cropped_img_two.save('cropped_img_two.png')

    # text = pytesseract.image_to_string(cropped_img)

    # Save the cropped image
    # cropped_img.save('cropped_element.png')
    # # print(text)
    
    # # Load your image
    # img = cv2.imread('cropped_element.png')


    # # Optional: Apply dilation and erosion to remove some noise
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    # thresh = cv2.dilate(thresh, kernel, iterations=1)
    # thresh = cv2.erode(thresh, kernel, iterations=1)

    # Use Tesseract to extract text
    # custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789AJQK'
    # text = pytesseract.image_to_string(thresh, config=custom_config)
    # print("Extracted Text: ", text)
    
    # detect_text('cropped_img_one.png')
    # detect_text('cropped_img_two.png')
    player = detect_document('cropped_img_one.png')
    yield_cards(player)
    print(player)
                
    dealer = detect_document('cropped_img_two.png')
    yield_cards(dealer)
    print(dealer)
    