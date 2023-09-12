#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

import requests
import lxml.html
import click


# login URL of the wifi on ice portal
LOGIN_URL = "https://login.wifionice.de/de/"

# url to get used data volume
USAGE_URL = "https://login.wifionice.de/usage_info/"

# set user agent
HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) "
        "AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405"
    )
}

# configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


class WifiOnIceManager:
    """
    simple class that allows to connect to the WiFi on ICE network
    """
    def __init__(self):
        self.s = requests.Session()

        # get current state
        self._get_state()

    def _get(self, url: str) -> requests.Response:
        """
        helper function for GET on URL with exception handling
        """
        try:
            r = self.s.get(
                url,
                headers=HEADERS,
                allow_redirects=True
            )
            r.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            log.debug(e)
            sys.exit(f"Could not GET '{url}'!")

        return r

    def _post(self, url: str, data: dict) -> requests.Response:
        """
        helperfunction to POST to URL with exception handling
        """
        try:
            r = self.s.post(
                url,
                headers=HEADERS,
                allow_redirects=True,
                data=data
            )
            r.raise_for_status()

        except requests.exceptions.ConnectionError as e:
            log.error(e)
            sys.exit(f"Could not POST '{data}' to '{url}'!")

        return r

    @property
    def state(self):
        """
        returns the current state of the connection
        """
        return (
            "up"
            if "logout" in self._status else
            "down"
        )

    @property
    def usage(self):
        """
        return the used data volume
        """
        r = self._get(USAGE_URL)
        usage = float(r.text)

        log.debug(f"usage: {usage}")

        return usage

    def _get_state(self):
        """
        internal function to get the current connection state and
        required CSRF parameters for login
        """
        r = self._get(LOGIN_URL)

        # get inputs from form and store them internally
        self._status = {
            inp.name: inp.value
            for inp in lxml.html.fromstring(r.text).findall(".//input")
            if inp.name is not None
        }
        log.debug(self._status)

    def up(self):
        """
        put network connection up
        """
        if self.state != "down":
            sys.exit("error: connection is already up")

        self._post(LOGIN_URL, data=self._status)
        self._get_state()

    def down(self):
        """
        put network connection down
        """
        if self.state != "up":
            sys.exit("error: connection is already down")

        self._post(LOGIN_URL, data=self._status)
        self._get_state()


@click.group()
def cli():
    """
    simple script to connect to the WiFi on ICE
    """


@cli.command()
def status():
    """
    show connection status
    """
    click.echo(WifiOnIceManager().state)


@cli.command()
def usage():
    """
    show usage
    """
    click.echo(WifiOnIceManager().usage)


@cli.command()
def up():
    """
    put network connection up
    """
    click.echo(WifiOnIceManager().up())


@cli.command()
def down():
    """
    put network connection down
    """
    click.echo(WifiOnIceManager().down())


if __name__ == "__main__":
    cli()
