import requests
import json
import re
import typer
from typing_extensions import Annotated
import time
import os

class BaseDownloader:
	def __init__(self, json_file: str, folder: str):
		self.json_file = json_file
		self.folder = folder

	def isvalid(self, filename: str):
		"""Validates filename, true by default. May be changed by subclasses to exclude particular files."""
		return True

	def namefile(self, url: str):
		return url.split("/")[-1]
	
	def formaturl(self, url: str):
		return url

	def download(self):
		with open(self.json_file, "r") as f:
			data = json.load(f)
		entries = data["log"]["entries"]
		for entry in entries:
			try:
				u = self.formaturl(entry["request"]["url"])
				if self.isvalid(u):
					iurl = requests.get(u, stream=True) # urllib.parse.unquote(u)
					name = self.namefile(u)
					with open(f"{self.folder}/{name}", "wb+") as f:
						for chunk in iurl:
							f.write(chunk)
			except Exception as e:
				print(f"Got exception: {e}")
				input()

class TwitterImage(BaseDownloader):
	def __init__(self, json_file: str, folder: str):
		super().__init__(json_file, folder)

	def namefile(self, url: str):
		if not (url.endswith(".jpg") or url.endswith(".png") or url.endswith(".webm") or url.endswith(".jpeg")):
			url = url + ".jpg"
		return url.split("/")[-1].replace("?format=jpg", "")

class Tweet(TwitterImage):
	def __init__(self, json_file: str, folder: str, small_scale: bool = False):
		super().__init__(json_file, folder)
		self.small_scale = small_scale

	def isvalid(self, filename: str):
		return "?format=jpg" in filename

	def formaturl(self, url: str):
		thisurl = super().formaturl(url)
		if not self.small_scale:
			r = re.findall("&name=[a-zA-Z0-9]*", thisurl)
			if len(r) > 0:
				print(r[0])
				thisurl = thisurl.replace(r[0], "")
		if self.isvalid(thisurl):
			print(thisurl)
		return thisurl

class InstagramImage(BaseDownloader):
	def __init__(self, json_file: str, folder: str):
		super().__init__(json_file, folder)
	
	def namefile(self, url):
		url = super().namefile(url)
		return url.split("?")[0]
	
	def isvalid(self, filename):
		return (not "scontent" in filename and not "?stp=dst-webp_s" in filename)

def picdown(
	sourcefile: str = "",
	folder: str = f"temp{int(time.time())}",
	sns: str = "default"
):
	if sourcefile == "":
		return print("[!] No source file specified")
	if not os.path.isdir(folder):
		os.mkdir(folder)
	mingdownloader: BaseDownloader = None
	print(sns)
	match sns:
		case "twitter" | "x" | "twt":
			print("Starting Twitter pic downloader...")
			mingdownloader = Tweet(sourcefile, folder)
		case "instagram" | "insta":
			print("Starting Instagram pic downloader...")
			mingdownloader = InstagramImage(sourcefile, folder)
		case _:
			print("Starting generic downloader...")
			mingdownloader = BaseDownloader(sourcefile, folder)
	mingdownloader.download()