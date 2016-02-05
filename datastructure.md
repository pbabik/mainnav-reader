
```
MAINNAV MG-950d datastructure of tracklog data                         Version 3

Reverse engineered by Dennis Keitzel


Each downloaded chunk (132 byte, except status messages like OK and FINISHED):

 offset   | size     | denotation
----------+----------+----------------------------------------------------------
0x00      |   1 byte | current mode? (always 0x01 in download mode)
0x01      |   1 byte | per chunk up-counter?
0x02      |   1 byte | per chunk down-counter?
0x03-0x82 | 128 byte | payload chunk
0x83      |   1 byte | 1-byte checksum of payload chunk

Note: For further processing, you must filter out the 4 byte metadata and join
      all received payload chunks together.


The first 8192 byte of the payload contain offset informations (16 byte each),
about the stored tracklogs. It seems, that the device is capable of storing up
to 512 of them.

Each offset information (16 byte):

 offset   | size    | endian | denotation
----------+---------+--------+--------------------------------------------------
0x00-0x02 |  3 byte | little | end offset of that tracklog
0x03-0x0f | 13 byte | -      | not used?

Note: On devices newer than MG-950dm the size of the end-offsets is 4 bytes
      each. The reason for this is an increase in the amount of memory (2>4MB)


From offset 0x2000 on, the tracklog data is stored. A tracklog consist of
multiple log entries, each of them has 16 byte.

Each log entry (16 byte):

 offset        | size   | endian | type  | denotation
---------------+--------+--------+-------+--------------------------------------
0x00-0x03      | 32 bit | -      | -     | time, see beneath
0x04-0x07      | 32 bit | little | float | longitude
0x08-0x0b      | 32 bit | little | float | latitude
0x0c-0x0c+1bit |  9 bit | big    | int   | speed
0x0d+1bit-0x0e | 15 bit | big    | s-int | elevation
0x0f           |  8 bit | -      | -     | not used?


Each time entry (32 bit):

 offset (bit) | size   | endian | type  | denotation
--------------+--------+--------+-------+---------------------------------------
00-05         |  6 bit | big    | int   | year (2006 + value)
06-09         |  4 bit | big    | int   | month
10-14         |  5 bit | big    | int   | day
15-19         |  5 bit | big    | int   | hour
20-25         |  6 bit | big    | int   | minute
26-31         |  6 bit | big    | int   | second


Note: It seems, that the chunk, next to the last with '\x04$FINISH\r\n', does
      not contain any necessary informations (0xFF all the way).
```