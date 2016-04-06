#!/usr/bin/env python

import json
import requests

from optparse import OptionParser

def get_lipsum(howmany, what, start_with_lipsum):

    query_str  = "amount=" + str(howmany)
    query_str += "&what=" + what
    query_str += "&start=" + start_with_lipsum

    r = requests.get('http://www.lipsum.com/feed/json', query_str)

    json_obj = json.loads(r.text)

    return json_obj

get_lipsum.__doc__ = """Get lorem ipsum text from lipsum.com. Parameters:
howmany: how many items to get
what: the type of the items [paras/words/bytes/lists]
start_with_lipsum: whether or not you want the returned text to start with Lorem ipsum [yes/no]
Returns a json object containing the contents of the http request output."""

if __name__ == "__main__":
    from optparse import OptionParser
    optionParser = OptionParser()
    optionParser.add_option(
        "-n","--howmany",
        type="int",
        dest="howmany",
        metavar="X",
        help="how many items to get"
    )
    whatChoices = ('paras','words','bytes','lists')
    optionParser.add_option(
        "-w","--what",
        choices=whatChoices,
        dest="what",
        metavar="TYPE",
        help="the type of items to get: " + ', '.join(whatChoices)
    )
    optionParser.add_option(
        "-l","--start-with-Lorem",
        action="store_true",
        dest="lipsum",
        help='Start the text with "Lorem ipsum"'
    )
    optionParser.set_defaults(
        lipsum=False,
        howmany=5,
        what="paras"
    )
    (opts,args) = optionParser.parse_args()

    if 3 == len(args): # for backward compatibility with arg-only version
        opts.howmany = args[0]
        opts.what = args[1]
        opts.lipsum = 'yes' == args[2]

    lipsum = get_lipsum(
        opts.howmany, opts.what,
        'yes' if opts.lipsum else 'no'
    )

    text = lipsum['feed']['lipsum']
    text = text.replace('\n', '\n\n')

    print text

