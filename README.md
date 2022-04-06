
This  script can resync .srt subtitle files that have a fixed offset between the subtitles' timestamps and the media file's timestamps. It can also remove 
closed captions.

Options:

--ma : Add minutes (integers only)
--ms : Subtract minutes (integers only)
--sa : Add seconds (integers only)
--ss : Subtract seconds (integers only)
--nocc : Remove closed captions

Usage:

For example, to subtract 3 seconds from the timestamps:
python subtitlefix.py --ss 3 [PATH/]filename.srt

To remove closed captions:
python subtitlefix.py --nocc [PATH/]filename.srt

You can do more than one operation on the file at the same time. For example, to add 1  minute and 20 seconds and get rid of closed captions at the same time:
python subtitlefix.py --ma 1 --sa 20 --nocc [PATH/]filename.srt 
Note that the order of the options isn't important.

TODO:
Create a GUI with more features.
