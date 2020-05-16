from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import gzip
import shutil
import os
import time
import wget
import astropy
import numpy as np
from astropy.io import fits
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def HARPN(path_donwload_folder, internet, target, fiber=None, file_type=None, folder=None, download=True):
       
    #Following if's open the respective browser in silence mode and go to the TNG form website
    if internet == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = False
        browser = webdriver.Chrome(options=chrome_options, executable_path=r'C:/bin/chromedriver') #<- !! INSERT PATH TO CHROME DRIVER
        browser.get('http://archives.ia2.inaf.it/tng/faces/search.xhtml?dswid=3397')
    if internet == 'firefox':
        os.environ['MOZ_HEADLESS'] = '1'      
        browser = webdriver.Firefox(executable_path='C:/bin/geckodriver')                          #<- !! INSERT PATH TO GECKO DRIVER
        browser.get('http://archives.ia2.inaf.it/tng/faces/search.xhtml?dswid=3397')
        time.sleep(1) #time to make sure HTML is up to date
    
    if download == True:
        #open single instrument panel
        browser.find_element_by_id('main:j_idt219').click()
        time.sleep(1) #time to make sure HTML is up to date  

        browser.find_element_by_id('main:j_idt225').click()
        time.sleep(1) #time to make sure HTML is up to date

        #fiber A or B
        browser.find_element_by_id('main:FIBER_2').send_keys(fiber)
        #file_type
        browser.find_element_by_id('main:FILE_TYPE_REDUCED').send_keys(file_type) 

        for i in target: 
            #target object
            objectt = browser.find_element_by_name('main:OBJECT')
            objectt.send_keys( Keys.CONTROL + "a" )
            objectt.send_keys(str(i) + Keys.ENTER)                 
            WebDriverWait(browser, 20).until(EC.staleness_of(objectt))
            
            #total number of results
            HTML = BeautifulSoup(browser.page_source, 'html5lib')
            for e in HTML.find_all('p'):
                if str(e)[:16] == '<p>Total results':
                    num_results = (int(str(e)[17:-4]))
            
            #Check if the Star has been found on the database:
            if num_results != 0:  

                #hit the blue download button
                wait = WebDriverWait(browser, 30)
                wait.until(EC.element_to_be_clickable((By.ID, 'download-dropdown'))).click()
                time.sleep(1)
                
                #hit download button relative to .txt files
                browser.find_element_by_id('main:j_idt667').click()
                
                #click the files_menu
                files_menu = wait.until(EC.element_to_be_clickable((By.ID, 'files-menu')))
                time.sleep(10)
                files_menu.click()
                #identify the file name being clicked in the files menu
                HTML = BeautifulSoup(browser.page_source, 'html5lib')
                for link in HTML.find_all('a'):
                    href = str(link.get('href'))      
                    if 'http://archives.ia2.inaf.it/user_space/tng' in href:
                        nome = str(href[-25:])   
                        break

                #donwload the .txt in the files menu
                wget.download(href, path_donwload_folder)      

                #create a folder for upcoming downloads
                if folder == None:
                    folder = path_donwload_folder + '/'
                if os.path.exists(folder + str(i)):
                    shutil.rmtree(folder + str(i))
                os.makedirs(folder + str(i))

                #open .txt downloaded file and get .gz files (wich contain the .fits files of interest)
                file = open(path_donwload_folder + '/' + str(nome))
                for linha in file:
                    try:   
                        wget.download(linha[:-1] , folder + str(i)) #last element is always garbage
                    except HTTPError:           #in case they are private the loop continues
                        continue    
                file.close()

                #exctrat .FITS files out of the gz files
                folder_i = folder + str(i)
                n_spectra = len(os.listdir(folder_i))
                for e in os.listdir(folder_i):
                    with gzip.open(folder_i + '/' + e , 'rb') as f_in:
                        with open( folder_i + '/' + e[:-3] , 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(folder_i + '/'+ e)   #remove unnecessary .gz files                               
                #number of free spectra extracted
                print(i + ': ' + str(n_spectra) + ' free spectra extracted')

                #SIGNAL_NOISE of downloaded spectra:
                testeDic = {}
                Lista = np.zeros(69)
                for e in os.listdir(folder_i):
                    ficheiro_e = fits.open( folder_i + '/' + str(e))
                    L=[]
                    for r in range(69):
                        valor = (ficheiro_e[0].header['HIERARCH TNG DRS SPE EXT SN' + str(r)])**2
                        L.append(valor)
                    Lista = Lista+L
                    ficheiro_e.close()
                for r in range(69):
                    testeDic.update({'SN' + str(r) : np.sqrt(Lista[r])})

                with open(folder_i + '/SIGNAL_NOISE.txt', 'w') as f:
                    for key, value in testeDic.items():
                        f.write('%s:%f\n' % (key, value))
                f.close()
                #testeDic

                if n_spectra == 0: #remove created folder for cases with 0 free spectra
                    shutil.rmtree(folder_i)

            #in case the star is not in the database
            if num_results == 0:  
                print( i + ': not in database')

        print('DONE!')       
        #close session in the headless browser
        browser.quit()
    
    #performs a survey of the given stars
    if download == False:
        estrelas_nao_reconhecidas=[]
        for i in target:
            
            element = browser.find_element_by_id('main:j_idt104:name-resolver-text')
            element.send_keys(Keys.CONTROL + "a" )
            element.send_keys(str(i) + Keys.ENTER)
            WebDriverWait(browser, 10).until(EC.staleness_of(element))
            
            HTML = BeautifulSoup(browser.page_source, 'html5lib')
            for element in HTML.find_all('input'):
                if element.get('id')=='main:j_idt104:ps_ra':
                    v=element.get('value')
                    if element.get('value') == None:
                        estrelas_nao_reconhecidas.append(i)
            
        browser.quit()
        k=(len(estrelas_nao_reconhecidas))
        print('Stars not recognized: ' + str(k))
        if k > 0: print(estrelas_nao_reconhecidas)
            
        
    
    
    
