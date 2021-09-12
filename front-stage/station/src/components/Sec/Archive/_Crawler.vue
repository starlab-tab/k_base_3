{
    "api": "https://www.freebuf.com/fapi/frontend/post/detail",
    "base_url": "https://www.freebuf.com",
    "custom": true,
    "platform": "freebuf",
    "pure_tags": [
        "p",
        "table",
        "th"
    ],
    "rules": {
        "author": [
            "data",
            "post_author"
        ],
        "content": [
            "data",
            "post_content"
        ],
        "date": [
            "data",
            "post_date"
        ],
        "title": [
            "data",
            "post_title"
        ]
    },
    "type": "json",
    "url_reg": "https:\\/\\/www\\.(freebuf)\\.com(\\S*)(\\d{6})"
}

{
    "api": "https://api.anquanke.com/data/v1/post",
    "base_url": "https://www.anquanke.com",
    "custom": true,
    "platform": "anquanke",
    "pure_tags": [],
    "rules": {
        "author": [
            "author",
            "nickname"
        ],
        "content": [
            "content"
        ],
        "date": [
            "date"
        ],
        "title": [
            "title"
        ]
    },
    "type": "json",
    "url_reg": "https:\\/\\/www\\.(anquanke)\\.com(\\/post\\/id\\/)(\\d{6}$)"
}

{
    "api": "https://xz.aliyun.com/t/",
    "base_url": "https://xz.aliyun.com",
    "custom": false,
    "platform": "xianzhi",
    "pure_tags": [],
    "rules": {
        "author": "#Wrapper > div > div.span10 > div.row.box.content > div > div > div.clearfix.user-info.topic-list > div > span.info-left > a > span",
        "content": "#topic_content",
        "date": "#Wrapper > div > div.span10 > div.row.box.content > div > div > div.clearfix.user-info.topic-list > div > span.info-left > span:nth-child(3)",
        "title": "#Wrapper > div > div.span10 > div.row.box.content > div > div > div.clearfix.user-info.topic-list > p > span"
    },
    "type": "html",
    "url_reg": "https:\\/\\/(xz\\.aliyun)\\.com(\\/t\\/)(\\d{4}$)"
}

{
    "api": "https://mp.weixin.qq.com/s/",
    "base_url": "https://mp.weixin.qq.com",
    "custom": true,
    "id": 31,
    "platform": "weixin",
    "pure_tags": [
        "div",
        "span",
        "p",
        "ul",
        "ol",
        "li",
        "blockquote",
        "a",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "section",
        "em",
      	"pre",
      	"code"
    ],
    "rules": {
        "author": "#js_name",
        "content": "#js_content",
        "title": "#activity-name"
    },
    "type": "html",
    "url_reg": "https:\\/\\/(mp\\.weixin)\\.qq\\.com(\\/s\\/)(\\S{22})"
}