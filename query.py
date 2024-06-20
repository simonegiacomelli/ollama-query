import os
from pathlib import Path


import subprocess

def query(lib):
    template = Path('template.txt').read_text()
    question = Path('temp-question.txt')
    question.write_text(template.replace('%1', lib))

    with open('temp-answer.txt', 'w') as f:
        subprocess.run(['ollama', 'run', 'llama3'], stdin=open('temp-question.txt', 'r'), stdout=f, check=True)

    return Path('temp-answer.txt').read_text().replace(' ', '')

def clean_content(content):
    c1 = content.strip()
    c2 = [l for l in c1.split('\n') if l.strip() != '']
    c3 = '\n\n'.join(c2) + '\n'
    return c3


def main():
    cache_path = Path('cache')
    cache_path.mkdir(exist_ok=True)
    libs = Path('libs.txt').read_text().split('\n')
    Path('libs-descriptions.txt').unlink(missing_ok=True)
    libs = [lib for lib in libs if lib and lib.strip() != '']
    for lib in libs:
        print(f'\nQuerying {lib}')
        cache = cache_path / f'{lib}.txt'
        if not cache.exists():
            cache.write_text(query(lib))
        content = clean_content( cache.read_text())

        with open('libs-descriptions.txt', 'a') as f:
            f.write(f'----- {lib} -----\n{content}\n')


if __name__ == '__main__':
    main()
