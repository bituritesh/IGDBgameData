# GameDataGsheet

### gameDataGsheet POC
- **gameDataGsheet POC** written using Python3. The current implementation supports Containing data related to various games present online in IGDB.

About the project -
This project has 2 data-gathering parts -
1. using the IGDB API endpoint: ```https://api.igdb.com/v4/games``` and write to the gsheet.
2. Using Beautiful Soup to crawl the web, extract the genre, and write to the gsheet.

To gather data from the API into the gsheet run:
```commandline
   python3 sheetWriter.py
   ```

To scrap genre data from the IGDB game website and insert it into gsheet run:
```commandline
   python3 IGDBGenreScrapper.py
   ```

Endpoints at - https://api-docs.igdb.com/#endpoints

---------------------------------------------------------------------------------------------------------------------------------------------------------

### How to set this service up locally
1. Clone the repository using:
      ```commandline
      git clone https://github.com/bituritesh/IGDBgameData.git
      ```
2. Once the repository is cloned. Change directory `cd` to the repository you cloned (gameGenrePredictor/) via the following command:
   ```commandline
   cd gameGenrePredictor/
   ```
3. We expect you to have `Python 3.9 or greater` installed on your machine.

4. Create a new virtual environment python3 -m venv venv

5. Activate this virtual environment using: 

   ```commandline
   source venv/bin/activate
   ```
6. Resolve the dependencies by installing them using(currently we don't have any): 
   
      ```commandline
      pip3 install -r requirements.txt
      ```
7. After installing playwright from `requirements.txt` you need to run this command to install the chromium-browser -

     ```commandline
      python3 -m playwright install chromium
      ```
      
7. After the dependencies are resolved if any. You can run the genre collector script by running the following command, make sure you are present at the current directory of the `IGDBGenreScrapper.py` script:
   
   ```commandline
   python3 IGDBGenreScrapper.py
      ```

# Troubleshooting and Enhancements:
  1. If any error is caused due to building wheels for `greenlet` use `xcode-select --install` to install the latest cli tools for MAC.
  2. Adding a logger, use ```loguru``` package instead of using ```print("")``` everytime, this will help sending the logs to a logging system if a need arises for someone.
  3. I will update ```README.md``` as the project progresses.

-------------------------------------------------------------------------------------------------------------------------------------------------------

Created an API under the folder gameDataAPI, this API is exposed with the collected data from above.

API route - ```http://127.0.0.1:8000/game-data/?game_id=```

```game_id``` - a query parameter, that takes the unique ID for every game in the IGDB database.

The response of this API returns - the game data present in the sheet.

Run the mains.py app > ```uvicorn mains:appName --reload```

Follow the link for the localhost and ```http://127.0.0.1:8000/docs``` to test the APIs with swagger UI

git handling - 
git status
git push
https://chat.openai.com/share/93fe312e-6290-4d59-85b8-0d14e3032037
https://gist.github.com/mindplace/b4b094157d7a3be6afd2c96370d39fad

--------------------------------------------------------------------------------------------------------------------------------------------------------

after installing playwright from requirements.txt you need to run this command to install the chromium browser `python3 -m playwright install chromium`
