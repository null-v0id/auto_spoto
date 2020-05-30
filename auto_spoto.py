import requests
import pickle
from twilio.rest import Client

# fav artist names->
artist_list = ['','',''] #enter your favourite artists' name (as many as you want)
                         # Example: artist_list = ['G-Eazy','NF','Eminem', 'Twenty One Pilots']

# twilio->
account_sid = '<Your twilio account sid>'
auth_token = '<Your twilio account auth token>'
client = Client(account_sid, auth_token)

# file->
with open('<Path to "last_updated_list.txt">', 'rb') as fp:
    pre_list = pickle.load(fp)


# updating token->
def tokenRequest():
    client_id = "<Your spotify account 'client ID'>"
    client_secret = "<Your spotify account 'client secret' ID>"
    url = "https://accounts.spotify.com/api/token"

    data = {"grant_type": "client_credentials"}
    req = requests.post(url, auth=(client_id, client_secret), data=data)
    reqJSON = req.json()
    acc_token = reqJSON['access_token']
    return acc_token


# sending message->
def sendMessage(track_name, artist_name, track_link):
    message = client.messages.create(
        from_='whatsapp:<Twilio number>',
        body='Hey, seems like your fav artist dropped a new song!'
             f'\nName : {track_name}'
             f'\nArtist : {artist_name}'
             f'\n{track_link}',
        to='whatsapp:<Your whatsapp number>',
    )
    print(message.sid)


# checking for playlist if updated
def updatePlaylist(new_token):
    for off in (0, 20, 40, 60, 80):
        url = f'https://api.spotify.com/v1/browse/new-releases?country=US&offset={off}&limit=20'
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": f"Bearer {new_token}"
                   }
        r = requests.get(url, headers=headers)
        jsonResponse = r.json()
        total_tracks = jsonResponse['albums']['limit']

        try:
            for i in range(total_tracks):
                curr_track = jsonResponse['albums']["items"][i]['name']
                artist_name = jsonResponse['albums']['items'][i]['artists'][0]['name']
                track_link = jsonResponse['albums']['items'][i]['external_urls']['spotify']
                if curr_track not in pre_list and artist_name in artist_list:
                    pre_list.append(curr_track)
                    print('New song added')
                    print(f'Name : {curr_track}')
                    print(f'Artist : {artist_name}')
                    sendMessage(curr_track , artist_name, track_link)

        except:
            print('A song was missed due to error (maybe)')
            pass
        with open('<Path to "last_updated_list.txt">', 'wb') as fp:
            pickle.dump(pre_list, fp)


token = tokenRequest()
updatePlaylist(token)


