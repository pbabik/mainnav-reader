Found the problem: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/460857

| **Distro** | **Version** | **Kernel** | **Type** | **Working?** | /var/log/messages |
|:-----------|:------------|:-----------|:---------|:-------------|:------------------|
| Ubuntu     | 9.04        | 2.6.28     | livecd   | Yes          |                   |
| Ubuntu     | 9.04        | 2.6.28     | updated  | Yes          | [#Ubuntu-9.04-updated](#Ubuntu-9.04-updated.md) |
| Ubuntu     | 9.10        | 2.6.31     | livecd   | No           | [#Ubuntu-9.10-livecd-notworking](#Ubuntu-9.10-livecd-notworking.md) |
| Ubuntu     | 9.10        | 2.6.31     | updated  | Yes          | [#Ubuntu-9.10-updated-working](#Ubuntu-9.10-updated-working.md) |
| Ubuntu     | 10.4        | 2.6.32     | livecd-dev | Yes          |                   |
|            |             |            |          |              |                   |
| OpenSUSE   | 11.1        | 2.6.27     | livecd   | Yes          |                   |
| OpenSUSE   | 11.2        | 2.6.31     | livecd   | No           | [#OpenSUSE-11.2-livecd-notworking](#OpenSUSE-11.2-livecd-notworking.md) |
| OpenSUSE   | 11.2        | 2.6.31     | updated  | Yes          | [#OpenSUSE-11.2-updated-working](#OpenSUSE-11.2-updated-working.md) |
| OpenSUSE   | 11.3        | 2.6.33     | livecd-dev | Yes          |                   |
| OpenSUSE   | 11.3        | 2.6.34     | ?        | Yes          |                   |
|            |             |            |          |              |                   |
| Fedora     | 11          | 2.6.29     | livecd   | Yes          |                   |
| Fedora     | 12          | 2.6.31     | livecd   | No           |                   |
| Fedora     | 12          | 2.6.31     | updated  | No           |                   |
| Fedora     | 13          | 2.6.33     | livecd-alpha | Yes          |                   |
|            |             |            |          |              |                   |
| Mandriva   | 2010 spring | 2.6.33     | livecd-rc | Yes          |                   |

### Ubuntu-9.04-updated-working ###
```
usb 3-2.1: new full speed USB device using uhci_hcd and address 8
usb 3-2.1: configuration #1 chosen from 1 choice
cp2101 3-2.1:1.0: cp2101 converter detected
usb 3-2.1: reset full speed USB device using uhci_hcd and address 8
usb 3-2.1: cp2101 converter now attached to ttyUSB0
```

### Ubuntu-9.10-livecd-notworking ###
```
usb 2-2: new full speed USB device using uhci_hcd and address 2
usb 2-2: configuration #1 chosen from 1 choice
usbcore: registered new interface driver usbserial
USB Serial support registered for generic
usbcore: registered new interface driver usbserial_generic
usbserial: USB Serial Driver core
USB Serial support registered for cp210x
cp210x 2-2:1.0: cp210x converter detected
usb 2-2: reset full speed USB device using uhci_hcd and address 2
usb 2-2: cp210x converter now attached to ttyUSB0
usbcore: registered new interface driver cp210x
cp210x: v0.09:Silicon Labs CP210x RS232 serial adaptor driver
```

### Ubuntu-9.10-updated-working ###
```
usb 2-2: new full speed USB device using uhci_hcd and address 2
usb 2-2: configuration #1 chosen from 1 choice
usbcore: registered new interface driver usbserial
USB Serial support registered for generic
usbcore: registered new interface driver usbserial_generic
usbserial: USB Serial Driver core
USB Serial support registered for cp210x
cp210x 2-2:1.0: cp210x converter detected
usb 2-2: reset full speed USB device using uhci_hcd and address 2
usb 2-2: cp210x converter now attached to ttyUSB0
usbcore: registered new interface driver cp210x
cp210x: v0.09:Silicon Labs CP210x RS232 serial adaptor driver
```

### OpenSUSE-11.2-livecd-notworking ###
```
usb 2-2: new full speed USB device using uhci_hcd and address 2
usb 2-2: New USB device found, idVendor=10c4, idProduct=ea60
usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
usb 2-2: Product: CP2102 USB to UART Bridge Controller
usb 2-2: Manufacturer: Silicon Labs
usb 2-2: SerialNumber: 0001
usb 2-2: configuration #1 chosen from 1 choice
usbcore: registered new interface driver usbserial
USB Serial support registered for generic
usbcore: registered new interface driver usbserial_generic
usbserial: USB Serial Driver core
USB Serial support registered for cp210x
cp210x 2-2:1.0: cp210x converter detected
usb 2-2: reset full speed USB device using uhci_hcd and address 2
usb 2-2: cp210x converter now attached to ttyUSB0
usbcore: registered new interface driver cp210x
cp210x: v0.09:Silicon Labs CP210x RS232 serial adaptor driver
```

### OpenSUSE-11.2-updated-working ###
```
usb 2-2: new full speed USB device using uhci_hcd and address 2
usb 2-2: New USB device found, idVendor=10c4, idProduct=ea60
usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
usb 2-2: Product: CP2102 USB to UART Bridge Controller
usb 2-2: Manufacturer: Silicon Labs
usb 2-2: SerialNumber: 0001
usb 2-2: configuration #1 chosen from 1 choice
usbcore: registered new interface driver usbserial
USB Serial support registered for generic
usbcore: registered new interface driver usbserial_generic
usbserial: USB Serial Driver core
USB Serial support registered for cp210x
cp210x 2-2:1.0: cp210x converter detected
usb 2-2: reset full speed USB device using uhci_hcd and address 2
usb 2-2: cp210x converter now attached to ttyUSB0
usbcore: registered new interface driver cp210x
cp210x: v0.09:Silicon Labs CP210x RS232 serial adaptor driver
```