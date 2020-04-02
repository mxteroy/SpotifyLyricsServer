from flask import Flask
from flask import request
from bs4 import BeautifulSoup
from auth import base_url, headers
from flask_cors import CORS

import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_song_path():
    search_url = base_url + "/search"
    artist = request.args.get('artist')
    song = request.args.get('song')
    data = {'q': song}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist.lower():
            song_info = hit
            break

    if song_info:
        api_path = song_info["result"]["api_path"]
        return get_song_lyrics(api_path)

def get_song_lyrics(api_path):
    song_url = base_url + api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]

    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_="lyrics").decode_contents()
    return lyrics

#PZPZlf
@app.route('/google')
def get_song_lyrics_google():
    artist = request.args.get('artist')
    song = request.args.get('song')
    url = 'https://www.google.com/search?q=' + song + ' ' + artist + " lyrics"

    page = requests.get(url)
    print(page)
    html = BeautifulSoup(page.text, "html.parser")
    print(html)
    lyrics = html.find("div", class_="PZPZlf").text
    return lyrics

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)