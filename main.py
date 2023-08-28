import os
import re

PROJECT_DIR = r"E:\1 Projects\Logseq2Obsidian\\"
FOLDER = r"Logseq"
FOLDER_JOURNALS = r"Logseq\journals"
FOLDER_PAGES = r"Logseq\pages"
# FOLDER = r"test"
# FOLDER_JOURNALS = r"test"
# FOLDER_PAGES = r"test"

aliases = {}


def add_alias(text, base_name):
    a = r'(^alias(es)?|\nalias(es)?):: (\w+)'
    match = re.search(a, text)
    if match:
        als = match.group(4).split(', ')
        # print(aliases)
        for al in als:
            aliases[r'[[{}]]'.format(al)] = r'[[{}|{}]]'.format(base_name, al)


# 必须在front_matter之前运行
def change_alias():
    for path, subdir, files in os.walk(FOLDER_PAGES):
        for file in files:
            os.chdir(PROJECT_DIR + path)
            with open(file, encoding='utf8') as f:
                text = f.read()
                for s, d in aliases.items():
                    text = text.replace(s, d)

            with open(file, encoding='utf8', mode='w+') as f:
                f.write(text)

        os.chdir(PROJECT_DIR)


# 必须在front_matter之前运行
def remove_property(text):
    prop = r'( |\t)+\w+:: .+\n'
    collapse = r'.*collapsed:: true.*'
    text = re.sub(prop, '', text)
    text = re.sub(collapse, "", text)
    return text


def front_matter(text):
    front = r'^\w+:: .+'
    front_repl = r'---\n\g<0>'
    back1 = r'(?<!( |\t))\w+:: .+(?=\n\n)'
    back2 = r'(?<!( |\t))\w+:: .+\n*$'
    back_repl = r'\g<0>\n---'
    prop = r'(?<!( |\t))(\w+):: (.+)'
    prop_repl = r'\2: \3'

    text = re.sub(r'alias::', r'aliases::', text)
    text = re.sub(r'tag::', r'tags::', text)
    text = re.sub(front, front_repl, text)
    text = re.sub(back1, back_repl, text)
    text = re.sub(back2, back_repl, text)
    text = re.sub(prop, prop_repl, text)

    return text


def code(text):
    c = r'- ```'
    c_repl = r'  ```'
    text = re.sub(c, c_repl, text)
    return text


def todo(text):
    done = r'- DONE '
    done_repl = r'- [x] '
    td = r'- (TODO|LATER|DOING|NOW) '
    td_repl = r'- [ ] '

    text = re.sub(done, done_repl, text)
    text = re.sub(td, td_repl, text)
    return text


def trans():
    for path, subdir, files in os.walk(FOLDER):
        for file in files:
            print(file)
            if not file.endswith('.md'):
                continue
            os.chdir(PROJECT_DIR + path)
            base_name = os.path.splitext(file)[0]
            with open(file, encoding='utf8') as f:
                text = f.read()
                add_alias(text, base_name)
                text = remove_property(text)
                text = front_matter(text)
                text = code(text)
                text = todo(text)

            with open(file, encoding='utf8', mode='w+') as f:
                f.write(text)

        os.chdir(PROJECT_DIR)


if __name__ == "__main__":
    trans()
    change_alias()
