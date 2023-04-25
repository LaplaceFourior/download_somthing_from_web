import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin


# Get the directory where the Resources.py file is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the all-file.json file
file_path = os.path.join(dir_path, "all-file.json")

def _get_redirect_file(href):
    try:
        r = requests.get(url=href, allow_redirects=True)
        if r.history:
            return r.url
        else:
            return None
    except requests.exceptions.RequestException:
        return None






class Resources:
    def __init__(self, url):
        self.url = url
        # use for download   
        self.links = {}
        self.file_formats = None
        self.response = None
        # Open the file
        with open(file_path, "r") as f:
            try:
                self.file_formats = json.load(f)
            except json.JSONDecodeError:
                raise json.JSONDecodeError("Failed to decode JSON file", "", 0)

    def set_url(self,url):
        self.url = url

    def get_links(self):
        return self.links

    def get_download_url(self,key,index):
        urls = []
        if 0 in index:
            index.remove(0)
        for i in range(len(index)):
            index[i] -= 1
        for i in index:
            urls.append(self.links[key][i])
        return urls

    def find_downloadable_links(self):
        print("start analysising the url: ",self.url)
        response = requests.get(self.url)
        self.response = response
        print("analysis url: ",self.url,"successfully")
        print("start finding target resources")
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                print(href)
                self._add_href_to_links(href)

    def _add_href_to_links(self, href):
        for key in self.file_formats:
            if href.endswith(key):
                # the real href of href
                real_href = urljoin(self.response.url, href)
                format_str = str(key)
                if format_str in self.links:
                    # there is a key about this format in the dict
                    self.links.get(format_str).append(real_href)
                    print(real_href)
                else:
                    # there is no key about this format in the dict
                    self.links[format_str] = []
                    self.links.get(format_str).append(href)
                    print(href)
                break
            else:
                redirect_href = _get_redirect_file(href)
                if redirect_href and redirect_href.endswith(key):
                    format_str = str(key)
                    if format_str in self.links:
                        # there is a key about this format in the dict
                        self.links.get(format_str).append(redirect_href)
                        print(redirect_href)

                    else:
                        # there is no ke about this format in the dict
                        self.links[format_str] = []
                        self.links.get(format_str).append(redirect_href)
                        print(redirect_href)
                    break
