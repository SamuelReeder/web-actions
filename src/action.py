import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionBuilder
import pytesseract
from PIL import Image
import cv2


class ActionInterface:
    def __init__(self, data):
        self.load_data(data)
        self.last_clicked_element = None
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()


    def load_data(self, data):
         with open(data, 'r') as f:
            self.data = json.load(f)
        

    def execute(self, name):
        if self.data[name]['url'] != 'none':
            self.driver.get(self.data[name]['url'])
        sleep(3)

        for action in self.data[name]['steps']:
            if action['action'] == 'click':
                element = None
                if action['id'] != 'none':
                    print('ID:', action['id'])
                    element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, action['id'])))
                # elif action['classes'] != 'none':
                #     print('Classes:', action['classes'])
                #     element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, action['classes'])))
                # elif action['tag']:
                #     print('Tag:', action['tag'])
                #     element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, action['tag'])))
                else:
                    x = action['position']['x']
                    y = action['position']['y']
                    action = ActionBuilder(self.driver)
                    action.pointer_action.move_to_location(x, y)
                    action.pointer_action.click()
                    action.perform()
                    self.last_clicked_element = self.driver.switch_to.active_element

                if element:
                    element.click()
                    self.last_clicked_element = element

            elif action['action'] == 'keydown' and self.last_clicked_element is not None:
                print('Key:', action['key'])
                self.last_clicked_element.send_keys(action['key'])
                
            sleep(1)
                
    def scan_cards(self):

        self.driver.get_screenshot_as_file('element.png')
        img = cv2.imread('element.png')

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        contrast = cv2.convertScaleAbs(blur, alpha=2.0, beta=50)
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        sharpened = cv2.filter2D(contrast, -1, kernel)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        
        cv2.imwrite('element.png', thresh)
        
        processed_img = Image.open('element.png')

        area_one = (720, 450, 1000, 660)  
        area_two = (1450, 450, 1850, 550) 

        cropped_img_one = processed_img.crop(area_one)
        cropped_img_two = processed_img.crop(area_two)

        cropped_img_one.save('cropped_img_one.png')
        cropped_img_two.save('cropped_img_two.png')