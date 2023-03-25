#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

import requests
import lxml.html


# login URL of the wifi on ice portal
LOGIN_URL = "https://login.wifionice.de/de/"

# url to get used data volume
USAGE_URL = "https://login.wifionice.de/usage_info/"

# set user agent
HEADERS = {
    "user-agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) "
                  "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
}

# configure logger
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


class WifiOnIceManager:
    """
    simple class that allows to connect to the WiFi on ICE network
    """
    def __init__(self):
        self.s = requests.Session()

        # get current state
        self._get_state()

    @property
    def state(self):
        """
        returns the current state of the connection
        """
        return "up" if "logout" in self._status else "down"

    @property
    def usage(self):
        """
        return the used data volume, or -1 if it fails
        """
        r = self.s.get(USAGE_URL)
        if r.status_code == requests.codes.ok:
            return float(r.text)

        return -1

    def _get_state(self):
        """
        internal function to get the current connection state and
        required CSRF parameters for login
        """
        r = self.s.get(LOGIN_URL, headers=HEADERS, allow_redirects=True)
        if r.status_code != requests.codes.ok:
            sys.exit("state detection error: {}".format(r.status_code))

        # get inputs from form and store them internally
        inputs = lxml.html.fromstring(r.text).findall(".//input")
        self._status = {
            inp.name: inp.value
            for inp in inputs
            if inp.name is not None
        }
        log.debug(self._status)

    def _action(self, cmd):
        """
        internal function to connect or disconnect
        """
        assert(cmd in ("connect", "disconnect"))

        r = self.s.post(
            LOGIN_URL, data=self._status,
            headers=HEADERS, allow_redirects=True
        )
        if r.status_code != requests.codes.ok:
            sys.exit("error while {}ing: {}".format(cmd, r.status_code))

        # get new state
        self._get_state()

    def up(self):
        if self.state != "down":
            sys.exit("error: connection is already up")

        self._action("connect")

    def down(self):
        if self.state != "up":
            sys.exit("error: connection is already down")

        self._action("disconnect")


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description="WifiOnIce")
    parser.add_argument(
        "command", choices=("status", "usage", "up", "down"),
        help="command to be applied"
    )
    args = parser.parse_args()

    # get wifi on ice manager instance
    moim = WifiOnIceManager()

    if args.command == "status":
        # just show the status
        print(moim.state)

    elif args.command == "usage":
        # just show the usage
        print(moim.usage)

    elif args.command == "up":
        moim.up()

    elif args.command == "down":
        moim.down()


if __name__ == "__main__":
    main()
