# RDPY-nx

Adapted from https://github.com/citronneur/rdpy by Sylvain Peyrefitte (citronneur).

This is a standalone copy of RDPY (last upstream commit cef16a9, April 2020) ported to Python 3, with the upstream history and the GNU GPL v3 licence kept. Upstream RDPY runs only on Python 2.7, which current Linux distributions no longer ship. Changes:

- Python 3 port (tested on Python 3.11 with Twisted 26, pyOpenSSL 26, rsa 4.9, pyasn1): bytes-based `Stream` and `String` types, rich comparisons, `hashlib`, integer RSA helpers, relative imports, the `rle` C extension on the Python 3 module API, a TLS client context that negotiates current TLS versions, and an MD4 fallback to pycryptodome for NLA on OpenSSL 3. The upstream unit tests are updated for bytes and pass.
- Client interoperability with xrdp (the info packet sets `INFO_MAXIMIZESHELL`, and a bitmap capability without multiple-rectangle support is accepted), so `rdpy-rdpmitm.py` can record sessions from xrdp servers.
- `rdpy-rdphoneypot.py` closes the session when a scenario file ends without a close event, instead of failing in the replay loop.
- New `bin/rdpy-rssrecord.py`: a headless recorder that writes an RDP server's screen (for example its login screen) to an rss scenario for the honeypot, replacing the `-r` option of the Qt4 client.
- `qt4reactor` is no longer a dependency. The Qt4 tools (`rdpy-rdpclient`, `rdpy-vncclient`, `rdpy-rdpscreenshot`, `rdpy-vncscreenshot`, `rdpy-rssplayer`) are converted to Python 3 syntax but need PyQt4, which does not exist for Python 3, and are untested. The honeypot, the MITM proxy, the recorder and the library work without Qt.

Install: `pip install .` (needs a C compiler and the Python headers for the `rle` extension).

The original README follows.

---

# RDPY

Remote Desktop Protocol in twisted python.

RDPY is a pure Python implementation of the Microsoft RDP (Remote Desktop Protocol) protocol (client and server side). RDPY is built over the event driven network engine Twisted. RDPY support standard RDP security layer, RDP over SSL and NLA authentication (through ntlmv2 authentication protocol).

RDPY provides the following RDP and VNC binaries :
* RDP Man In The Middle proxy which record session
* RDP Honeypot
* RDP screenshoter
* RDP client
* VNC client
* VNC screenshoter
* RSS Player

## Build

RDPY is fully implemented in python, except the bitmap decompression algorithm which is implemented in C for performance purposes.

### Dependencies

Dependencies are only needed for pyqt4 binaries :
* rdpy-rdpclient
* rdpy-rdpscreenshot
* rdpy-vncclient
* rdpy-vncscreenshot
* rdpy-rssplayer

#### Linux

Example for Debian based systems :
```
sudo apt-get install python-qt4
```

#### OS X
Example for OS X to install PyQt with homebrew
```
$ brew install qt sip pyqt
```

#### Windows

x86 | x86_64
----|-------
[PyQt4](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x32.exe) | [PyQt4](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe/download)
[PyWin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py2.7.exe/download) | [PyWin32](http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win-amd64-py2.7.exe/download)

### Build

```
$ git clone https://github.com/citronneur/rdpy.git rdpy
$ pip install twisted pyopenssl qt4reactor service_identity rsa pyasn1
$ python rdpy/setup.py install
```

Or use PIP:
```
$ pip install rdpy
```

For virtualenv, you will need to link the qt4 library to it:
```
$ ln -s /usr/lib/python2.7/dist-packages/PyQt4/ $VIRTUAL_ENV/lib/python2.7/site-packages/
$ ln -s /usr/lib/python2.7/dist-packages/sip.so $VIRTUAL_ENV/lib/python2.7/site-packages/
```

## RDPY Binaries

RDPY comes with some very useful binaries. These binaries are linux and windows compatible.

### rdpy-rdpclient

rdpy-rdpclient is a simple RDP Qt4 client.

```
$ rdpy-rdpclient.py [-u username] [-p password] [-d domain] [-r rss_ouput_file] [...] XXX.XXX.XXX.XXX[:3389]
```

You can use rdpy-rdpclient in a Recorder Session Scenario, used in rdpy-rdphoneypot.

### rdpy-vncclient

rdpy-vncclient is a simple VNC Qt4 client .

```
$ rdpy-vncclient.py [-p password] XXX.XXX.XXX.XXX[:5900]
```

### rdpy-rdpscreenshot

rdpy-rdpscreenshot saves login screen in file.

```
$ rdpy-rdpscreenshot.py [-w width] [-l height] [-o output_file_path] XXX.XXX.XXX.XXX[:3389]
```

### rdpy-vncscreenshot

rdpy-vncscreenshot saves the first screen update in file.

```
$ rdpy-vncscreenshot.py [-p password] [-o output_file_path] XXX.XXX.XXX.XXX[:5900]
```

### rdpy-rdpmitm

rdpy-rdpmitm is a RDP proxy allows you to do a Man In The Middle attack on RDP protocol.
Record Session Scenario into rss file which can be replayed by rdpy-rssplayer.

```
$ rdpy-rdpmitm.py -o output_dir [-l listen_port] [-k private_key_file_path] [-c certificate_file_path] [-r (for XP or server 2003 client)] target_host[:target_port]
```

