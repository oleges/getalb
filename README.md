# getalb 0.2.4

Script for downloading entire albums at once from http://musicmp3spb.org,
as opposite to song-by-song manual downloading.
Downloaded files are stored in 'getalb/music/' directory.
Script works with Python 2.7.
Script uses BeautifulSoup library for parsing html pages.

## Version history

0.1.0 - Initial release.

0.2.0 - Almost all code have been refactored according to PEP 8.

0.2.1 - Fixed crash with no URL passed as input.

0.2.2 - Fixed savind albums to cwd. Albums are saved to 'getalb/music/' dir
irrespective from cwd.

0.2.3 - Fixed missing '/music' dir.

0.2.4 - Added function unify_album_name for deleting OS reserved characters.
Improved code readability.

## Known issues

## License

Copyright (c) 2015 Oleg Esenkov. See the LICENSE file for license rights and
limitations (MIT).
