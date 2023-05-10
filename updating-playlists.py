import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def update_playlists_privacy(youtube, channel_id, next_page_token=None, counter=0):
    request = youtube.playlists().list(
        part="id,snippet,status",
        maxResults=500,
        mine=True,
        pageToken=next_page_token
    )
    response = request.execute()
    playlists = response.get("items", [])
    for playlist in playlists:
        counter += 1
        playlist["status"]["privacyStatus"] = "private"
        update_request = youtube.playlists().update(
            part="id,snippet,status",
            body=playlist
        )
        update_response = update_request.execute()
        print(f'\n\nPlaylist {counter}. {playlist["snippet"]["title"]}: \n\n')
        print(update_response)

    next_page_token = response.get("nextPageToken", None)
    if next_page_token:
        update_playlists_privacy(youtube, channel_id, next_page_token, counter)


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    channel_id = ""

    update_playlists_privacy(youtube, channel_id)


if __name__ == "__main__":
    main()
