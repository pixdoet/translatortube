#!/usr/bin/env python3
"""
    translatortube - API translator to translate hard-to-request InnerTube data into easily readable JSON format
    (C) 2023 pixdoet
"""


from typing import Union
from fastapi import FastAPI

import watch

app = FastAPI()


# default to homepage
@app.get("/")
def read_root():
    return {"Hello": "WORD"}


@app.get("/watch/{video_id}")
def get_video(
    video_id: str, ios: Union[bool, None] = None, raw: Union[bool, None] = None
):
    watch_response = watch.request_watch(video_id=video_id, ios=ios, raw=raw)
    return watch_response
