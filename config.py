import json
import os

current_file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_file_path, 'config.json')
with open(config_path) as f:
    config = json.load(f)

CONFIG_AGENCY_URL = config['agency_url'] if (config['agency_url'] != '') else None
CONFIG_USER_AGENT = config['user_agent'] if (config['user_agent'] != '') else None
CONFIG_MOST_WAITING_TIME = config['most_waiting_time']
CONFIG_WHETHER_USE_AGENCY = config['whether_use_agency']
CONFIG_WHETHER_UPDATE_AGENCY_URL = config['whether_update_agency_url']
