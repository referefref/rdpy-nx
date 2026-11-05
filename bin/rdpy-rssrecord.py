#!/usr/bin/env python3
#
# Copyright (c) 2014-2015 Sylvain Peyrefitte
#
# This file is part of rdpy.
#
# rdpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
Headless recorder of a Recorded Session Scenario (rss) file for rdpy-rdphoneypot.
Connects to an RDP server, records the screen updates it sends for a few
seconds (for example its login screen) and writes them to an rss file.
It replaces the -r option of the Qt4 client rdpy-rdpclient for systems
without PyQt4.
"""

import sys, argparse

from rdpy.core import log, rss
from rdpy.protocol.rdp import rdp
from twisted.internet import reactor

log._LOG_LEVEL = log.Level.INFO

class RecorderObserver(rdp.RDPClientObserver):
    def __init__(self, controller, recorder, width, height, duration):
        rdp.RDPClientObserver.__init__(self, controller)
        self._rss = recorder
        self._width, self._height = width, height
        self._duration = duration
        self._updates = 0

    def onReady(self):
        self._rss.screen(self._width, self._height, self._controller.getColorDepth())
        reactor.callLater(self._duration, self._controller.close)

    def onSessionReady(self):
        pass

    def onClose(self):
        self._rss.close()
        log.info("recorded %d screen updates" % self._updates)
        if reactor.running:
            reactor.stop()

    def onUpdate(self, destLeft, destTop, destRight, destBottom, width, height, bitsPerPixel, isCompress, data):
        self._updates += 1
        self._rss.update(destLeft, destTop, destRight, destBottom, width, height, bitsPerPixel,
                         rss.UpdateFormat.BMP if isCompress else rss.UpdateFormat.RAW, data)

class RecorderFactory(rdp.ClientFactory):
    def __init__(self, args):
        self._args = args

    def buildObserver(self, controller, addr):
        a = self._args
        controller.setScreen(a.width, a.height)
        controller.setUsername(a.username)
        controller.setPassword(a.password)
        controller.setDomain(a.domain)
        controller.setSecurityLevel({"rdp": rdp.SecurityLevel.RDP_LEVEL_RDP,
                                     "tls": rdp.SecurityLevel.RDP_LEVEL_SSL,
                                     "nla": rdp.SecurityLevel.RDP_LEVEL_NLA}[a.sec])
        return RecorderObserver(controller, rss.createRecorder(a.output), a.width, a.height, a.duration)

    def clientConnectionLost(self, connector, reason):
        if reactor.running:
            reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        log.error("connection failed: %s" % reason)
        if reactor.running:
            reactor.stop()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description = "Record an rss scenario for rdpy-rdphoneypot without a GUI")
    p.add_argument("target", help = "host[:port] of the RDP server to record")
    p.add_argument("-o", "--output", required = True, help = "rss file to write")
    p.add_argument("-W", "--width", type = int, default = 1024)
    p.add_argument("-H", "--height", type = int, default = 768)
    p.add_argument("-u", "--username", default = "")
    p.add_argument("-p", "--password", default = "")
    p.add_argument("-d", "--domain", default = "")
    p.add_argument("-s", "--sec", choices = ["rdp", "tls", "nla"], default = "rdp")
    p.add_argument("-t", "--duration", type = float, default = 10.0, help = "seconds to record")
    args = p.parse_args()
    host, _, port = args.target.partition(":")
    reactor.connectTCP(host, int(port or 3389), RecorderFactory(args))
    reactor.run()
