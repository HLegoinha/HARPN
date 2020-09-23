# HARPN
HARPN is a simple function that downloads .fits spectra from HARPSN database. It creates a folder for each input star and saves inside all the availabe free .fits spectra as well as a .txt containing the average signal to noise of all spectra donwloaded!
It returns a message showing the amount of downloaded files as soon as a star has been processed or warns the user if the star can't be found in the database. The mensage '0 files extracted' means that the star only has private spectra. 

In order to use it it's necessary to download chrome driver or firefox driver (this one is named geckodriver) for your os:

ChromeDriver: https://chromedriver.chromium.org/downloads

geckodriver: https://github.com/mozilla/geckodriver/releases/tag/v0.26.0 (apears in the end of the page)

After the download is finished, depending on your OS, you can find detailed instructions for the procedures in order to correctly use the function in the end of this README .

After following those procedures the function is ready to be used by giving the following arguments in the following order:

Mandatory:
(1) folder
(2) PATH_Driver
(3) star List

Optionals:
(4) file type
(5) fiber
(6) download


1) folder: 
This should be a string that contains the path to a folder where the downloadable files will be saved. Pay attention to the '/' instead of the backslash. In the end of the path add another '/' like this e.g. on windows 'C:/Users/Henrique Legoinha/Desktop/stars/' and this e.g. on Linux '/home/henrique/Downloads'


2) PATH_Driver:
This should simply be a string containing the path to 'geckodriver' or 'chromedriver' in your pc. 
e.g. on linux: '/home/henrique/ChromeDriver/chromedriver' or '/usr/local/bin/geckodriver',
e.g. on windows: r'C:/bin/chromedriver' or 'C:/bin/geckodriver'


3) star List:
A list containg the name of the star to be downloaded. If it is only one star it's required to be in brackets as well. e.g. ['STAR']


4) file type:
This should be a string like one of the selectable files in the HARPN form website. e.g. 's1d'


5) fiber:
This should be a string refering to the 'A' or 'B' fibers. e.g. 'A'


6) download: This should be True or False. It is, however, True by default meaning that the function will always search and download files unless download is defined to be False. In this case, the function will only perform a survey returning the name of the stars that are not recognized by the database. Those who are recognized might not be in the database.


>>> SET UP

To do this in Windows: 
Create a folder named bin in the OS(C:), drop the driver.exe in there and add that folder to your PATH variables (in Windows). Right-click on the Windows icon > system > about > system info > advanced system definition >  Enviroment variables > System variables: there should be a variable named PATH. If there is no variable with that name create a new one and put there the bin folder directory. If it already exists simply add the bin folder directory putting first ';' in case a directory already exists inside. 


To do this on Linux:
For chrome users:
Inside '/home/${user}' create a new directory “ChromeDriver”. Unzip the downloaded chromedriver into this folder. Using «chmod +x filename» make the file executable (file name is the name of the folder, ChromeDriver). Go to the folder using cd command («cd ChromeDriver») and execute the chrome driver with «./chromedriver» command.

For firefox users:
Run the following lines in the terminal

export GECKO_DRIVER_VERSION='v0.24.0'

wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz

tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz

rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz

chmod +x geckodriver

cp geckodriver /usr/local/bin/




