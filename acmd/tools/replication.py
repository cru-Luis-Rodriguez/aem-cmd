# coding: utf-8
import sys
import optparse
import requests
from lxml import html

from acmd import tool, log, error
from acmd.tools import get_command, get_argument
SERVICE_PATH = '/bin/replicate.json'

parser = optparse.OptionParser("acmd replication [options] <activate> <path>")
parser.add_option("-r", "--raw",
                  action="store_const", const=True, dest="raw",
                  help="output raw response data")


@tool('replication')
class ReplicationTool(object):
    def execute(self, server, argv):
        options, args = parser.parse_args(argv)
        cmd = get_command(args, 'help')
        path = get_argument(args)
        if cmd == 'activate':
            activate(server, options, path)
        else:
            parser.print_help()


def activate(server, options, path):
    """ curl -u admin:admin -X POST -F path="/content/path/to/page" -F cmd="activate" http://localhost:4502/bin/replicate.json
    """
    url = server.url(SERVICE_PATH)
    form_data = dict(cmd='activate', path=path)

    resp = requests.post(url, auth=server.auth, data=form_data)
    if not resp.status_code == 200:
        error("Failed to perform activation because {}: {}\n".format(resp.status_code, resp.content))
    else:
        if options.raw:
            sys.stdout.write("{}\n".format(resp.content))
        else:
            tree = html.fromstring(resp.text)
            msg = tree.xpath('//div[@id="Message"]/text()')[0]
            log("{}".format(msg))
            confirm = tree.xpath('//div[@id="Path"]/text()')[0]
            sys.stdout.write("{}\n".format(confirm))