import sys
import click
from typing import List

import nbformat
import os
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

exporter = HTMLExporter()
ep = ExecutePreprocessor(timeout=600, kernel_name='python3', store_widget_state=True)


def open_nb(name: str, src: str) -> nbformat:
    """
    Open notebook file

    :param name: name of notebook to open
    :param src: source directory
    :return: notebook object
    """
    print('Reading...', end=' ')
    nb = nbformat.read('{src}/{name}/{name}.ipynb'.format(name=name, src=src), as_version=4)
    print('OK', end=' ')
    return nb


def execute(nb: nbformat, name: str, src: str) -> nbformat:
    """
    Execute notebook and store widget state.

    :param nb: notebook object to execute
    :param name: notebook name (for setup directory context purpose)
    :param src: notebook source directory (for setup context)
    :return: notebook object with computed and stored output widget state
    """
    print('Executing...', end=' ')
    ep.preprocess(nb, {'metadata': {'path': '%s/%s/' % (src, name)}})
    print('OK', end=' ')
    return nb


def copy_image(name: str, export: str, src: str):
    """
    Copy images present next to notebook file to exported folder.

    :param name: notebook name
    :param export: export directory
    :param src: source directory
    :return: None
    """
    src = '%s/%s' % (src, name)
    dest = '%s/%s' % (export, name)
    images = [f for f in os.listdir(src) if f.split('.')[-1] in ['png']]
    for img in images:
        os.rename('%s/%s' % (src, img), '%s/%s' % (dest, img))


def to_export(nb: nbformat, name: str, export: str):
    """
    Export notebook into HTML format.

    :param nb: notebook with result state
    :param name: notebook name
    :param export: directory to export
    :return: None
    """
    print('Exporting...', end=' ')
    html, _ = exporter.from_notebook_node(nb)

    path = '%s/%s' % (export, name)
    if not os.path.exists(path):
        os.makedirs(path)

    with open('%s/index.html' % path, 'w') as f:
        f.write(html)

    print('OK', end=' ')


def list_notebook() -> List[str]:
    """
    List available notebook in  directory.

    :return:
    """
    dirs = os.listdir('./examples')
    return [d for d in dirs if os.path.isfile('examples/{name}/{name}.ipynb'.format(name=d))]


@click.command('Check and export notebooks')
@click.option('--src', nargs=1, help='Notebook directory')
@click.option('--check', nargs=1, help='check notebook according to result file given')
@click.option('--export', nargs=1, help='export notebooks to directory given')
def main(src: str, check: str, export: str):
    for name in list_notebook():
        print(name, ':', end='')
        nb = open_nb(name, src)
        nb = execute(nb, name, src)
        if check:
            pass  # Implement check
        if export:
            to_export(nb, name, export)
            copy_image(name, export, src)
        print('')


if __name__ == '__main__':
    main()
