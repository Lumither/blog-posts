#!/usr/bin/env python3

import argparse

import rich

from templates.post import BlogPost


def main():
    # if args.new:
    #     new_post()
    bp = BlogPost()
    bp.init()


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--new", help="Create a post with build-in template", type=str)
args = parser.parse_args(namespace=rich)

if __name__ == '__main__':
    main()
