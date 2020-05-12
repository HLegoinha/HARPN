# HARPN
Legoinha is a simple function that downloads .fits spectra from HARPSN database. It creates a folder for each input star and saves inside all the availabe and free .fits spectra as well as a .txt containing the average signal to noise of all spectra donwloaded!


In order to use it it's necessary to download chrome driver or firefox driver (named geckodriver):

ChromeDriver: https://chromedriver.chromium.org/downloads

geckodriver: https://github.com/mozilla/geckodriver/releases/tag/v0.26.0 (apears in the end of the page)

After the download creat a folder named bin in the OS(C:), drop the downloaded driver.exe in there and add that folder tou yout PATH variables (in windows). 

To do this in windows: right-click on the windows icon > system > about > system info > advanced system definition >  Envoirment variables > System variables: there should be a variable named PATH. If there is no variable with that name create a new one and put there the bin folder directory. If it already exists simply add the bin folder directory puting first a ';' in case there is already a directory inside. 


The function is now ready to be used by giving the following arguments in the following order:

Mandatory:
(1) Path to download folder
(2) Browser
(3) Star List

Optionals:
(4) File type
(5) Fiber
(6) Folder


1) Path to download folder: 
It must be a string with the path to the download folder. I point out that python reads '/' instead of ordinary windows '\', so don't forget to replace them if you copy the path directly from the folder directory.


2) Browser:
This should simply be 'firefox' or 'chrome' depending on what webdriver is intaled or prefered


3) Star List:
A list containg the name of the star to be downloaded. If it is only one star it is required to be in brackts as well. e.g: ['STAR']


4) File type:
This should be a string like one of the selectable files in the HARPN form website. e.g.: 's1d'


5) Fiber:
This should be a string refering to the 'A' or 'B' fibers. e.g: 'A'


6) Folder:
This should be a string that contains the path to a folder where the downloaded files will be saved. If not specified the downloaded files will be stored in the download folder. Again, pay attetion to the '/' instead of '\'.
