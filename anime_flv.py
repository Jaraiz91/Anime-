from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By   # para elegir por elemento
from selenium.webdriver.support.ui import WebDriverWait # para el time sleep
from selenium.webdriver.support import expected_conditions as EC # condiciones esperadas
from selenium.webdriver import ActionChains as AC # acciones en cadena

from webdriver_manager.chrome import ChromeDriverManager

PATH=ChromeDriverManager().install()   #'driver/chromedriver'

opciones=Options()
opciones.add_experimental_option('excludeSwitches', ['enable-automation']) # para quitar flag de robot
opciones.add_experimental_option('useAutomationExtension', False)
opciones.add_argument('user-data-dir=selenium')  

url = 'https://www3.animeflv.net/'

#driver=webdriver.Chrome(PATH, options=opciones)
#driver.get(url)
#time.sleep(5)

def go_to_series_initial_page(series, driver):

    buscar=driver.find_element_by_xpath('//*[@id="search-anime"]')
    buscar.send_keys(series)
    time.sleep(2)
    buscar.submit()
    primer_res=driver.find_element_by_xpath('/html/body/div[3]/div/div/main/ul/li[1]/article/a')
    primer_res.click()
    pagina_inicio = driver.current_url



def start_episode(capitulo, driver):
    '''Function for all the chapter selection and video process. 
    it starts from the initial page of the previously chosen series'''
    
    sort=driver.find_element_by_xpath('//*[@id="sortEpisodes"]')
    sort.click()
    capitulos = driver.find_elements_by_class_name('fa-play-circle')
    capitulos[capitulo-1].click()
    time.sleep(2)
    #Quitarse anuncio emergente
    windows_before = driver.current_window_handle
    driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/ul/li[1]/a').click()
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    windows_after = driver.window_handles
    new_window = [x for x in windows_after if x != windows_before][0]
    driver.switch_to.window(new_window)
    driver.switch_to.window(windows_before)
    #opcion2 = driver.find_element_by_xpath('//*[@id="XpndCn"]/div[1]/ul/li[2]/a')
    #opcion2.click()
    source_code = driver.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(source_code, 'html.parser')
    video_url = soup.find('div', id='video_box').find('iframe').attrs['src']
    driver.get(video_url)
    play = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="bodyel"]/div/div/div[5]/div[2]')))
    play.click()
    time.sleep(5)
    #put full screen
    full_screen = driver.find_element_by_xpath('//*[@id="bodyel"]/div/div/div[5]/div[7]/div[4]')

    full_screen.click()

def automate_next_chapter(driver, page, current_chapter):

    while 1:
        duration = driver.find_element_by_xpath('//*[@id="bodyel"]/div/div/div[5]/div[7]/div[5]').text
        current_time = driver.find_element_by_xpath('//*[@id="bodyel"]/div/div/div[5]/div[7]/div[3]').text
        print(current_time)
        print(duration)
        if current_time == duration:
            print('\ncapítulo finalizado')
            driver.get(page)
            start_episode(driver=driver, capitulo= current_chapter +1)




def main():

    url = 'https://www3.animeflv.net/'
    serie = input('Escribe la serie de Anime que deseas ver')
    capitulo = int(input('Por qué capítulo quieres empezar?'))
    driver=webdriver.Chrome(PATH, options=opciones)
    driver.get(url)
    

    while 1:

       
        go_to_series_initial_page(serie, driver=driver)
        pagina_inicio = driver.current_url
        start_episode(capitulo=capitulo, driver=driver)
        automate_next_chapter(driver=driver, page= pagina_inicio, current_chapter=capitulo)
        capitulo += 1
            
        
        
            




if __name__ == '__main__':
    main()






