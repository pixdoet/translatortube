"""
    watch.py - Requests watch info from innertube
"""

import requests

import consts
import json


def request_watch(video_id: str, ios: bool, raw: bool):
    if ios:
        cName = "IOS"
    else:
        cName = "ANDROID"
    req_arr = {
        "context": {
            "client": {
                "hl": "en",
                "clientName": cName,
                "clientVersion": consts.INNERTUBE_REQUEST_CLIENT_VERSION,
                "androidSdkVersion": consts.INNERTUBE_REQUEST_ANDROID_SDK_VERSION,
                "mainAppWebInfo": {"graftUrl": f"/watch?v={video_id}"},
            }
        },
        "videoId": video_id,
    }

    r = requests.post(
        url=f"https://www.youtube.com/youtubei/v1/player?key={consts.INNERTUBE_REQUEST_API_KEY}",
        headers={
            "Content-Type": "application/json",
            "X-Goog-AuthUser": "0",
            "X-Origin": "https://www.youtube.com",
            f"User-agent": consts.ANDROIDTUBE_REQUEST_USER_AGENT,
        },
        json=req_arr,
    )

    response_object = r.json()
    # start pretty-printing data
    response_arr = {
        "details": {
            "title": response_object["videoDetails"]["title"],
            "tags": "",
            "description": response_object["videoDetails"]["shortDescription"],
            "thumbnails": response_object["videoDetails"]["thumbnail"]["thumbnails"],
            "views": response_object["videoDetails"]["viewCount"],
            "ownerDetails": {
                "ownerChannelName": response_object["videoDetails"]["author"],
                "ownerChannelId": response_object["videoDetails"]["channelId"],
            },
        },
        "sources": {
            "canPlay": False,
        },
    }
    # check tags
    if "keywords" in response_object["videoDetails"]:
        response_arr["details"]["tags"] = response_object["videoDetails"]["keywords"]

    # check playbility then add videosrc
    if response_object["playabilityStatus"]["status"] == "OK":
        response_arr["sources"]["canPlay"] = True
        # start adding video src
        for idx, videoSources in enumerate(response_object["streamingData"]["formats"]):
            response_arr["sources"].update(
                {
                    videoSources["qualityLabel"]: {
                        "url": videoSources["url"],
                        "width": videoSources["width"],
                        "height": videoSources["height"],
                    }
                }
            )

    if raw:
        return response_object
    else:
        return response_arr


# x = request_watch(video_id="sJsu7Tv-fRY", ios=False)
# print(x.status_code)
# print(json.dumps(x.json()))
