from app.utils import safe_image
from bs4 import BeautifulSoup as bs4
import re

def delete_blog_post_image():
    pass


def save_html_image(media_type=None, content=None):
    soup = bs4(content, "lxml")
    images = soup.find_all('img')
    print(images)
    if len(images) > 0:
        for img in soup.find_all('img'):
            image_url = img.attrs.get('src', None)
            print(image_url)
            # if image_url and image_url.startswith('http'):
            #     img.attrs = {}
            #     image_url, status = safe_image.for_url(media_type=media_type, image_url=image_url)
            #     if status:
            #         img['src'] = image_url
            #     else:
            #         img['alt'] = image_url
        return '\n'.join(str(tag).strip() for tag in soup.html.body)
    else:
        return content


def save_markdown_image(media_type=None, content=None):
    images = re.findall(r'!\[\S*\]\((https?://\S*?/[a-z0-9\\/_?=-]*\.png|\.jpg|\.jpeg|\.webp|\.gif)\)', content, re.M|re.I)
    if images and len(images) > 0:
        for image_url in images:
            new_image_url, status = safe_image.for_url(media_type=media_type, image_url=image_url)
            if status:
                content = re.sub(pattern=image_url, repl=new_image_url, string=content, flags=re.I|re.M)
    return content