from typing import List, TypedDict


class Episode(TypedDict):
    title: str
    slug: str
    summary: str
    pub_date: str
    link: str
    audio_url: str
    guid: str
    keywords: List[str]
    duration: str
