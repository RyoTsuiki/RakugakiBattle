# throw_request.py
"""flask_project にデータを投げるプログラム.

*もしエラーが出た場合, URL を確認すること*
使用例はmain 関数を確認すること

"""
import urllib.request
import urllib.parse
import sys

URL = "http://192.168.11.16:8888/log/"


def get_request(params):
    """ GET リクエストをサーバに投げる関数.

    Args:
        params (dict): リクエストパラメータ

    Return:
        str: サーバから受け取った文字列
    """
    req = urllib.request.Request('{}?{}'.format(
        URL, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = res.read()
    return body.decode("utf-8")


def post_request(data, model):
    """ POST リクエストをサーバに投げる関数.

    Args:
        data (dict): リクエストパラメータ
        model (str): モデル名

    Reutrn:
        str: サーバから受け取った文字列
    """
    url = URL + model
    data = urllib.parse.urlencode(data).encode('utf-8')
    print(data)
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as res:
        body = res.read().decode()
    return body


if __name__ == "__main__":
    data1 = {'odai': 'banana', 'pre': 'banana','axe': 0, 'airplane': 1, 'apple': 2, 'banana': 3, 'bicycle': 4, 'car': 5, 'donut': 6, 'fish': 7, 'hat': 8, 'house': 9}
    data2 = {'odai': 'banana', 'pre': 'banana', 'basket': 0, 'aircraft carrier': 1, 'backpack': 2, 'bat': 3, 'alarm clock': 4, 'ant': 5, 'The Mona Lisa': 6, 'baseball bat': 7, 'basketball': 8, 'arm': 9, 'baseball': 10, 'anvil': 11, 'axe': 12, 'barn': 13, 'The Eiffel Tower': 14, 'airplane': 15, 'bandage': 16, 'asparagus': 17, 'animal migration': 18, 'apple': 19, 'ambulance': 20, 'angel': 21, 'banana': 22, 'The Great Wall of China': 23, 'bear': 24, 'bench': 25, 'blackberry': 26, 'bed': 27, 'book': 28, 'beach': 29, 'bee': 30, 'blueberry': 31, 'bicycle': 32, 'binoculars': 33, 'bracelet': 34, 'bird': 35, 'bridge': 36, 'beard': 37, 'broccoli': 38, 'bread': 39, 'belt': 40, 'brain': 41, 'bowtie': 42, 'bottlecap': 43, 'birthday cake': 44, 'boomerang': 45, 'broom': 46, 'bathtub': 47, 'candle': 48, 'castle': 49, 'cat': 50, 'carrot': 51, 'bucket': 52, 'chandelier': 53, 'butterfly': 54, 'cactus': 55, 'bush': 56, 'cake': 57, 'church': 58, 'camel': 59, 'calculator': 60, 'camera': 61, 'campfire': 62, 'bus': 63, 'canoe': 64, 'chair': 65, 'ceiling fan': 66, 'cannon': 67, 'cell phone': 68, 'bulldozer': 69, 'calendar': 70, 'camouflage': 71, 'circle': 72, 'cello': 73, 'clarinet': 74, 'clock': 75, 'car': 76, 'computer': 77, 'cloud': 78, 'cow': 79, 'couch': 80, 'compass': 81, 'cookie': 82, 'crab': 83, 'cooler': 84, 'crocodile': 85, 'cruise ship': 86, 'cup': 87, 'crayon': 88, 'crown': 89, 'diamond': 90, 'coffee cup': 91, 'dolphin': 92, 'dog': 93, 'diving board': 94, 'donut': 95, 'door': 96, 'dishwasher': 97, 'dresser': 98, 'dragon': 99, 'ear': 100, 'elbow': 101, 'elephant': 102, 'drums': 103, 'drill': 104, 'eraser': 105, 'duck': 106, 'eye': 107, 'eyeglasses': 108, 'feather': 109, 'dumbbell': 110, 'envelope': 111, 'firetruck': 112, 'fence': 113, 'fan': 114, 'fire hydrant': 115, 'face': 116, 'flamingo': 117, 'fish': 118, 'fireplace': 119, 'flip flops': 120, 'foot': 121, 'flashlight': 122, 'finger': 123, 'frying pan': 124, 'fork': 125, 'garden hose': 126, 'flower': 127, 'giraffe': 128, 'floor lamp': 129, 'flying saucer': 130, 'frog': 131, 'garden': 132, 'grass': 133, 'guitar': 134, 'helicopter': 135, 'hammer': 136, 'grapes': 137, 'hamburger': 138, 'house plant': 139, 'hat': 140, 'headphones': 141, 'hand': 142, 'hedgehog': 143, 'helmet': 144, 'hockey puck': 145, 'goatee': 146, 'golf club': 147, 'harp': 148, 'house': 149, 'hexagon': 150, 'hockey stick': 151, 'ladder': 152, 'hot air balloon': 153, 'hot tub': 154, 'lantern': 155, 'laptop': 156, 'knife': 157, 'hourglass': 158, 'horse': 159, 'hospital': 160, 'jacket': 161, 'lollipop': 162, 'jail': 163, 'mailbox': 164, 'hurricane': 165, 'ice cream': 166, 'map': 167, 'hot dog': 168, 'lighter': 169, 'leg': 170, 'knee': 171, 'key': 172, 'leaf': 173, 'light bulb': 174, 'lion': 175, 'mountain': 176, 'kangaroo': 177, 'lightning': 178, 'lipstick': 179, 'keyboard': 180, 'mouse': 181, 'lobster': 182, 'line': 183, 'lighthouse': 184, 'monkey': 185, 'mosquito': 186, 'onion': 187, 'microphone': 188, 'megaphone': 189, 'matches': 190, 'microwave': 191, 'moon': 192, 'mermaid': 193, 'marker': 194, 'necklace': 195, 'ocean': 196, 'nail': 197, 'mug': 198, 'mouth': 199, 'oven': 200, 'panda': 201, 'motorbike': 202, 'mushroom': 203, 'paper clip': 204, 'moustache': 205, 'paint can': 206, 'octopus': 207, 'palm tree': 208, 'octagon': 209, 'parachute': 210, 'pear': 211, 'pants': 212, 'owl': 213, 'pencil': 214, 'piano': 215, 'peanut': 216, 'nose': 217, 'peas': 218, 'penguin': 219, 'passport': 220, 'pickup truck': 221, 'purse': 222, 'picture frame': 223, 'radio': 224, 'pineapple': 225, 'paintbrush': 226, 'pizza': 227, 'pond': 228, 'rainbow': 229, 'parrot': 230, 'pillow': 231, 'rollerskates': 232, 'sandwich': 233, 'saw': 234, 'popsicle': 235, 'saxophone': 236, 'scissors': 237, 'river': 238, 'school bus': 239, 'police car': 240, 'raccoon': 241, 'power outlet': 242, 'remote control': 243, 'rain': 244, 'postcard': 245, 'pool': 246, 'shovel': 247, 'pig': 248, 'roller coaster': 249, 'skyscraper': 250, 'sleeping bag': 251, 'pliers': 252, 'rake': 253, 'smiley face': 254, 'snail': 255, 'sink': 256, 'skateboard': 257, 'skull': 258, 'sailboat': 259, 'rabbit': 260, 'potato': 261, 'sea turtle': 262, 'screwdriver': 263, 'shoe': 264, 'shorts': 265, 'rifle': 266, 'shark': 267, 'see saw': 268, 'rhinoceros': 269, 'sheep': 270, 'scorpion': 271, 'squiggle': 272, 'strawberry': 273, 'stairs': 274, 'snake': 275, 'square': 276, 'sock': 277, 'snowflake': 278, 'star': 279, 'spider': 280, 'stove': 281, 'stereo': 282, 'stethoscope': 283, 'spoon': 284, 'speedboat': 285, 'spreadsheet': 286, 'snorkel': 287, 'soccer ball': 288, 'streetlight': 289, 'steak': 290, 'string bean': 291, 'submarine': 292, 'stop sign': 293, 'stitches': 294, 'snowman': 295, 'swing set': 296, 'squirrel': 297, 'table': 298, 'teapot': 299, 'tractor': 300, 'traffic light': 301, 'tree': 302, 'trombone': 303, 'triangle': 304, 'sweater': 305, 'train': 306, 'suitcase': 307, 'sword': 308, 'sun': 309, 'toilet': 310, 't-shirt': 311, 'tiger': 312, 'television': 313, 'swan': 314, 'tennis racquet': 315, 'toothbrush': 316, 'syringe': 317, 'telephone': 318, 'toaster': 319, 'tent': 320, 'tooth': 321, 'truck': 322, 'teddy-bear': 323, 'toe': 324, 'underwear': 325, 'umbrella': 326, 'toothpaste': 327, 'tornado': 328, 'whale': 329, 'trumpet': 330, 'watermelon': 331, 'wine bottle': 332, 'violin': 333, 'wheel': 334, 'vase': 335, 'washing machine': 336, 'waterslide': 337, 'windmill': 338, 'wine glass': 339, 'van': 340, 'yoga': 341, 'zigzag': 342, 'zebra': 343, 'wristwatch': 344}
    post_request(data2, "model2")
    print("post data")
