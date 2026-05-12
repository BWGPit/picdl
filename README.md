## About this project
_What you see is what you get_

**To avoid malicious or unwanted scrapers**, this project lets you save the images you have already seen in your browsing session, and just **avoids you the tedious work** of manually right click & save a bunch of images. You can see it as an automation of the former procedure.

### Installation
_Requires pipx_
```bash
cd executable
pipx install .
```

### Usage
Navigate through the desired web page with your browser and open `Devtools`, then select the `Network` tab and filter by `Img`. Open the images you want to save as you normally do to just see them, and select the `Export HAR (sanitized)` icon on the top of the filter bar. Save the HAR file as a JSON file (just renaming it to `.json` works).

Now open your terminal and use `picdl` as follows.
```bash
picdown --sourcefile "PATH/TO/THE/FILE/YOU/JUST/SAVED"
```
By default, the images will be downloaded in a folder called `temp[timestamp]`, but you can change the destination folder with the argument `--folder "PATH/TO/FOLDER"`. Additionally, if you want specific support (or more precise results) for a social network (currently, X/Twitter and Instagram are supported), you can use `--sns twitter` or `--sns instagram`.

### Disclaimer
This project is intended for good and reasonable use. The user is responsible for how they use this code.