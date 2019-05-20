import requests
import re
import sys
base_url = "https://hub.docker.com/v2/repositories/{image}/tags/"


def get_all_tags(image, tag_prefix=".*"):
    print(f"search name: {image}, re: {tag_prefix}")
    url = base_url.format(image=image) + "?page_size=50"
    tags = []
    while True:
        res = requests.get(url)
        content_type = res.headers.get('Content-Type', '')

        if res.status_code != 200 or not content_type.startswith("application/json"):
            raise RuntimeError("错误响应:{}, content type: {}".format(res.status_code, content_type))
        data = res.json()
        url = data.get('next')
        if not url:
            break
        results = data['results']
        for tag_info in results:
            name = tag_info['name']
            last_updated = tag_info['last_updated']
            if re.match(tag_prefix, name):
                tags.append([name, last_updated])
    tags.sort(key=lambda item: item[1], reverse=True)
    for tag in tags:
        print(tag)
    return tags


if __name__ == '__main__':
    # get_all_tags("nvidia/cuda", "9.2.*")
    if not 2 <= len(sys.argv) <= 3:
        raise RuntimeError("参数个数不对")

    get_all_tags(*sys.argv[1:])
