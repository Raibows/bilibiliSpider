from selenium import webdriver
from bs4 import BeautifulSoup
opt = webdriver.ChromeOptions()
opt.add_argument('--headless')
browser = webdriver.Chrome(executable_path=r"C:\Users\Raibows\Downloads\chromedriver_win32\chromedriver.exe",
                           chrome_options=opt)
browser.get('https://zh.moegirl.org/Awsl')
html = browser.page_source
browser.close()
soup = BeautifulSoup(html)
temp = soup.find_all('div', {
    'class':'mw-parser-output'
})
print(temp)
print('fuck-----------------------------------')
print(temp[-1:-16:-1])