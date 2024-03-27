import requests
import json
from django.conf import settings

base_url = "https://dev-backend.writesonic.com"
api_key = "72b06e71-6aaa-47bd-ba86-7473f806066b"
country_code_path = 'static/data/country_codes.json'
prompt_path = 'static/data/prompt.json'
url_file_path = 'static/data/urls.txt'


def get_country_code_dict():
    with open(country_code_path, 'r') as json_file:
        code_dict = json.load(json_file)
    return code_dict

def get_questions_dict():
    with open(prompt_path, 'r') as json_file:
        questions_dict = json.load(json_file)
    return questions_dict

def get_prompt(qts: str):
    questions_dict = get_questions_dict()
    return questions_dict[qts]

def get_urls():
    with open(url_file_path, 'r') as urls_file:
        urls_list = urls_file.readlines()

    urls_list = [url.strip() for url in urls_list]

    return urls_list 

def generate_content_piece(input_prompt: str, country_code: str, specific_domains_to_capture: list):
    """
    Returns a string which is the output of the given prompt
    """
    url = f"{base_url}/v2/business/content/chatsonic/sse"
    payload = {
        "enable_memory": False,
        "enable_google_results": True,
        "input_text": input_prompt,
        "history_data": [],
        "mode": "CONTENT_CURATION",
        "content_curation_config": {
            "web_config": {
                "specific_domains_to_capture": specific_domains_to_capture,
                "country_code": country_code,
            }
        }
    }
 
    params = {
        "data": json.dumps(payload),
    }
    headers = {"X-API-KEY": api_key}
 
    response = requests.request("GET", url, headers=headers, params=params, stream=True)
    res = ""
    for line in response:
        line = line.decode()
        # print(line)
        if 'event: update' in line:
            parts = line.split('data: ')
            for x in parts:
                if x.endswith('event: update\r\n'):
                    x = x[:-len('event: update\r\n')]
                if x.endswith('\r\n\r\n'):
                    x = x[:-len('\r\n\r\n')]
                res += x
    # print("="*20)
    #print(res)
    # print("="*20)
    return res