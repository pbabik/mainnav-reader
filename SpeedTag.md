Some users requested a speed tag within the resulting gpx file. But since the speed is calculated from distance and time it's not part of the official gpx specifications.

If you want those speed tags nonetheless, 78madman wrote a patch to generate them (the format trekbuddy uses). The patch is pretty straight forward because the gps devices actually logs the speed but gets ignored by mainnav-reader.

See [Issue #3](https://code.google.com/p/mainnav-reader/issues/detail?id=#3) for discussion and patch