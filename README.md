# TheFootballFanApp
A passion project dedicated towards the Bulgarian Football Fan providing all neccesarry information about his favorite team. The website includes information about matches, travel tips and more.


## Current version runthrough
The current version of the project allows the user to check in with the latest results and gather information about the next fixture of his favorite team, including travel location and estimated travel time by car, which is adjusted according to expected traffic. Future versions of the project will compare prices with different alternatives (traveling by train using data from the БДЖ website), aiming to give the user the full picture of how you can best get to the next game. Currently the website interface is very plane and basic, but future updates will give it more of a modern look.

![HomePage](https://user-images.githubusercontent.com/71731579/193261077-7c1854fe-e440-48ae-ac99-20d3ff3718ec.PNG)
![TeamPage](https://user-images.githubusercontent.com/71731579/193261098-cbaedcfd-e309-4e82-9b9d-9bb932d6b377.PNG)
![TravelPage](https://user-images.githubusercontent.com/71731579/193261103-c5a2a9f6-7c1a-420b-be36-5cf890a8d214.PNG)


## How the project is build
This project is build by using 2 webscraping libraries- beautifulsoup4 and selenium. These libraries allow reliable data from different websites to be extracted. Unfortunately with webscraping, scraping large amounts of data from different sources slows the website down. For now the damage is combated with multiprocessing, but the website is still pretty slow for modern day standards. Further improvements will be made in future updates.


## Main Sources of information
As this is my first Django project built from scratch I went through a lot of articles, videos and StackOverflow questions. Here is a short list of some of the links that helped me out majorly during the project build up:
- https://www.youtube.com/watch?v=Xjv1sY630Uc&t=4s&ab_channel=TechWithTim
- https://www.digitalocean.com/community/tutorials/python-multiprocessing-example
- https://www.youtube.com/watch?v=RvCBzhhydNk&t=925s&ab_channel=Pythonology
- https://stackoverflow.com/questions/68749127/web-scraping-accept-cookies-selenium-python-airbnb
- https://www.youtube.com/watch?v=gXLjWRteuWI&t=704s&ab_channel=DesignCourse
- https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data
- https://www.w3schools.com/tags/att_input_type_hidden.asp


## Websites from which data has been scraped
- https://www.livescore.com/en/
- https://www.flashscore.com/
- https://int.soccerway.com
- https://www.bing.com/maps


## Virtual Environment Setup
The following project was set up on a conda venv, due to some unexpected issues with pip, but the latter could also be used.

### Installing conda
Here is a brief installation guide:
1) Download the anaconda version according to your Operating System (https://www.anaconda.com/products/distribution)
2) Run through the anaconda installer
3) Open the terminal and type in the following command to create a new virtual environment

![conda_crt_venv](https://user-images.githubusercontent.com/71731579/193061314-ff8a9de5-1539-4e52-b888-42b7c5b625bd.PNG)

You may need to pass in at least 1 starting package in your newly created venv.

![conda_crt_venv_2](https://user-images.githubusercontent.com/71731579/193061968-2710b61c-2b4d-4e6e-9f91-d7f1a51e5ac8.PNG)

4) Afterwards you need to activate your new env with the following command

![conda_act_venv](https://user-images.githubusercontent.com/71731579/193062061-f3d0b302-e409-476b-8cd2-8ad37711109d.PNG)

You can watch the following video as a reference guide(https://www.youtube.com/watch?v=YJC6ldI3hWk&t=406s&ab_channel=CoreySchafer). 

### Installing packages
A list with the required libraries for installation can be found in the Requirements.txt file. 
This list is expected to grow with upcoming updates.
Here, an example installation with one of the packages is shown:

![conda_pck_instl_ex](https://user-images.githubusercontent.com/71731579/193052792-542e7965-0fa3-4983-aab7-af72fdb6e407.PNG)

To install any package in an already existing conda venv, simply replace the last word (in this case 'selenium') with the package that you need to install.

To check if a package already exists in your virtual environment, type the following command:

![conda_lst_pckg](https://user-images.githubusercontent.com/71731579/193062178-75be49af-4b78-410a-a02b-b3a8ac396c1d.PNG)

This is the command to install any package if you choose to use pip

![pip_install](https://user-images.githubusercontent.com/71731579/193228762-5819ccb7-3950-4af6-89a9-97ed57283973.PNG)

## Chromedriver setup 
1) Open Google Chrome WebBrowser
2) Navigate yourself to the About Chrome page and check in your current version
3) Download the correct version of ChromeDriver from the link provided (https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbEt3Z2Z4QVdja3N4VTFPT0tLNnBlY1c1el9Rd3xBQ3Jtc0trbW95NlhTbS1wOTYyR3dqNE9CaTYtUmNtbklSUE1wRmZPaF9pR2prd3hQN0FucEJkRk1YZndKWVg2X0xLTnlGeEkzTHZPVXN2Rm9GVHlzN3doMkZoQV9vN1ZaUE45a2YyV1hyc0hUS2ZOSnYtcy1aNA&q=https%3A%2F%2Fsites.google.com%2Fa%2Fchromium.org%2Fchromedriver%2Fdownloads&v=Xjv1sY630Uc)
4) Extract and copy the file to 'C:\Program Files (x86)\' and paste the chrome file there

## Future plans
- bug fixes
- code optimization
- reduce page loading time
- adding features and webpages
- design improvements
- implementation with the БДЖ website
- replace bing maps with google maps
