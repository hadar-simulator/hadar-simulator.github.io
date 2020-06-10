import sys
from typing import List

import nbformat
import os
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

exporter = HTMLExporter()
ep = ExecutePreprocessor(timeout=600, kernel_name='python3', store_widget_state=True)


def read(name: str) -> nbformat:
    print('Reading...', end=' ')
    nb = nbformat.read('examples/{name}/{name}.ipynb'.format(name=name), as_version=4)
    print('OK', end=' ')
    return nb


def execute(nb: nbformat, name: str) -> nbformat:
    print('Executing...', end=' ')
    ep.preprocess(nb, {'metadata': {'path': 'examples/%s/' % name}})
    print('OK', end=' ')
    return nb


def export(nb: nbformat, name: str):
    print('Exporting...', end=' ')
    html, _ = exporter.from_notebook_node(nb)

    path = '../assets/notebook/%s' % name
    if not os.path.exists(path):
        os.makedirs(path)

    with open('%s/index.html' % path, 'w') as f:
        f.write(html)
    print('OK', end=' ')


def copy_image(name: str):
    src = 'examples/%s' % name
    dest = '../assets/notebook/%s' % name
    images = [f for f in os.listdir(src) if f.split('.')[-1] in ['png']]
    for img in images:
        os.rename('%s/%s' % (src, img), '%s/%s' % (dest, img))


def list_notebook() -> List[str]:
    dirs = os.listdir('./examples')
    return [d for d in dirs if os.path.isfile('examples/{name}/{name}.ipynb'.format(name=d))]


if __name__ == '__main__':
    for name in list_notebook():
        print(name, ':', end='')
        nb = read(name)
        nb = execute(nb, name)
        export(nb, name)
        copy_image(name)
        print('')
