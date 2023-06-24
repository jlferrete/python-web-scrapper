import random
import pandas as pd
import xlsxwriter
from datetime import datetime
from custom_webdriver.custom_webdriver import driver
from custom_credentials.custom_credentials import USER, PWD, WEB_URL_TO_SCRAPE, EXPORT_FILE_NAME
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

def main():
    print("Starting to scrape")
    #Create dataframe and set columns
    df = pd.DataFrame()
    df['Product_name'] = None
    df['Product_image'] = None
    df['Product_price'] = None
    df['Product_description'] = None
        
    # testing_interceptor() 
    driver.get(WEB_URL_TO_SCRAPE)
    navigate_to_login()
    enter_credentials()
    navigate_to_data_page()
    df = scrap_data(df)
    #Set a flag for pagination
    exists_next_page = True
    while exists_next_page:
        exists_next_page = create_new_tab_for_pagination(df)
    
    # Export DataFrame to XLSX
    df_reset=df.set_index('Product_name')
    with pd.ExcelWriter(EXPORT_FILE_NAME, engine='xlsxwriter') as writer:
        df_reset.to_excel(writer, sheet_name= datetime.today().strftime('%Y-%m-%d'))

    #print("Mi programa ha terminado de ejecutarse.") 
    #input("Presione Enter para cerrar el programa.")

    # terminate the browser instance
    driver.quit()

    print("Web Scrapped successfully")

def navigate_to_login():
    # wait until presence of button is located
    login_button_checker = check_element([By.XPATH, '/html/body/div[3]/div/div[8]/div/div[3]/a'])
            
    login_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[8]/div/div[3]/a')
    login_button.click()

def enter_credentials():
    # wait until presence of elements is located   
    login_form_checker = [
        check_element((By.ID, 'id_name')),
        check_element((By.ID, 'id_password')),
        check_element((By.CSS_SELECTOR, 'form button[type=submit]'))
    ]
  
    # retrieve the form elements
    name_input = driver.find_element(By.ID, 'id_name')
    password_input = driver.find_element(By.ID, 'id_password')
    submit_button = driver.find_element(By.CSS_SELECTOR, 'form button[type=submit]')

    # filling out the form elements
    name_input.send_keys(USER)
    password_input.send_keys(PWD)

    # submit the form and log in
    submit_button.click()

def navigate_to_data_page():
    # wait until presence of link is located
    section_link_checker = check_element([By.XPATH, '/html/body/div/div/div[2]/div/div[2]/p[5]/a'])

    section_link = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div[2]/p[5]/a')
    section_link.click()
    
def scrap_data(df):  
    # Wait until presence of a "card" is located
    card_url_checker = check_element([By.CSS_SELECTOR, '.card-body > h4 > a'])

    #Locate card elements
    cards_urls = driver.find_elements(By.CSS_SELECTOR, '.card-body > h4 > a')

    for card_url in cards_urls:              
        product_details_link = card_url.get_attribute('href')
        #Open a new window
        driver.execute_script("window.open('');")
        # Switch to the new window and open a new URL
        driver.switch_to.window(driver.window_handles[1])
        driver.get(product_details_link)

        extract_product_details(df)

        # Close the tab with URL B
        driver.close()
        # Switch back to the first tab with URL A
        driver.switch_to.window(driver.window_handles[0])
    
    return df

def create_new_tab_for_pagination(df):
    
    if check_exists_by_xpath(driver, "//a[@class='page-link'][contains(text(), 'Next')]"):
        element = driver.find_element(By.XPATH, "//a[@class='page-link'][contains(text(), 'Next')]").get_attribute('href')        
        # Switch to the new window and open a new URL
        driver.switch_to.window(driver.window_handles[0])
        driver.get(element)
        
        # Wait until presence of a "card" is located
        # card_url_checker = check_element([By.CSS_SELECTOR, '.card-body > h4 > a'])

        #Locate card elements
        cards_urls = driver.find_elements(By.CSS_SELECTOR, '.card-body > h4 > a')

        for card_url in cards_urls:              
            product_details_link = card_url.get_attribute('href')

            #Open a new window
            driver.execute_script("window.open('');")
            # Switch to the new window and open a new URL
            driver.switch_to.window(driver.window_handles[1])
            driver.get(product_details_link)
               
            extract_product_details(df)
            # Close the tab with URL B
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
        return True
    else:
        driver.close()
        return False      

def extract_product_details(df):
    '''    
    login_form_checker = [
        check_element((By.CSS_SELECTOR, '.card-title')),
        check_element((By.CSS_SELECTOR, '.card-img-top')),
        check_element((By.CSS_SELECTOR, '.card-body > h4')),
        check_element((By.CSS_SELECTOR, '.card-text'))
    ]
    '''    

    product_name = driver.find_element(By.CSS_SELECTOR, '.card-title').text
    product_image = driver.find_element(By.CSS_SELECTOR, '.card-img-top').get_attribute('src')
    product_price = driver.find_element(By.CSS_SELECTOR, '.card-body > h4').text
    product_description = driver.find_element(By.CSS_SELECTOR, '.card-text').text

    # Append scraped data to DataFrame
    product = pd.Series(data={
        'Product_name':product_name, 
        'Product_image':product_image,
        'Product_price':product_price,
        'Product_description':product_description})   
        
    # Add product to DataFrame
    df.loc[len(df)] = product

    return df

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def check_element(element):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(element)
        )
    except NoSuchElementException:
        return False
    return True

def testing_interceptor():
    driver.get("http://httpbin.org/anything")   

if __name__ == '__main__':
    main()


