import sys 
import argparse 
import io
from pathlib import Path
from datetime import timedelta
import re


sub_parse = argparse.ArgumentParser(prog='SubtitleFix', description="This script can resync '.srt' subtitle files that have a fixed offset between the subtitles' timestamps and the media file's timestamps. It can also remove closed captions.")
sub_parse.add_argument('subfile', help='The path of the subtitle file.')
sub_parse.add_argument('--ma', type=int, help='Add minutes (integers only).')
sub_parse.add_argument('--ms', type=int, help='Subtract minutes (integers only).')
sub_parse.add_argument('--sa', type=int, help='Add seconds (integers only).')
sub_parse.add_argument('--ss', type=int, help='Subtract seconds (integers only).')
sub_parse.add_argument('--nocc', action='store_true', help='Remove closed captions.')
allargs = sub_parse.parse_args()

if Path(allargs.subfile).exists()==False:
 raise FileNotFoundError("File not found. If you're sure the file exists, check the name and path you typed.")

subfilelst=allargs.subfile.rsplit('.',1)
if(len(subfilelst)>1 and subfilelst[1]!='srt'):
 raise TypeError('Only .srt files are supported.')

arglist=[allargs.ma,allargs.ms,allargs.sa,allargs.ss]
for i in arglist:
 if isinstance(i,int) and i<=0:
  raise ValueError('Only positive numbers are accepted.')
if any(arglist)==False and allargs.nocc==False:
 raise ValueError('No option was used.')
 

def add_time(filerw,argtimedelta):
 txtobj=io.StringIO()
 for line in filerw.readlines():
  if(line.count(':')==4):
   #e.g. 00:00:42,159 --> 00:00:46,359
   hr1=int(line[0:2])
   min1=int(line[3:5])
   sec1=int(line[6:8])
   subtimedelta1=timedelta(seconds=sec1,minutes=min1,hours=hr1)
   strttimedelta=subtimedelta1+argtimedelta
   strttime=str(strttimedelta) 
   if(strttime[1]==':'):
    strttime='0'+strttime
   hr2=int(line[17:19])
   min2=int(line[20:22])
   sec2=int(line[23:25])
   subtimedelta2=timedelta(seconds=sec2,minutes=min2,hours=hr2)
   endtimedelta=subtimedelta2+argtimedelta
   endtime=str(endtimedelta)
   if(endtime[1]==':'):
    endtime='0'+endtime
   line=strttime+line[8:17]+endtime+line[25:29]+'\n'
  txtobj.writelines(line)
 filerw.seek(0)
 filerw.truncate()
 txtobj.seek(0)
 objtxt=txtobj.read() 
 filerw.write(objtxt)
 filerw.seek(0)


def subtract_time(filerw,argtimedelta):
 txtobj=io.StringIO()
 y=True
 for line in filerw.readlines():
  if(line.count(':')==4):
   #e.g. 00:00:42,159 --> 00:00:46,359
   hr1=int(line[0:2])
   min1=int(line[3:5])
   sec1=int(line[6:8])
   subtimedelta1=timedelta(seconds=sec1,minutes=min1,hours=hr1)
   strttimedelta=subtimedelta1-argtimedelta
   strttime=str(strttimedelta) 
   if('day' in strttime):
    y=False
    break
   if(strttime[1]==':'):
    strttime='0'+strttime
   hr2=int(line[17:19])
   min2=int(line[20:22])
   sec2=int(line[23:25])
   subtimedelta2=timedelta(seconds=sec2,minutes=min2,hours=hr2)
   endtimedelta=subtimedelta2-argtimedelta
   endtime=str(endtimedelta)
   if(endtime[1]==':'):
    endtime='0'+endtime
   line=strttime+line[8:17]+endtime+line[25:29]+'\n'
  txtobj.writelines(line)
 if(y==True):
  filerw.seek(0)
  filerw.truncate()
  txtobj.seek(0)
  objtxt=txtobj.read() 
  filerw.write(objtxt)
  filerw.seek(0)
 else:
  raise ValueError('Subtraction not possible because earliest time cannot be earlier than 00:00:00.')
  
  
def nocc(filerw):
 filestr=filerw.read()
 noccstr=re.sub(r'[- ]*\([A-Z \W]*\)','',filestr)
 filerw.seek(0)
 filerw.truncate()
 filerw.write(noccstr)
 filerw.seek(0)


with open(allargs.subfile,'r+') as filerw:
 if(allargs.ma):
  argtimedelta=timedelta(minutes=allargs.ma)
  add_time(filerw,argtimedelta)
  print('Minutes successfully added.')
 if(allargs.ms):
  argtimedelta=timedelta(minutes=allargs.ms)
  subtract_time(filerw,argtimedelta)
  print('Minutes successfully subtracted.')
 if(allargs.sa):
  argtimedelta=timedelta(seconds=allargs.sa)
  add_time(filerw,argtimedelta)
  print('Seconds successfully added.')
 if(allargs.ss):
  argtimedelta=timedelta(seconds=allargs.ss)
  subtract_time(filerw,argtimedelta)
  print('Seconds successfully subtracted.')
 if(allargs.nocc):
  nocc(filerw)
  print('Closed captions successfully removed.')
