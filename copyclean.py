#!/usr/bin/python

import re
import os
import datetime
import shutil
import syslog


#Define path of the files to be copied
pathfromfiles = ''
#Define path for the destination of the copied files
pathtobackups = ''
#Files older than will be copied and deleted
keepDays = 30

#Search backup destiantion for files that are older that number of days specified and delete.  Note this looks at the timestamp in the file name no the system timestamp.
for dirpath, dirnames, filenames in os.walk(pathfromfiles):
    for file in filenames:
        dt = re.search('(?<=fwsm-)\d+', file) #Positive lookbehind to pull out the timestamp
        if dt:
            dtObj = datetime.datetime.strptime(dt.group(), "%Y%m%d") #This creates a datetime object out of the result of the regex above
            if datetime.datetime.now() - datetime.timedelta(days=keepDays) > dtObj:
                shutil.copy(os.path.join(pathfromfiles, file), os.path.join(pathtobackups, file))
                syslog.syslog('Removed file older than {0} days: {1}'.format(str(keepDays), file))
            else:
                pass
        else:
            pass
