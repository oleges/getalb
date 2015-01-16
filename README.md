# getalb 0.2.2

Script for downloading entire albums at once from http://musicmp3spb.org,
as opposite to song-by-song manual downloading.
Downloaded files are stored in 'getalb/music/' directory.
Script works with Python 2.7.
Script uses BeautifulSoup library for parsing html pages.

## Version history

0.1.0 - Initial release.
0.2.0 - Almost all code have been refactored according to PEP 8.
0.2.1 - Fixed crash with no URL passed as input.
0.2.2 - Albums are saved to getalb/music/ dir irrespective from cwd.

## Known issues

* Crashes on album names with forbidden symbols.

## License

Copyright (c) 2015 Oleg Esenkov. See the LICENSE file for license rights and
limitations (MIT).
