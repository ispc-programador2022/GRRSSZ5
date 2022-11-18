from bs4 import BeautifulSoup 
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import re
from time import gmtime, strftime

def get_twitter_trends_to_dict(driver):

    content=driver.page_source.encode('utf-8').strip()

    ## se utiliza BeautifulSoup para tomar el html
    soup = BeautifulSoup(content,"lxml")

    parent_list=soup.find_all("div", class_="css-1dbjc4n r-1loqt21 r-6koalj r-1ny4l3l r-ymttw5 r-1f1sjgu r-o7ynqc r-6416eg")
    tops=[]
    tittles=[]
    twits=[]
    for parent in parent_list:
        tops.append(parent.find("div", {"class":"css-1dbjc4n r-1d09ksm r-18u37iz r-1wbh5a2"})) 
        tittles.append(parent.find("div",{"class":"css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0"}))
        twits.append(parent.find("div", {"class":"css-901oao r-14j79pv r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-14gqq1x r-bcqeeo r-qvutc0"}))

    trending_toppic_dict=[]

    #se divide la lista en cada una de las etiquetas, tomando unicamente el texto de la misma.
    for i in range(len(tops)):
        trend=[]

        trend.append(int(re.findall('[0-9]+',tops[i].text)[0]))

        trend.append (tittles[i].text)
        try: 
            if re.search("[0-9]",twits[i].text):
                if re.search("K",twits[i].text):
                    try:
                        trend.append((int(re.findall('[0-9]+',twits[i].text)[0])*1000+int(re.findall('[0-9]+',twits[i].text)[1])*100))
                    except:
                        trend.append(int(re.findall('[0-9]+',twits[i].text)[0])*1000)
                else:
                    try:
                        trend.append(int(re.findall('[0-9]+',twits[i].text)[0])*1000+int(re.findall('[0-9]+',twits[i].text)[1]))
                    except:
                        trend.append(int(re.findall('[0-9]+',twits[i].text)[0]))
        except: 
            trend.append (None)
        
        trend.append(strftime("%Y-%m-%d", gmtime()))
        trend.append(strftime("%H:%M:%S", gmtime()))
        
        trending_toppic_dict.append(trend)
           

    return trending_toppic_dict


def trending_toppic ():
     ## optiones para no abrir la ventana al ejecutar el programa
    option = webdriver.EdgeOptions()
    option.add_argument('--headless')

    ##ejecusión del driver, si se quita el parámetro "options" se abrirá la ventana del browser
    driver = webdriver.Edge("./drivers\msedgedriver.exe",options=option )#, 

    ##Se toma el url de la página a scriptar y se determina el código de caracteres, para el español sería utf-8
    url = driver.get('https://twitter.com/explore/tabs/trending')

    sleep(5)

    trending_toppic = get_twitter_trends_to_dict(driver)

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        
        trending_toppic_2=get_twitter_trends_to_dict(driver)
        i=0
        while (True):
            j=trending_toppic_2[i][0]
            try:
                if trending_toppic[j-i-1][0]==trending_toppic_2[0][0]:
                    del trending_toppic_2[0]

            except:
                 trending_toppic+=trending_toppic_2
                 return trending_toppic
            i=+1

print (trending_toppic ())