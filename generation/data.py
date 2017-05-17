#!/usr/bin/env python3

import requests
import time
import json
from pprint import pprint
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.image import Image

icons = {
        'drizzle': 'drizzle.png',
        'rain': 'rain.png',
        'storm': 'storm.png',
        'clear': 'clear.png',
        'error': 'error.png'
}


def do_request(payload):
    endpoint = "http://api.openweathermap.org/data/2.5/forecast/daily"
    r = requests.get(endpoint, params=payload)
    result = r.text
    return json.loads(result)


def mock_request():
    return {"city":{"id":3433955,"name":"Ciudad Autónoma de Buenos Aires","coord":{"lon":-58.4501,"lat":-34.6},"country":"AR","population":0},"cod":"200","message":0.0697004,"cnt":2,"list":[{"dt":1494774000,"temp":{"day":16,"min":13.02,"max":16,"night":13.02,"eve":16,"morn":16},"pressure":1026.64,"humidity":90,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10n"}],"speed":1.66,"deg":61,"clouds":44}]}


def parse_data(data):
    city = data['city']['name']
    lst = data['list']

    day = lst[0]
    info = {}
    d = time.localtime(day['dt'])
    info['city'] = city
    info['dt'] = time.strftime('%d/%m/%Y', d)
    info['temp'] = day['temp']
    info['desc'] = day['weather'][0]['description']
    return info


def desc_to_icon(desc):
    for key in icons:
        if key in desc.lower():
            return icons[key]
    return icons['error']


def render_image(data):
    with Drawing() as draw:
        with Image(width=758, height=1024, background=Color('#fff')) as img:
            img.type = 'grayscale'
            img.format = 'png'

            try:
                img.alpha_channel = 'remove'
            except TypeError:
                img.alpha_channel = False

            img.depth = 8
            draw.font_size = 40
            draw.text_alignment = 'center'
            draw.font = "./DejaVuSans.ttf"
            # city, desc, dt
            # temp: morn, eve, night - max, min, day
            y = 100
            draw.text(img.width // 2, y, data['dt'])

            # Img
            y += 30
            filename = './icons/%s' % desc_to_icon(data['desc'])
            with Image(filename=filename) as icon:
                icon.resize(200, 200)
                img.composite(icon, left=img.width//2-icon.width//2, top=y)
            y += 250
            draw.text(img.width // 2, y, data['desc'].title())

            y += 70
            draw.font_size = 25
            draw.text(img.width // 6 * 1, y, 'Morning')
            draw.text(img.width // 6 * 3, y, 'Eve')
            draw.text(img.width // 6 * 5, y, 'Night')

            y += 30
            draw.text(img.width // 6 * 1, y, str(int(data['temp']['morn'])))
            draw.text(img.width // 6 * 3, y, str(int(data['temp']['eve'])))
            draw.text(img.width // 6 * 5, y, str(int(data['temp']['night'])))

            draw.text(img.width // 2, img.height - 20, data['city'])

            draw(img)
            # display(img)
            img.type = 'grayscale'
            img.save(filename='tmp.png')


def main():
    # data = mock_request()
    payload = json.loads(open('config.json').read())
    data = do_request(payload)
    d = parse_data(data)
    render_image(d)


if __name__ == '__main__':
    main()
