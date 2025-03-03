import uuid
from datetime import date
from datetime import datetime as dt
from typing import Dict, Optional

from templates.utils import Template, create_all_files
from utils.autocompletion import input_autocompletion, fuzzy_pinyin_matcher
from utils.cache import get_tags_cache, get_categories_cache
from utils.lang import eprint, wprint

POST_TEMPLATE = '''
---
title: {{ title }}
subtitle: {{ subtitle }}
published_date: {{ published_date }}
last_updated: {{ last_update }}
category: {{ category }}
tags: {{ tags }}
uuid: {{ uuid }}
---

WIP

'''


def get_title():
    while True:
        i = input("title > ")
        if i.strip() == "":
            eprint("empty title")
            continue
        else:
            return i.strip()


def get_subtitle():
    return input("subtitle > ")


def get_published_date():
    while True:
        d = input("published_date (YYYY-MM-DD) > ")
        if d == "":
            wprint("using today's date")
            return dt.today().strftime("%Y-%m-%d")
        else:
            try:
                _validate = dt.strptime(d, "%Y-%m-%d")
                return d
            except ValueError:
                eprint("invalid date")
                continue


def get_tags():
    return input_autocompletion("tags > ", get_tags_cache(), fuzzy_pinyin_matcher)


def get_category():
    while True:
        i = input_autocompletion("category > ", get_categories_cache(), fuzzy_pinyin_matcher)
        if i.strip() == "":
            eprint("empty category")
            continue
        else:
            return i.strip()


class BlogPost(Template):
    WORK_PATH: str = "content/posts/{year}/{identifier}/"
    ITEMS: Dict[str, Optional[str]] = {"index.md": POST_TEMPLATE, "assets/": None}

    def init(self):
        year = date.today().year

        index_md = POST_TEMPLATE.format(
            title=get_title(),
            subtitle=get_subtitle(),
            published_date=get_published_date(),
            last_update=dt.today().strftime("%Y-%m-%d"),
            tags=get_tags(),
            category=get_category(),
            uuid=uuid.uuid4()
        )
        create_all_files(self.WORK_PATH.format(year=year, identifier="test"), self.ITEMS)
