import sys
import json
import requests

class LoreAPI(object):
    
    def __init__(self, scheme, host, auth_token):
        self.scheme = scheme
        self.host = host
        self.auth_token = auth_token

    def get_course_by_url_name(self, url_name):
        path = "/url_lookup/%s" % (url_name)
        url = self.get_url(path)
        return requests.get(url)

    def get_lore_user_id(self, twitter_user_id):
        return 2650366

    def post_text_to_course(self, text, course_id, author_id):
        path = "/posts"
        url = self.get_url(path)

        json_data = {
            "type": "post",
            "parent": int(course_id),
            "author": 2650254,
            "contents": [
                {
                    "text": { "content": [{ "content": text }] },
                    "id": -1000,
                    "type": "content_text_block",
                }
            ]
        }

        query_params = {
            "auth_token": self.auth_token,
            "json_data": json.dumps(json_data)
        }
        
        return requests.post(url, query_params)

    def get_url(self, path):
        return "%s://%s%s" % (self.scheme, self.host, path)

if __name__ == "__main__":
    api = LoreAPI("", "", "")
    if sys.argv[1] == "get":
        response = api.get_course_by_url_name(sys.argv[2])
        print response.status_code
        print response.text

    if sys.argv[1] == "post":
        response =  api.post_text_to_course("Ahoy from the command line.", 2650366, 2650254)
        print response.status_code
        print response.text

        

        
