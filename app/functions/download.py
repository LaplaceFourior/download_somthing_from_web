from tqdm import tqdm
import requests
import os
from config import CONFIG_AGENCY_URL, CONFIG_WHETHER_UPDATE_AGENCY_URL, CONFIG_USER_AGENT
import parsel
import json
import re
from tkinter import filedialog

#
current_file_path = os.path.dirname(os.path.abspath(__file__))
all_agency_url_file_path = os.path.join(current_file_path, 'all-agency-url.json')
test_user_agent = CONFIG_USER_AGENT


def download_links(urls, directory, user_agent):
    for url in urls:
        try:
            file_name = url.split('/')[-1]
            file_path = os.path.join(directory, file_name)
            r1 = requests.get(url, stream=True, verify=False)
            total_size = int(r1.headers.get('content-length', 0))
            temp_size = 0
            chunk_size = 1024
            while (temp_size < total_size):
                with open(file_path, 'ab') as f:
                    with tqdm(desc=file_name, total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as bar:
                        try:
                            headers = {
                                'Range': 'bytes=%d-' % temp_size,
                                'User-Agent': user_agent
                            }
                            bar.update(temp_size)
                            r = requests.get(url, stream=True, verify=False, headers=headers, timeout=100)
                            for chunk in r.iter_content(chunk_size=chunk_size):
                                size = f.write(chunk)
                                bar.update(size)
                                temp_size += size
                        except Exception as e:
                            print(f"Failed to download {url}: {e}")
                            continue
        except:
            print('Failed to download ', url)
            continue
    return True

def get_best_agency(url):
    best_proxies = {}
    less_time = 0
    if CONFIG_WHETHER_UPDATE_AGENCY_URL == 1:
        update_agency_url()
        with open(all_agency_url_file_path, 'r') as f:
            data = json.load(f)
    else:
        with open(all_agency_url_file_path, 'r') as f:
            data = json.load(f)
    for key in data:
        ip_num = data[key][0]
        ip_port = data[key][1]
        proxies_dict = {
            "http": "http://" + ip_num + ":" + ip_port,
            "https": "https://" + ip_num + ":" + ip_port
        }
        headers = {
            'User-Agent': test_user_agent
        }
        try:
            r = requests.get(url=url, proxies=proxies_dict, headers=headers, timeout=100)
        except:
            print(proxies_dict, "timeout")
            continue
        request_time = r.elapsed.total_seconds()
        print(request_time)
        if key == '0':
            less_time = request_time
            best_proxies = proxies_dict
        else:
            if request_time < less_time:
                less_time = request_time
                best_proxies = proxies_dict
            else:
                continue
    return best_proxies


def update_agency_url():
    all_agency_url = {}

    user_agent = CONFIG_USER_AGENT
    headers = {
        'User-Agent': user_agent
    }
    url = CONFIG_AGENCY_URL
    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    trs = selector.css(
        'body > div.layui-row.layui-col-space15 > div.layui-col-md8 > div > div.layui-form > table > tbody > tr')
    num = 0
    print("Start to get agency url from ", user_agent)
    for tr in trs:
        ip_num = tr.css('td:nth-child(1)::text').get()
        ip_port = tr.css('td:nth-child(2)::text').get()
        ip_num = re.sub(r'[^\d\.]', '', ip_num)
        ip_port = re.sub(r'[^\d\.]', '', ip_port)
        all_agency_url[str(num)] = [ip_num, ip_port]
        num = num + 1
    with open(all_agency_url_file_path, 'w') as f:
        json.dump(all_agency_url, f)
    print("Getting agency url completed")


# # update_agency_url()
# url = "https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_14.pdf"
# # a = get_best_agency(url)
# directory = filedialog.askdirectory()
# download_links([url],directory,CONFIG_USER_AGENT)
