'''module that provides actions to manipulate lists'''

import os
import json
import shutil
import collections

from datetime import datetime

from lst_model import List, ListItem

DEFAULT_LST_CONF_DIR = os.path.expanduser("~/.config/lst")
CONFIG_DIR = os.environ.get("LST_PATH", DEFAULT_LST_CONF_DIR)
LST_CONF_PATH = os.path.join(CONFIG_DIR, "config.json")

os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG = None

def get_path_from_list_name(list_name):
    '''return the path for the given list name'''
    # TODO: more error handling
    global CONFIG

    if CONFIG is None:
        try:
            with open(LST_CONF_PATH) as handle:
                CONFIG = json.load(handle)
        except IOError:
            CONFIG = {}

    list_config = CONFIG.get("lists", {}).get(list_name, {})
    list_path = list_config.get("path", None)

    if list_path is None:
        return os.path.join(os.path.expanduser("~"), ".lst", list_name)
    else:
        expanded_list_path = os.path.expanduser(list_path)
        return datetime.now().strftime(expanded_list_path)

def get_list_from_list_name(list_name, for_writing=False):
    '''return a list instance for the given list name'''
    path = get_path_from_list_name(list_name)
    return List.from_path(list_name, path, for_writing)

def add(opts):
    '''add an element to a list'''
    line = ListItem(" ".join(opts.msg), opts.tags)
    list_name = opts.list_name[0]

    lst = get_list_from_list_name(list_name, True)

    lst.add_line(line)

    print(line.to_string())

def remove(opts):
    '''remove an element from a list'''
    count = 0
    list_name = opts.list_name[0]
    lst = get_list_from_list_name(list_name)
    lst_path = get_path_from_list_name(list_name)

    tmp_lst_path = lst_path + ".tmp"

    tmp_lst = List(list_name + ".tmp", open(tmp_lst_path, "w"))

    indexes = set(opts.indexes)

    for item in lst:
        if count in indexes:
            item.active = False

        tmp_lst.add_line(item)

        count += 1

    tmp_lst.handle.close()
    shutil.move(tmp_lst_path, lst_path)

def purge(opts):
    '''remove an element from a list'''
    answer = None if not opts.force else "yes"

    while answer not in ("yes", "no"):
        answer = input("are you sure you want to purge the list? [yes/no] ")

    if answer == "yes":
        list_name = opts.list_name[0]
        lst = get_list_from_list_name(list_name)
        lst_path = get_path_from_list_name(list_name)

        tmp_lst_path = lst_path + ".tmp"

        tmp_lst = List(list_name + ".tmp", open(tmp_lst_path, "w"))

        for item in lst:
            if item.active:
                tmp_lst.add_line(item)

        tmp_lst.handle.close()
        shutil.move(tmp_lst_path, lst_path)
    else:
        pass

def slice(opts):
    '''show a slice of elements from a list'''
    list_name = opts.list_name[0]

    lst = get_list_from_list_name(list_name)
    start, stop, step = opts.begin[0], opts.end[0], opts.step[0]

    for index, item in lst[start:stop:step]:
        if item.active or opts.show_all:
            index_str = str(index) + " " if opts.show_index else ""
            print(item.to_string(index_str))

def head(opts):
    '''show top N elements from a list'''
    count = 0
    index = 0
    list_name = opts.list_name[0]

    lst = get_list_from_list_name(list_name)

    for item in lst:
        if count >= opts.count:
            break

        if item.active or opts.show_all:
            index_str = str(index) + " " if opts.show_index else ""
            print(item.to_string(index_str))
            count += 1

        index += 1

def tail(opts):
    '''show bottom N elements from a list'''
    items = collections.deque(maxlen=opts.count)
    list_name = opts.list_name[0]
    index = 0

    lst = get_list_from_list_name(list_name)

    for item in lst:
        if item.active or opts.show_all:
            items.append((index, item))

        index += 1

    for index, item in items:
        index_str = str(index) + " " if opts.show_index else ""
        print(item.to_string(index_str))

def filter(opts):
    '''show matched elements from a list'''
    index = 0
    list_name = opts.list_name[0]

    lst = get_list_from_list_name(list_name)

    if opts.tags is not None:
        tags = set(opts.tags)
        any_match = True
    elif opts.all_tags is not None:
        tags = set(opts.all_tags)
        any_match = False
    else:
        tags = set()
        any_match = False

    def print_item(index, item):
        '''print a single item'''
        index_str = str(index) + " " if opts.show_index else ""
        print(item.to_string(index_str))

    no_filter = len(opts.query) == 0 and len(tags) == 0

    for item in lst:
        if item.active or opts.show_all:
            if no_filter:
                print_item(index, item)
                continue

            for query in opts.query:
                if query.lower() in item.msg.lower():
                    print_item(index, item)
                    continue

            common_tags_count = len(tags.intersection(item.tags))
            if ((common_tags_count == len(tags) and common_tags_count > 0) or 
                    (any_match and common_tags_count > 0)):

                print_item(index, item)
                continue


        index += 1
