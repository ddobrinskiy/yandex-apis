# In[1]:


import json
import math
import sys, os
import datetime

import requests
import pandas as pd


# In[2]:



def read_credentials_deprecated():
    with open('credentials.json') as f:
        return json.load(f)


# In[3]:


def read_credentials():
    creds = dict()
    creds['CLID'] = os.environ['YA_CLID']
    creds['APIKEY'] = os.environ['YA_APIKEY']
    return creds
    

def fetch_api_request():

    coords = {"work":{"lat": 55.747114, "lon": 37.535729},
              "home":{"lat": 55.803878, "lon": 37.591452},
              "grig":{"lat": 55.509929, "lon": 37.905518},
    }

    coord_template = "{lon},{lat}"

    from_ = coord_template.format(**coords["work"])
    to_   = coord_template.format(**coords["grig"])
    rll = f"{from_}~{to_}"

    # доп требования
    # req_str = "nosmoking,conditioner"

    api_creds = read_credentials()

    response = requests.get(
        'https://taxi-routeinfo.taxi.yandex.net/taxi_info',
        params={
            "clid":api_creds["CLID"],
            "apikey":api_creds["APIKEY"],
            "rll":rll,
            "class":"econom,business,comfortplus,vip",
            "lang":"ru",

        },

        headers={'Accept': 'application/json'},
    )

    # View the new `text-matches` array which provides information
    # about your search term within the results
    return response


# In[4]:


def generate_option_message(o):
    waiting_time_min = math.ceil(o['waiting_time']/60)
    msg_template = "  {}: ожидание {} мин, цена {}"

    return  msg_template.format(o['class_text'].rjust(8, ' '), 
                        waiting_time_min,
                        o['price_text']
                       )


# In[5]:


def print_current_options(options):
    print(f"Поездка с Работы до Григ займёт {json_response['time_text']}")
    for o in options:
        try:
            print(generate_option_message(o))
        except:
            pass


# In[6]:


def save_current_options(options):
    global df
    
    df = pd.DataFrame(options)
    df['ts'] = datetime.datetime.now()
    df['time_to_home_sec'] = json_response['time']
    
    path = os.path.dirname(os.path.abspath('__file__'))

    filepath = path + '/prices_history.csv'
    if os.path.exists(filepath):
        df.to_csv(filepath, index=False, header=False, mode='a')
    else:
        df.to_csv(filepath, index=False, header=True, mode='w')


# In[7]:


if __name__=='__main__':
    json_response = fetch_api_request().json()
    options = sorted(json_response['options'], key=lambda x: x['class_level'])
    
    save_current_options(options)
    print_current_options(options)


# In[ ]:




