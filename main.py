import json
import os
from helper.api import CodeWarsApi
from helper.kata import KataParser
import collections
collections.Callable = collections.abc.Callable



with open('./setup.json') as fin:
    setup = json.load(fin)

with open('./source.html') as fin:
    file = fin.read()

base_dir = setup['download_folder']
extensions = setup['file_extensions']

def trimPath(value, deletechars = '\/:.!*?"<>|'):
    for c in deletechars:
        value = value.replace(c,'')
    return value

parser = KataParser(file)
katas = parser.parse_katas()
api = CodeWarsApi(setup['codewars']['api_key'])


print('Exporting katas...')
for i, kata in enumerate(katas):
    print('\r{}/{} katas exported.'.format(i+1, len(katas)), end='')

    kata_info = api.get_kata_name_and_description(kata.kata_id)
    kata_name = kata_info[0]
    kata_description = kata_info[1]
	
    for language, source_code in zip(kata.languages, kata.source_codes):
        file_dir = os.path.join(base_dir, kata.difficulty, trimPath(kata.title), language)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        filename = 'solution' + extensions.get(language, '')
        with open(os.path.join(file_dir, filename), 'w', encoding="utf-8") as fout:
            fout.write(source_code)

        with open(os.path.join(file_dir, 'README.md'), 'w', encoding="utf-8") as fout:
            fout.write(f"# [{kata_name}](https://www.codewars.com/kata/{kata.kata_id})\n\n")
            fout.write(kata_description)