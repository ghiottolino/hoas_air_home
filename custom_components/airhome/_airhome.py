#!/usr/bin/env python
# Python class to connect to an airhome system.
#
# Copyright 2022 Nicola Tesser <ghiottolino@gmail.com>
# Licensed under a MIT license. See LICENSE for details

import urllib.request
import urllib.parse
import json

REMOTE_ADDRESS = "https://www.air-home.de/api/systemdatas/{SERIALNUMBER}/info?configNames=volumeflowinput&configNames=temproom&configNames=controlvaluefaneta&configNames=controlvaluefansup&configNames=humidityoutput&configNames=sensoren&configNames=heat_emission&configNames="
REQUEST_INTERVAL_SEC = 10  # minimum interval between requests
REQUEST_INTERVAL_SEC_LOCAL = 1  # minimum interval between requests


class AuthenticationError(Exception):
    """Class for Authentication Error Exception."""

    pass

#airhome = AIRHOME(serialNumber = SERIALNUMBER, cookie= 'ASP.NET_SessionId=YYY')

class AIRHOME:
    """A class describing an AirHome system."""

    def __init__(self, **kwargs):
        """Constructor of an E3DC object.

        Args:
            **kwargs: Arbitrary keyword argument

        Keyword Args:
            cookie (str): the cookie to connect - required for CONNECT_LOCAL
            serialNumber (str): the serial number of the system to monitor
            configuration (Optional[dict]): dict containing details of the E3DC configuration. {"pvis": [{"index": 0, "strings": 2, "phases": 3}], "powermeters": [{"index": 0}], "batteries": [{"index": 0, "dcbs": 1}]}
        """
        self.cookie = kwargs["cookie"]
        self.serialNumber = kwargs["serialNumber"]

        if "configuration" in kwargs:
            configuration = kwargs["configuration"]

            self.cookie = configuration["cookie"]
            self.serialNumber = configuration["serialNumber"]

    def poll(self):
        try:
            req = urllib.request.Request(REMOTE_ADDRESS.replace('{SERIALNUMBER}', self.serialNumber))
            req.add_header('Cookie',self.cookie)
            f = urllib.request.urlopen(req)
            data = json.loads(f.read().decode('utf-8'))
            return data
        except:
            raise AuthenticationError("Error communicating with server")
        if data["ERRNO"] != 0:
            raise AuthenticationError("Error communicating with server"+data)
