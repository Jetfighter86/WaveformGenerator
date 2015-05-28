__author__ = 'Phillip'

import vlc, sys,os,subprocess,requests

class VLCPlayer:

    def __init__(self,vlcPath):
        self.VLCPATH = vlcPath
        os.chdir(self.VLCPATH)

    def vlcParseFilename(self,filename, cmd='',pathdir=''):
        try:
            if pathdir:
                if pathdir[-1] != '\\':
                    pathdir = str(pathdir) + '/'
            newStr = pathdir + filename
            newStr = str(newStr).replace(' ','%20')
            newStr = str(newStr).replace('[','%5B')
            newStr = str(newStr).replace(']','%5D')
            newStr = str(newStr).replace("'",'%27')
            newStr = str(newStr).replace("\\",'/')
            if cmd == '':
                return newStr
            elif cmd == 'openFile' and (pathdir):
                return 'file:///' + newStr
        except BaseException:
            return BaseException.args

    def openFile(self,filepath):

        filelink=''


if __name__ == '__main__':
    vlcPath = r'C:\Program Files (x86)\VideoLAN\VLC'
    moviePath = "C:\Users\Phillip\Videos\Friends\Friends Season 10"
    moviePath1 = r"C:\Users\Phillip\Videos\Friends\Friends Season 1"
    filename1 = r'Friends - [1x01] - The One where Monica gets a Roommate.mkv'
    filename = r"Friends - [10x08] - The One with the Late Thanksgiving.mkv"
    VLCObj = VLCPlayer(vlcPath)
    print VLCObj.vlcParseFilename(filename,cmd='openFile',pathdir=moviePath)
    print VLCObj.vlcParseFilename(filename1,cmd='openFile',pathdir=moviePath1)
    # VLCObj.openFile()
    requests.get()