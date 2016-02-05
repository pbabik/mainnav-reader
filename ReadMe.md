# Requirements #

  * python 2.5 or 2.6
  * pySerial (python-serial on some distros)

# Installation #

Download the latest version, extract the archive and run as root:

  * `python setup.py install`

Informations about installing on MacOSX can be found on the [mailinglist](http://groups.google.com/group/mainnav-reader/browse_thread/thread/965e4971bac96176).

# Usage #

To test the connection, type in:

  * `mainnav-reader --verbose /dev/ttyUSB0`

Or, if the GPS device is connected via Bluetooth (Note: Be sure you have a connection to the serial-port prepared):

  * `mainnav-reader --verbose /dev/rfcomm0`

The simplest way to download the tracklogs is:

  * `mainnav-reader --download /dev/ttyUSB0`

Or for short:

  * `mainnav-reader -d /dev/ttyUSB0`

For more options take a look at the help page via:

  * `mainnav-reader --help`