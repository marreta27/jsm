# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
from BeautifulSoup import BeautifulSoup
from html5lib import HTMLParser
from html5lib import treebuilders
import logging

def html_parser(html):
    try:
        soup = BeautifulSoup(html)
    except:
        parser = HTMLParser(tree=treebuilders.getTreeBuilder("beautifulsoup"))
        soup = parser.parse(html)
    return soup

def use_debug():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(message)s")

def debuglog(val):
    logging.debug(val)
    