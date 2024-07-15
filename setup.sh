#!/bin/bash

# Install Node.js dependencies
npm install core-js@^3.8.3 vue@^3.2.13 --save
npm install @babel/core@^7.12.16 @babel/eslint-parser@^7.12.16 @vue/cli-plugin-babel@~5.0.0 @vue/cli-plugin-eslint@~5.0.0 @vue/cli-service@~5.0.0 eslint@^7.32.0 eslint-plugin-vue@^8.0.3 --save-dev

# Install Python dependencies
pip install fastapi python-multipart uvicorn jinja2 pydantic yt-dlp

tar -xf ffmpeg-7.0.1.tar.xz
