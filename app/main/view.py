from flask import request, render_template, jsonify
from . import main
from ..functions.Resources import Resources
from ..functions.download import download_links
from tkinter import filedialog
from config import CONFIG_USER_AGENT

#  new a class resources
resources = Resources("")


@main.route('/', methods=['GET', 'POST'])
def index():
    """
        main 
    """
    return render_template('main.html')


@main.route('/submit-url', methods=['POST'])
def submit_url():
    url = request.json['url']
    resources.set_url(url)
    resources.find_downloadable_links()
    links = resources.get_links()
    # Do something with the URL
    return jsonify({'links': links})


@main.route('/download', methods=['POST', 'GET'])
def download():
    # user_agent = request.headers.get('User-Agent')
    if CONFIG_USER_AGENT == "":
        user_agent = request.headers.get('User-Agent')
    else:
        user_agent = CONFIG_USER_AGENT
    all_url = []
    download_url_index = request.json['selectedValues']
    for key in download_url_index:
        value_index = download_url_index[key]
        all_url += resources.get_download_url(key, value_index)
    directory = filedialog.askdirectory()
    if not directory:
        return jsonify({'status': {'error': 'No directory selected'}})
    try:
        result = download_links(all_url, directory, user_agent)
        if not result:
            return jsonify({'status': {'error': 'Files downloaded failed, there is something wrong when downloading '
                                                'files'}})
    except Exception as e:
        print(f"Failed to download files: {e}")
        return jsonify({'status': {'error': 'Failed to download files'}})
    return jsonify({'status': {'success': 'Files downloaded successfully'}})
