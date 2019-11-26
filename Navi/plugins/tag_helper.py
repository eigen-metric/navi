from .api_wrapper import request_data
from .database import new_db_connection

def update_tag(c,v,list):
    print("Your tag is being updated")
    tag_data = request_data('GET', '/tags/values')
    try:
        for tag in tag_data['values']:
            if tag['category_name'] == str(c):
                if tag['value'] == str(v):
                    try:
                        tag_uuid = tag['uuid']
                        payload = {"action":"add", "assets":list, "tags":[tag_uuid]}
                        data = request_data('POST', '/tags/assets/assignments', payload=payload)
                        print("Job UUID : ", data['job_uuid'])
                        print("\nTag should be update within a few minutes\n")
                    except:
                        pass

    except:
        pass

def tag_Checker(uuid, key, value):
    database = r"navi.db"
    conn = new_db_connection(database)
    with conn:
        cur = conn.cursor()
        #This needs to be changed to UUID when the api gets fixed
        cur.execute("SELECT * from tags where asset_ip='" + uuid + "' and tag_key='" + key + "' and tag_value='" + value + "';")

        rows = cur.fetchall()

        length = len(rows)
        if length != 0:
            answer ='yes'
            return 'yes'
        else:
            return 'no'


def tag_msg():
    print("Remember to run the update command if you want to use your new tag in Navi")
