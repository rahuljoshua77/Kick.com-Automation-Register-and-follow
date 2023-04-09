from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import os, random, time
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import warnings,json
import undetected_chromedriver as uc
options = uc.ChromeOptions()

from faker import Faker
fake = Faker() 
warnings.filterwarnings("ignore", category=DeprecationWarning) 
cwd = os.getcwd()
 

options.add_argument(f'--load-extension=C:\Project\BLIBLI\Buster-Captcha-Solver-for-Humans')
options.add_argument('--disable-popup-blocking')
options.add_argument("--start-fullscreen")
options.add_argument("--start-maximized")

def date():
    date = f"[{time.strftime('%d-%m-%y %X')}]"
    return date

def xpath_fast(el):
    element_all = wait(browser,3).until(EC.presence_of_element_located((By.XPATH, el)))
    return browser.execute_script("arguments[0].click();", element_all)

def xpath_type(el,mount):
    return wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el))).send_keys(mount)

def xpath_el(el):
    element_all = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, el)))
    
    return browser.execute_script("arguments[0].click();", element_all)

def get_email():
    browser.execute_script("window.open('','');") 
 
    browser.switch_to.window(browser.window_handles[1])
    browser.get('https://www.emailnator.com/')
    sleep(2)
    try:
        xpath_el('//button[@id="close-btn-ann"]')
    except:
        pass
    xpath_el('//input[@name="plusGmail"]')
    xpath_el('//input[@name="domain"]')
    xpath_el('//button[@class="btn-lg form-control mb-2 btn btn-primary"]')
    sleep(7)
    email = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Email Address"]'))).get_attribute('value')
    xpath_el('//button[@class="btn-lg btn btn-primary"]')
    browser.switch_to.window(browser.window_handles[0])
    return email

def getOtp():
    browser.switch_to.window(browser.window_handles[1])
    browser.refresh()
    sleep(2)

    url_1 =  wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//td[text()="Kick <noreply@email.kick.com>"]/ancestor::a'))).get_attribute('href')
    browser.get(url_1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(5)
    otp = wait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//strong'))).text
    return otp

def open_browser():
 
    global browser     
    random_angka = random.randint(100,999)
    random_angka_dua = random.randint(10,99)
    #opts.add_argument(f"--user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Mobile Safari/537.36")
    browser = uc.Chrome(options=options,driver_executable_path="./chromedriver.exe",use_subprocess=True)
    
    browser.get('https://kick.com/')
    
    xpath_el('//button[@type="button" and text()="Accept"]')
    sleep(1)
    xpath_el('//button[@id="signup-button"]')
    sleep(1)
    print(f"[+]  {date()} Getting Mail")
    email = get_email()
    xpath_type('//input[@id="email"]',email)
    sleep(1)
    print(f"[+]  {date()} Email found: {email}")
    xpath_el('//button[@id="headlessui-listbox-button-5"]')
    sleep(1)
    xpath_el(f'//li[@value="{random.randint(1,6)}"]')
    sleep(1)
    xpath_el('//button[@id="headlessui-listbox-button-7"]')
    sleep(1)
    xpath_el(f'//li[@value="{random.randint(1,6)}"]')
    sleep(1)
    xpath_el('//button[@id="headlessui-listbox-button-9"]')
    sleep(1)
    xpath_el(f'//li[@value="200{random.randint(1,6)}"]')
    sleep(1)
    xpath_type('//input[@id="username"]',f"{str(fake.first_name()).lower()}{random_angka_dua}{random_angka_dua}")
    sleep(1)
    xpath_type('//input[@id="password"]','Hoki2022-')
    sleep(1)
    xpath_type('//input[@id="password_confirmation"]','Hoki2022-')
    sleep(1)
    print(f"[+]  {date()} Submit Data")
    
    xpath_el('//button[@type="submit"]')
    tries = 1
    status = "False"
    sleep(5)
    while True:
        if tries == 30:
            status = "False"
            break
        try:
            print(f"[+]  {date()} Getting OTP")
            otpz = getOtp()
            print(f"[+]  {date()} OTP Found: {otpz}")
            browser.switch_to.window(browser.window_handles[0])
            status = "True"
            break
        except Exception as e:
            sleep(2)
            tries = tries + 1
            pass
        
    if status == "True":
        for index, value in enumerate(otpz):
            
            xpath_type(f'//input[@id="digit{index+1}"]',value)
            sleep(1)
        sleep(10)
        xpath_el('//button[@class="btn relative btn btn-primary btn-block mt-5"]')
        print(f"[+]  {date()} Checking Captcha")
        sleep(10)
        try:
            wait(browser,15).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//iframe[contains(@title,"recaptcha")]')))
            wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]'))).click()
            sleep(15)
            print(f"[+]  {date()} Solving Captcha")
            while True:
                try:
                    wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]'))).click()
                    print(f"[+]  {date()} Captcha Clear")
                    sleep(1)
                    el = wait(browser,1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]')))
                    browser.execute_script("arguments[0].click();", el)
                    sleep(1)
                    wait(browser,1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]'))).click()
                except:
                    try:
                        sleep(1)
                        wait(browser,1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]'))).click()
                        sleep(1)
                        wait(browser,1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="button-holder help-button-holder"]'))).click()
                        break
                    except:
                        break
                try:
                    browser.switch_to.default_content()
                except:
                    pass
            try:
                browser.switch_to.default_content()
            except:
                pass
        except Exception as e:
            print(f"[+]  {date()} Captcha Clear")
            pass
    try:
        browser.switch_to.default_content()
    except:
        pass
    try:
        wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '(//a[@href="/following"])[1]')))
        print(f"[+]  {date()} Registration done")
        cookies = browser.get_cookies()
        if os.path.exists(f'{cwd}/cookies') == False:
            os.mkdir(f'{cwd}/cookies')
        with open(f'{cwd}\\cookies\\{email.split("@")[0].replace(".","")}.json', 'w', newline='') as outputdata:
            json.dump(cookies, outputdata)
        with open('success.txt','a') as f:
            f.write(f"{email}|Hoki2022-")
    except:
        print(f"[+]  {date()} Registration failed")
    browser.quit()

open_browser()