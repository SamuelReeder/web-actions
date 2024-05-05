import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ActionBuilder



def complete_action(data, action):
    # Find the action in the data
    for i in range(len(data)):
        if data[i]['action'] == action:
            # Update the action to be complete
            data[i]['complete'] = True
            break
    return data

if __name__ == '__main__':
    
    with open('actions(2).json', 'r') as f:
        # Load JSON data from file
        data = json.load(f)
        
    print('Before:', data)
    print(data['1'])
    
    driver = webdriver.Firefox()
    driver.maximize_window()

    driver.get(data['1']['url'])
    sleep(2)

    last_clicked_element = None

    for action in data['1']['steps']:
        if action['action'] == 'click':
            # Find element and click
            element = None
            if action['id'] != 'none':
                print('ID:', action['id'])
                element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, action['id'])))
            # elif action['classes'] != 'none':
            #     print('Classes:', action['classes'])
            #     element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, action['classes'])))
            # elif action['tag']:
            #     print('Tag:', action['tag'])
            #     element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, action['tag'])))
            else:
                # Move cursor to x, y position and click
                x = action['position']['x']
                y = action['position']['y']
                # print('Position:', x, y)
                # action_chain = ActionChains(driver)
                # header = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'header')))
                # action_chain.move_to_element(header).move_by_offset(x, y).click().perform()
                # last_clicked_element = driver.switch_to.active_element
                # x = action['position']['x']
                # y = action['position']['y']
                # print('Position:', x, y)

                # # Execute JavaScript to scroll to the desired position
                # # driver.execute_script(f"window.scrollTo({x}, {y});")

                # # Click at the desired position using JavaScript
                # driver.execute_script(f"document.elementFromPoint({x}, {y}).click();")

                # # Get the last clicked element
                # Move to position (64,60) and click() at that position (Note: you will not see your mouse move)
                action = ActionBuilder(driver)
                action.pointer_action.move_to_location(x, y)
                action.pointer_action.click()
                action.perform()
                last_clicked_element = driver.switch_to.active_element

            if element:
                element.click()
                last_clicked_element = element

            sleep(2)
        elif action['action'] == 'keydown' and last_clicked_element is not None:
            # Send key to the last clicked element
            print('Key:', action['key'])
            last_clicked_element.send_keys(action['key'])
            
            sleep(2)

    # Rest of your code...


    # Close WebDriver instance
    # driver.quit()
    