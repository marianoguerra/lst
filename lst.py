#!/usr/bin/env python3
'''lst is a module and program to manipulate list like files'''
import sys
import argparse

import lst_actions

ADD_TAG_HELP = "tag message with specified tag"

REMOVE_ALL_HELP = "remove all elements from list"
REMOVE_INDEX_HELP = "remove elements at index"
REMOVE_FORCE_HELP = "don't ask for confirmation"

PURGE_FORCE_HELP = "don't ask for confirmation"

FILTER_TAGS_HELP = "show elements that have *any* of the tags"
FILTER_ALL_TAGS_HELP = "show elements that have *all* of the tags"

SHOW_ALL_HELP = "show removed elements too"
SHOW_INDEX_HELP = "show the absolute index of the item"

ACTION_HANDLERS = {
    "add": lst_actions.add,
    "remove": lst_actions.remove,
    "slice": lst_actions.slice,
    "head": lst_actions.head,
    "tail": lst_actions.tail,
    "filter": lst_actions.filter,
    "purge": lst_actions.purge
}

def define_add_parser(subparsers):
    '''define the parser for the add command'''
    parser = subparsers.add_parser('add', help="add an element to a list")

    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-t', '--tags', metavar="TAG", nargs="+",
        help=ADD_TAG_HELP)

    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)
    parser.add_argument(dest='msg', metavar="MSG", nargs="+")

def define_remove_parser(subparsers):
    '''define the parser for the remove command'''
    parser = subparsers.add_parser('remove', help="remove element from list")
    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-a', '--all', action="store_true",
        default=False, help=REMOVE_ALL_HELP)
    group.add_argument('-i', '--index', metavar="INDEX", type=int,
        dest="indexes", nargs="+", help=REMOVE_INDEX_HELP)

    parser.add_argument('-f', '--force', action="store_true",
        help=REMOVE_FORCE_HELP)

def define_purge_parser(subparsers):
    '''define the parser for the purge command'''
    parser = subparsers.add_parser('purge',
        help="purge removed items from the file")
    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)

    parser.add_argument('-f', '--force', action="store_true",
        help=PURGE_FORCE_HELP)

def define_slice_parser(subparsers):
    '''define the parser for the slice command'''
    parser = subparsers.add_parser('slice', help="show a slice of the list")

    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)
    parser.add_argument('-a', '--show-all', action="store_true", dest="show_all",
        default=False, help=SHOW_ALL_HELP)
    parser.add_argument('-i', '--show-index', action="store_true", dest="show_index",
        default=False, help=SHOW_INDEX_HELP)
    parser.add_argument(dest='begin', metavar="BEGIN", nargs=1, default=0,
            type=int)
    parser.add_argument(dest='end', metavar="END", nargs=1, default=None,
            type=int)
    parser.add_argument(dest='step', metavar="STEP", nargs=1, default=1,
            type=int)

def define_head_parser(subparsers):
    '''define the parser for the head command'''
    parser = subparsers.add_parser('head',
        help="show the first N elements of the list")

    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)
    parser.add_argument('-a', '--show-all', action="store_true", dest="show_all",
        default=False, help=SHOW_ALL_HELP)
    parser.add_argument('-i', '--show-index', action="store_true", dest="show_index",
        default=False, help=SHOW_INDEX_HELP)
    parser.add_argument('-c', '--count', dest='count', metavar="COUNT",
            default=10, type=int)

def define_tail_parser(subparsers):
    '''define the parser for the tail command'''
    parser = subparsers.add_parser('tail',
        help="show the last N elements of the list")

    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)
    parser.add_argument('-a', '--show-all', action="store_true", dest="show_all",
        default=False, help=SHOW_ALL_HELP)
    parser.add_argument('-i', '--show-index', action="store_true", dest="show_index",
        default=False, help=SHOW_INDEX_HELP)
    parser.add_argument('-c', '--count', dest='count', metavar="COUNT",
            default=10, type=int)

def define_filter_parser(subparsers):
    '''define the parser for the filter command'''
    parser = subparsers.add_parser('filter',
        help="show elements that match the filter")

    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)
    parser.add_argument(dest='query', metavar="QUERY", nargs="*")

    parser.add_argument('-a', '--show-all', action="store_true", dest="show_all",
        default=False, help=SHOW_ALL_HELP)
    parser.add_argument('-i', '--show-index', action="store_true", dest="show_index",
        default=False, help=SHOW_INDEX_HELP)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-t', '--tags', metavar="TAG", nargs="+", dest="tags",
        help=FILTER_TAGS_HELP, default=None)

    group.add_argument('-T', '--all-tags', metavar="TAG", nargs="+",
        dest="all_tags", help=FILTER_ALL_TAGS_HELP, default=None)

def define_export_parser(subparsers):
    '''define the parser for the export command'''
    parser = subparsers.add_parser('export')
    parser.add_argument(dest='list_name', metavar="LIST", nargs=1, type=str)

def define_parser():
    '''create and return the parser'''
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action_name")

    define_add_parser(subparsers)
    define_remove_parser(subparsers)
    define_purge_parser(subparsers)
    define_slice_parser(subparsers)
    define_head_parser(subparsers)
    define_tail_parser(subparsers)
    define_filter_parser(subparsers)
    define_export_parser(subparsers)

    return parser, subparsers

def run(parser_builder=define_parser):
    '''run the application'''
    parser, subparsers = parser_builder()
    opts = parser.parse_args()

    if opts.action_name in ACTION_HANDLERS:
        ACTION_HANDLERS[opts.action_name](opts)
    else:
        print("error: no handler for action", opts.action_name)

if __name__ == "__main__":
    run()


