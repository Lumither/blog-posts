from datetime import date
from typing import Dict, Optional

from templates.utils import Template, create_all_files
from utils.autocompletion import input_autocompletion, fuzzy_pinyin_matcher

POST_TEMPLATE = '''
---
title: { title }
subtitle: { subtitle }
published_date: { published_date }
last_updated: { last_update }
category: { category }
tags: { tags }
---

WIP

'''


class BlogPost(Template):
    WORK_PATH: str = "content/posts/{year}/{identifier}/"
    ITEMS: Dict[str, Optional[str]] = {"index.md": POST_TEMPLATE, "assets/": None}

    def init(self):
        year = date.today().year
        print(input_autocompletion("input > ",
                                   ["helllo", "测试", "你好", "这是一个非常有意思的故事", "test"],
                                   fuzzy_pinyin_matcher
                                   )
              )
        create_all_files(self.WORK_PATH.format(year=year, identifier="test"), self.ITEMS)
