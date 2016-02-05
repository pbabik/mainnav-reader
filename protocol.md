
```
MAINNAV MG-950d serial port communication protocol                     Version 2

Based on 'Mainnav MD-950d serial port log':
http://opcenter.de/pub/misc/mainnav-log.html

Additions by Dennis Keitzel


Serial port parameters: 115200/8-N-1


Task: Request device status and log size.
Send: '$3\r\n'
Receive:'$OK!\r\n\x00\x00\x20\x60'
Further explanation: last 4 bytes is the size of all tracklogs (big endian).


Task: Delete all tracklogs from the device.
Send: '$2\r\n'
Receive:'$OK!\r\n'
When the deletion process is completed, the device sends out '$FINISH\r\n'.


Task: Download all tracklogs
Send: '$1\r\n' (switch to download mode)
Receive: '$OK!\r\n'
Send: '\x15' (request the first chunk)
Receive: ... (the first chunk)
Send: '\x06' (request the next chunk)
Receive: ... (the second chunk)
Send: '\x06' (request the next chunk)
Receive: ... (the third chunk)
[...]
Send: '\x06' (request the next)
Receive: '\x04$FINISH\r\n' (there are no more chunks, \x04 means EOT)

Note: Sending '\x06' increases/decreases the per chunk up/down-counter.
      Sending '\x15' do NOT increases/decreases the per chunk up/down-counter.
      But it does not affect the actual data being sent by the device, it's
      always the next chunk, so I don't know for what this is for.
      You must start downloading with '\x15'.
      
      Update: On devices newer than MG-950dm the two commands actually behaves
      as expected. Sending '\x15' retrieves the same chunk and '\x06' the next
      one. Therefore, crc checking is possible, because we have the ability to
      re-download a chunk.


Task: Abort a running transmission
Send: '$1\r\n' (switch to download mode)
Receive: '$OK!\r\n'
Send: '\x15' (request a chunk)
Receive: ... (the first chunk)
Send '\x18' (abort it)
Receive: '\x06\x06\x06\x06' (device is now back in standard mode)
```