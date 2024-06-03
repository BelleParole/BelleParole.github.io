import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

INSTAGRAM_USERNAME = 'belleparoleaps'
INSTAGRAM_URL = f'https://www.instagram.com/{INSTAGRAM_USERNAME}/'

def fetch_instagram_posts():
    response = requests.get(INSTAGRAM_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script', type='text/javascript')
    shared_data = None
    for script in scripts:
        if 'window._sharedData =' in script.string:
            shared_data = script.string.split('window._sharedData = ')[1].strip(' ;')
            break

    if not shared_data:
        return []

    import json
    data = json.loads(shared_data)
    user = data['entry_data']['ProfilePage'][0]['graphql']['user']
    posts = user['edge_owner_to_timeline_media']['edges']
    result = []
    for post in posts:
        node = post['node']
        result.append({
            'id': node['id'],
            'image_url': node['display_url'],
            'caption': node['edge_media_to_caption']['edges'][0]['node']['text'] if node['edge_media_to_caption']['edges'] else '',
            'timestamp': node['taken_at_timestamp']
        })
    return result

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = fetch_instagram_posts()
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True)
