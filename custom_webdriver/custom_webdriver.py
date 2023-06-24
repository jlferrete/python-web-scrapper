from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Seting custom headers to avoid anti-bot technologies
user_agent = 'Mozilla/5.0 (Linux; Android 11; 100011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36'
sec_ch_ua = '"Google Chrome";v="104", " Not;A Brand";v="105", "Chromium";v="104"'
referer = 'https://www.google.com'

def interceptor(request):
    # delete the "User-Agent" header and set a new one
    del request.headers["user-agent"]  # Delete the header first
    request.headers["user-agent"] = user_agent
    # set the "Sec-CH-UA" header
    request.headers["sec-ch-ua"] = sec_ch_ua
    # set the "referer" header
    request.headers["referer"] = referer

# Setting options
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option(
    # this will disable image loading
    #"prefs", {"profile.managed_default_content_settings.images": 2}
#)
#options.add_argument('--incognito')
# Enable headless mode in Selenium
# options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))

driver.request_interceptor = interceptor