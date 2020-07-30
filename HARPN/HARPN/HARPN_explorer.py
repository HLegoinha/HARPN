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
import numpy as np
from astropy.io import fits
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


def HARPN(folder, PATH_DRIVER, target, fiber=None, file_type=None, download=True):
       
    #Following if's open the respective browser in silence mode and go to the TNG form website
    if PATH_DRIVER[(len(PATH_DRIVER)-12):] == 'chromedriver':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        browser = webdriver.Chrome(options=chrome_options, executable_path= PATH_DRIVER) 
        browser.get('http://archives.ia2.inaf.it/tng/faces/search.xhtml?dswid=3397')
    if PATH_DRIVER[(len(PATH_DRIVER)-11):] == 'geckodriver':
        os.environ['MOZ_HEADLESS'] = '0'      
        browser = webdriver.Firefox(executable_path = PATH_DRIVER)
        browser.get('http://archives.ia2.inaf.it/tng/faces/search.xhtml?dswid=3397')
        time.sleep(1) #time to make sure HTML is up to date
    
    
    if download == True:
        #open single instrument panel
        browser.find_element_by_id('main:j_idt219').click()
        time.sleep(1) #time to make sure HTML is up to date  
        
        #HARPN
        browser.find_element_by_id('main:j_idt225').click()
        time.sleep(1) #time to make sure HTML is up to date

        #fiber A or B
        browser.find_element_by_id('main:FIBER_2').send_keys(fiber)
        
       #file_type
        HTML = BeautifulSoup(browser.page_source, 'html5lib')
        for line in HTML.find_all('select'):
            if line.get('id') == 'main:FILE_TYPE_REDUCED':
                contador=0
                for ii in line:
                    x = str(ii)
                    palavraa = x[17+len(file_type):-9]
                    if len(x) > 30:
                        contador+=1
                    if palavraa == file_type:
                        n_times = contador-1
        for i in range(n_times):
            browser.find_element_by_id('main:FILE_TYPE_REDUCED').send_keys(Keys.DOWN)
        
        #ignore TBL files
        browser.find_element_by_id('main:TBL_FILE').send_keys('oo')
              
        counter=1 #in order to count the stars already processed
        for i in target: 
            #target object (using resolver and search btn)
            objectt = browser.find_element_by_name('main:j_idt104:name-resolver-text')
            objectt.send_keys( Keys.CONTROL + "a" )
            objectt.send_keys(str(i) + Keys.ENTER)                 
            WebDriverWait(browser, 20).until(EC.staleness_of(objectt))
 
            browser.find_element_by_id('main:search-btn').click()
            WebDriverWait(browser, 20).until(EC.staleness_of(browser.find_element_by_id('main:search-btn')))        

            #star identified? if yes get number of results
            HTML = BeautifulSoup(browser.page_source, 'html5lib')
            for element in HTML.find_all('input'):
                if element.get('id')=='main:j_idt104:ps_ra':
                    if element.get('value') != None:  #check if the object has values for its coordinates
                        for e in HTML.find_all('p'):
                            if str(e)[:16] == '<p>Total results':
                                num_results=(int(str(e)[17:-4]))
                                if num_results != 0: #check if the number of results are diferent than zero
                                    
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
                                   
                                    #create a folder for upcoming downloads
                                    if os.path.exists(folder + str(i)):
                                        shutil.rmtree(folder + str(i))
                                    os.makedirs(folder + str(i)) 
                                    
                                    
                                    #donwload the .txt in the files menu
                                    wget.download(href, folder)                                   
                            
                            
                                    #open .txt downloaded file and get .gz files (wich contain the .fits files of interest)
                                    file = open(folder + '/' + str(nome))
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
                                    
                                    print(str(counter)+')  '+ i + ': ' + str(n_spectra)+'/'+ str(num_results) + ' spectra extracted')
                                    counter +=1
                                    #SIGNAL_NOISE of downloaded spectra:
                                    Dic = {}
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
                                        Dic.update({'SN' + str(r) : np.sqrt(Lista[r])})

                                    with open(folder_i + '/SIGNAL_NOISE.txt', 'w') as f:
                                        f.write(i + ': ' + str(n_spectra)+'/'+ str(num_results) + ' free spectra extracted\n')
                                        for key, value in Dic.items():
                                            f.write('%s:%f\n' % (key, value))
                                    f.close()

                                    #remove created folder for cases with 0 free spectra
                                    if n_spectra == 0:
                                        shutil.rmtree(folder_i)
                                    #remove unecessary .txt files
                                    os.remove(folder + '/'+ nome)

                                #in case the star is not in the database (but is recognized)
                                if num_results == 0:  
                                    print(str(counter)+')  '+ i + ': not in database')
                                    counter +=1

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
                    if element.get('value') == None:
                        estrelas_nao_reconhecidas.append(i)

        browser.quit()
        k=(len(estrelas_nao_reconhecidas))
        print('Stars not recognized: ' + str(k))
        if k > 0: print(estrelas_nao_reconhecidas)
            
