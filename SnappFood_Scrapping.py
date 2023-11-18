import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import pandas as pd 

URL = "https://snappfood.ir/service/restaurant/city/Tehran/near?page=0&superType=1"

headers = {
    'User-Agent': 'Chrome/68.0.3440.84',#ChromeDriver 104.0.5112.79
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


driver = webdriver.Chrome('./chromedriver')  
driver.get(URL)  

time.sleep(3)

for i in range(4): #scrole down
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)

for j in range(100): #number of time to click on more items
	for i in range(1): #scrole down
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
	driver.find_element_by_css_selector('.sc-fFubgz.kNRNFK').click()


html = driver.page_source


soup = BeautifulSoup(html,"html.parser")
#main = soup.find("main")#,class_ ="sc-citwmv")
div1 = soup.find_all("a",class_ ="VendorCard__HtmlLink-sc-6qaz7-4 cdoeYu")
#div3 = soup.find_all("p",class_ ="sc-hKgILt fYlAbO")
div3 = soup.find_all("span",class_ ="sc-hKgILt jsaCNc")
div5 = soup.find_all("p",class_ ="sc-hKgILt fYlAbO")


resturants = []
menu = []
id = 0
for i in range(len(div1)):
	resturants.append([id,div1[i]['title'],div5[i].text,div3[i].text])
	print("Resturant title = " + div1[i]['title'] + "   link = "+ div1[i]['href'])
	driver.get("https://snappfood.ir" + div1[i]['href'])
	time.sleep(1)
	html = driver.page_source
	soup = BeautifulSoup(html,"html.parser")
	div2 = soup.find_all("h2",class_ ="sc-hKgILt esHHju")
	div4 = soup.find_all("span",class_ ="sc-hKgILt hxREoh")
	
	#N= len(div5)
        #if N!=0:
           #arr=[]
	   #arr = [0 for i in range(N)]
           #print("arr:",arr)
	#div4 =  div4.append(arr)
	
        id2 = 0
        for j in range(len(div2)):
	    try:
               menu.append([id,id2,div2[j].text,div4[j].text])
            except IndexError: 
               menu.append([id,id2,div2[j].text,'null'])
	id = id+1
	id2 = id2 +1

     

resturants = pd.DataFrame(columns=('ID','resturant','voteCount','rating'),data = resturants)
menu = pd.DataFrame(columns=('resturantID','menu_id','productTitle','price'),data = menu)
resturants.to_excel('resturants.xlsx')
menu.to_excel('menu.xlsx')
