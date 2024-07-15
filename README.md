# YotubeConverter
A webapp allowing users to download video and audio files of differening qualities.
# Prerequisites
* Anaconda
* Vscode
* [FFMPEG](https://ffmpeg.org/ "@embed")
* Zip File unziper
# Setup
  Install the following libraries below in a venv or an Anaconda env. Unzip FFMPEG, and drop in the same directory as the Readme.md file.
# Setup
  ```
    ./setup.sh
    ./start.sh
  ```
# Install libraries
```
npm install core-js@^3.8.3 vue@^3.2.13 --save
npm install @babel/core@^7.12.16 @babel/eslint-parser@^7.12.16 @vue/cli-plugin-babel@~5.0.0 @vue/cli-plugin-eslint@~5.0.0 @vue/cli-service@~5.0.0 eslint@^7.32.0 eslint-plugin-vue@^8.0.3 --save-dev

```
```
pip install fastapi python-multipart uvicorn jinja2 pydantic yt-dlp
```
# Launching the webapp
In a terminal and at the root directory of the code space run the following commands.
```
python3 app.py
```
This will start the backend side code for the api calls. Open another terminal and run the following commands to start the frontend.

```
cd YoutubeConverter
```
This should brin you into YoutubeConverter directory from there run.

```
npm run serve
```