Output directory is used to save the rss file with following format (YYYYMMDDHHMMSS_ip_index.rss)
The private key file and the certificate file are classic cryptographic files for SSL connections. The RDP protocol can negotiate its own security layer If one of both parameters are omitted, the server use standard RDP as security layer.

### rdpy-rdphoneypot

rdpy-rdphoneypot is an RDP honey Pot. Use Recorded Session Scenario to replay scenario through RDP Protocol.

```
$ rdpy-rdphoneypot.py [-l listen_port] [-k private_key_file_path] [-c certificate_file_path] rss_file_path_1 ... rss_file_path_N
```

The private key file and the certificate file are classic cryptographic files for SSL connections. The RDP protocol can negotiate its own security layer. If one of both parameters are omitted, the server use standard RDP as security layer.
You can specify more than one files to match more common screen size.

### rdpy-rssplayer

rdpy-rssplayer is use to replay Record Session Scenario (rss) files generates by either rdpy-rdpmitm or rdpy-rdpclient binaries.

```
$ rdpy-rssplayer.py rss_file_path
```

## RDPY Qt Widget

RDPY can also be used as Qt widget through rdpy.ui.qt4.QRemoteDesktop class. It can be embedded in your own Qt application. qt4reactor must be used in your app for Twisted and Qt to work together. For more details, see sources of rdpy-rdpclient.

## RDPY library

In a nutshell RDPY can be used as a protocol library with a twisted engine.

### Simple RDP Client

```python
from rdpy.protocol.rdp import rdp

class MyRDPFactory(rdp.ClientFactory):

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def buildObserver(self, controller, addr):

        class MyObserver(rdp.RDPClientObserver):

            def onReady(self):
                """
                @summary: Call when stack is ready
                """
                #send 'r' key
                self._controller.sendKeyEventUnicode(ord(unicode("r".toUtf8(), encoding="UTF-8")), True)
                #mouse move and click at pixel 200x200
                self._controller.sendPointerEvent(200, 200, 1, true)

            def onUpdate(self, destLeft, destTop, destRight, destBottom, width, height, bitsPerPixel, isCompress, data):
                """
                @summary: Notify bitmap update
                @param destLeft: xmin position
                @param destTop: ymin position
                @param destRight: xmax position because RDP can send bitmap with padding
                @param destBottom: ymax position because RDP can send bitmap with padding
                @param width: width of bitmap
                @param height: height of bitmap
                @param bitsPerPixel: number of bit per pixel
                @param isCompress: use RLE compression
                @param data: bitmap data
                """
                
            def onSessionReady(self):
		        """
		        @summary: Windows session is ready
		        """

            def onClose(self):
                """
                @summary: Call when stack is close
                """

        return MyObserver(controller)

from twisted.internet import reactor
reactor.connectTCP("XXX.XXX.XXX.XXX", 3389, MyRDPFactory())
reactor.run()
```

### Simple RDP Server
```python
from rdpy.protocol.rdp import rdp

class MyRDPFactory(rdp.ServerFactory):

    def buildObserver(self, controller, addr):

        class MyObserver(rdp.RDPServerObserver):

            def onReady(self):
                """
                @summary: Call when server is ready
                to send and receive messages
                """

            def onKeyEventScancode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in scan code format
                @param code: scan code of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventScancode
                """

            def onKeyEventUnicode(self, code, isPressed):
                """
                @summary: Event call when a keyboard event is catch in unicode format
                @param code: unicode of key
                @param isPressed: True if key is down
                @see: rdp.RDPServerObserver.onKeyEventUnicode
                """

            def onPointerEvent(self, x, y, button, isPressed):
                """
                @summary: Event call on mouse event
                @param x: x position
                @param y: y position
                @param button: 1, 2, 3, 4 or 5 button
                @param isPressed: True if mouse button is pressed
                @see: rdp.RDPServerObserver.onPointerEvent
                """

            def onClose(self):
                """
                @summary: Call when human client close connection
                @see: rdp.RDPServerObserver.onClose
                """

        return MyObserver(controller)

from twisted.internet import reactor
reactor.listenTCP(3389, MyRDPFactory())
reactor.run()
```

### Simple VNC Client
```python
from rdpy.protocol.rfb import rfb

class MyRFBFactory(rfb.ClientFactory):

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def buildObserver(self, controller, addr):
        class MyObserver(rfb.RFBClientObserver):

            def onReady(self):
                """
                @summary: Event when network stack is ready to receive or send event
                """

            def onUpdate(self, width, height, x, y, pixelFormat, encoding, data):
                """
                @summary: Implement RFBClientObserver interface
                @param width: width of new image
                @param height: height of new image
                @param x: x position of new image
                @param y: y position of new image
                @param pixelFormat: pixefFormat structure in rfb.message.PixelFormat
                @param encoding: encoding type rfb.message.Encoding
                @param data: image data in accordance with pixel format and encoding
                """

            def onCutText(self, text):
                """
                @summary: event when server send cut text event
                @param text: text received
                """

            def onBell(self):
                """
                @summary: event when server send biiip
                """

            def onClose(self):
                """
                @summary: Call when stack is close
                """

        return MyObserver(controller)

from twisted.internet import reactor
reactor.connectTCP("XXX.XXX.XXX.XXX", 3389, MyRFBFactory())
reactor.run()
```
