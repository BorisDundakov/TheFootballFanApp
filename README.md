# TheFootballFanApp

A passion project dedicated towards the Bulgarian Football Fan providing all neccesarry information about his favorite team. The website includes information about matches, travel tips and more.


## Current version runthrough
The current version of the project allows the user to check in with the latest results and gather information about the next fixture of his favorite team, including travel location and estimated travel time by car, which is adjusted according to expected traffic. Future versions of the project will compare prices with different alternatives (traveling by train using data from the БДЖ website), aiming to give the user the full picture of how you can best get to the next game. Currently the website interface is very plane and basic, but future updates will give it more of a modern look.

![HomePage](https://user-images.githubusercontent.com/71731579/193261077-7c1854fe-e440-48ae-ac99-20d3ff3718ec.PNG)
![TeamPage](https://user-images.githubusercontent.com/71731579/193261098-cbaedcfd-e309-4e82-9b9d-9bb932d6b377.PNG)
![TravelPage](https://user-images.githubusercontent.com/71731579/196380017-2fb01093-76e2-4ab6-8a64-9d442a64a3b4.PNG)


## How the project is build
This project is build by using 2 webscraping libraries - beautifulsoup4 and selenium. These libraries allow reliable data from different websites to be extracted. Unfortunately with webscraping, scraping large amounts of data from different sources slows the website down. For now the damage is combated with multiprocessing, but the website is still pretty slow for modern-day standards. Further improvements will be made in future updates.


## Websites from which data has been scraped
- https://www.livescore.com/en/
- https://www.flashscore.com/
- https://int.soccerway.com
- https://www.bing.com/maps


## Virtual Environment Setup
The following project was set up on a conda venv, due to some unexpected issues with pip, but the latter could also be used.

### Installing conda
1) Download the anaconda version according to your Operating System (https://www.anaconda.com/products/distribution)
2) Run through the anaconda installer
3) Open the terminal and type in the following command to create a new virtual environment

![conda_crt_venv](https://user-images.githubusercontent.com/71731579/193265365-f2fee44c-1aad-47ca-9ad9-20d289b4047f.PNG)

You may need to pass in at least 1 starting package in your newly created venv.

![conda_crt_venv_2](https://user-images.githubusercontent.com/71731579/193265398-49a82519-2b5b-4d0f-9d00-bb769f304d37.PNG)

4) Activate your new environment with the following command

![conda_act_env](https://user-images.githubusercontent.com/71731579/193265477-1d38116b-a332-4a9a-9936-a6b9629a11b6.PNG)


### Installing packages
A list of the required libraries for installation can be found in the Requirements.txt file. 
This list is expected to grow with upcoming updates.
Here, an example installation with one of the packages is shown:

![conda_pck_instl_ex](https://user-images.githubusercontent.com/71731579/193265590-2c27a5fb-58d3-447c-9ee9-7cda1eb73cea.PNG)

To install any package in an already existing conda venv, simply replace the last word (in this case 'selenium') with the package that you need to install.

To check if a package already exists in your virtual environment, type the following command:

![conda_lst_pckg](https://user-images.githubusercontent.com/71731579/193265629-ef2f3a04-ab57-4d28-b441-ea82c5fa9c41.PNG)

This is the command to install a package if you choose to use pip. To install any package in an already existing conda venv, simply replace the last word (in this case 'geocoder') with the package that you need to install.

![pip_instl_pckg](https://user-images.githubusercontent.com/71731579/193265670-b2a6cf2f-ac5d-4bbe-aaba-6c3bd409e1e4.PNG)


## Chromedriver setup 
1) Open Google Chrome WebBrowser
2) Navigate yourself to the About Chrome page and check in your current version
3) Download the correct version of ChromeDriver from the link provided (https://sites.google.com/a/chromium.org/chromedriver/downloads)
4) Extract and copy the file to 'C:\Program Files (x86)\' and paste the chrome file there


## Future plans
- bug fixes
- code optimization
- reduce page loading time
- adding features and webpages
- design improvements
- implementation with the БДЖ website
- replace bing maps with google maps
