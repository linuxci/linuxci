#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2024 IBM
# Author : Tejas Manhas <Tejas.Manhas@ibm.com>
# Co-Author : Abdul Haleem <abdhalee@linux.vnet.ibm.com>
#Functionality to store last good commit history for bisection

import json
import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lib import common_lib as cb


def fetch(sid):
    '''
    The function will fetch value of any given key parameter 
    of given SID json file and update if key is not present
    returns: commitid and commit date
    '''
    json_path = "%s%s/%s.json" % (cb.base_path, sid, sid)
    Ojson = cb.read_json(json_path)
    if Ojson['goodCommit']:
        return Ojson['goodCommit']


def push(sid, goodcommit):
    '''
    The function will update SID jsons any given key parameter
    with its value
    goodcommit : sha-id
    commitdate : YYYY-MM-DD
    '''
    Njson = {}
    gc_att = str('goodCommit')
    json_path = "%s%s/%s.json" % (cb.base_path, sid, sid)
    Ojson = cb.read_json(json_path)
    if gc_att in Ojson:
        Ojson[gc_att] = goodcommit
        cb.append_diff_json(json_path, Ojson)
    else:
        Njson[gc_att] = goodcommit
        cb.append_diff_json(json_path, Njson)
    return "UPDATED"


def process(*args):
    arg1=args[0]
    sys.path.append(os.path.join(arg1))
    num = len(args)
    if num == 1:
        arg2=args[0]
        res = fetch(arg1)

    elif num ==2:
        arg1=args[0]
        arg2=args[1]
        res =push(arg1,arg2)
    else :
        raise ValueError("Arguments are not valid for good-commit")
    return res


if __name__ == "__main__":
    argsi = sys.argv[1:]
    result = process(*argsi)
    serialized_result = json.dumps(result)
    print(serialized_result)
