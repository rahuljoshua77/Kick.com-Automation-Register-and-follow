from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time,os,base64,json,csv,re
import undetected_chromedriver as uc
 
import warnings,config
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from time import sleep
cwd = os.getcwd()
opts = Options()

# opts.add_argument('--headless=chrome')
# #pts.headless = False

options = uc.ChromeOptions()

opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

opts.add_argument('--disable-setuid-sandbox')
opts.add_argument('--disable-infobars')
opts.add_argument('--ignore-certifcate-errors')
opts.add_argument('--ignore-certifcate-errors-spki-list')
opts.add_argument("--incognito")
opts.add_argument('--no-first-run')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument("--disable-infobars")
opts.add_argument("--disable-extensions")
opts.add_argument("--disable-popup-blocking")
opts.add_argument('--log-level=3') 
opts.add_argument("--start-fullscreen")
opts.add_argument("--start-maximized")

opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option("useAutomationExtension", False)
opts.add_experimental_option("excludeSwitches",["enable-automation"])
 
# mobile_emulation = {
#     "deviceMetrics": { "width": 660, "height": 1080, "pixelRatio": 3.4 },
#     }
def date_show():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date
 
def xpath_type(el,mount):
    return wait(browser,15).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_fast(el):
    element_all = wait(browser,5).until(EC.presence_of_element_located((By.XPATH, el)))
    #browser.execute_script("arguments[0].scrollIntoView();", element_all)
    return browser.execute_script("arguments[0].click();", element_all) 

def xpath_long(el):
    element_all = wait(browser,30).until(EC.element_to_be_clickable((By.XPATH, el)))
 
    return browser.execute_script("arguments[0].click();", element_all) 

def login_acc(data):
    try:
        xpath_fast("//button[text()='Accept']")
    except:
        pass

    xpath_long('//button[@id="login-button"]')
    xpath_type('//input[@id="email"]',data.split("|")[0])
    xpath_type('//input[@id="password"]',data.split("|")[1])
    sleep(3)
    xpath_long('//button[@type="submit"]')
    wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '(//a[@href="/following"])[1]')))

    
def login(data):
    # Define the field names
    global browser
    # opts.add_experimental_option("mobileEmulation", mobile_emulation)
    opts.add_argument(f"user-agent=Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1")
    browser = uc.Chrome(options=options,driver_executable_path="./chromedriver.exe",use_subprocess=True)

    browser.get("https://kick.com")
    print(f"{date_show()} [{data.split('|')[0]}] Load cookies")
   
    try:
        with open(f"{cwd}//cookies//{data.split('|')[0].split('@')[0].replace('.','')}.json", 'r') as cookiesfile:
            cookies = json.load(cookiesfile)
        for cookie in cookies:
            browser.add_cookie(cookie)
        browser.get("https://kick.com")
        wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '(//a[@href="/following"])[1]')))
        login_success = "True"
    except:
        try:
            login_acc(data)
            print(f"{date_show()} [{data.split('|')[0]}] Success login")
            login_success = "True"
        except:
            login_success = "False"
            
    
    if login_success == "True":
        try:
            
            print(f"{date_show()} [{data.split('|')[0]}] Trying to follow")
            browser.get(link)
            try:
                xpath_fast("//button[text()='Start watching']")
            except:
                pass
            try:
                xpath_long("//*[text()=' Follow']/parent::button")
                print(f"{date_show()} [{data.split('|')[0]}] Success Follow")
                sleep(5)
            except:
                print(f"{date_show()} [{data.split('|')[0]}] Failed Follow")
            sleep(2)
        except:
            print(f"{date_show()} [{data.split('|')[0]}] Failed login")
    
        browser.quit()
    
if __name__ == '__main__':
     
    print(f'{date_show()} Automation Chat')
    link = input(f'{date_show()} Input Link: ')
    # get_data = os.listdir('./cookies')
    file_list_akun = "data.txt"
    myfile_akun = open(f"{cwd}/{file_list_akun}","r")
    akun = myfile_akun.read()
    list_accountsplit = akun.split("\n")
    for i in list_accountsplit:
        login(i)
    
    # jumlah = int(input(f'{date_show()} Multi process: '))

    # with Pool(jumlah) as p:  
    #     p.map(login, get_data)