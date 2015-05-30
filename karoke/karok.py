__author__ = 'Phillip'

import vlc, sys,os,subprocess,requests
import wx


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

    def main(self):

        try:
            from msvcrt import getch
        except ImportError:
            import termios
            import tty

            def getch():  # getchar(), getc(stdin)  #PYCHOK flake
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                return ch

        def end_callback(event):
            print('End of media stream (event %s)' % event.type)
            sys.exit(0)
        def end_callback(event):
            print('End of media stream (event %s)' % event.type)
            sys.exit(0)

        echo_position = False

        def pos_callback(event, player):
            if echo_position:
                sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type,
                                                          event.u.new_position * 100,
                                                          player.get_position() * 100))
            sys.stdout.flush()

        def print_version():
            """Print libvlc version"""
            try:
                print('Build date: %s (%#x)' % (build_date, hex_version()))
                print('LibVLC version: %s (%#x)' % (bytes_to_str(libvlc_get_version()), libvlc_hex_version()))
                print('LibVLC compiler: %s' % bytes_to_str(libvlc_get_compiler()))
                if plugin_path:
                    print('Plugin path: %s' % plugin_path)
            except:
                print('Error: %s' % sys.exc_info()[1])


        vlcPath = r'C:\Program Files (x86)\VideoLAN\VLC'
        moviePath = "C:\Users\Phillip\Videos\Friends\Friends Season 10\\"
        moviePath1 = r"C:\Users\Phillip\Videos\Friends\Friends Season 1"
        filename1 = r'Friends - [1x01] - The One where Monica gets a Roommate.mkv'
        filename = r"Friends - [10x08] - The One with the Late Thanksgiving.mkv"
        movie = moviePath + filename
        instance = vlc.Instance("--sub-source marq")
        media = instance.media_new(movie)
        player = instance.media_player_new()
        player.set_media(media)
        player.play()
        # Some marquee examples.  Marquee requires '--sub-source marq' in the
        # Instance() call above.  See <http://www.videolan.org/doc/play-howto/en/ch04.html>
        player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)
        player.video_set_marquee_int(vlc.VideoMarqueeOption.Size, 24)  # pixels
        player.video_set_marquee_int(vlc.VideoMarqueeOption.Position, vlc.Position.Bottom)
        if False:  # only one marquee can be specified
            player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 5000)  # millisec, 0==forever
            t = media.get_mrl()  # movie
        else:  # update marquee text periodically
            player.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 0)  # millisec, 0==forever
            player.video_set_marquee_int(vlc.VideoMarqueeOption.Refresh, 1000)  # millisec (or sec?)
            ##t = '$L / $D or $P at $T'
            t = '%Y-%m-%d  %H:%M:%S'
        player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, vlc.str_to_bytes(t))
        # Some event manager examples.  Note, the callback can be any Python
        # callable and does not need to be decorated.  Optionally, specify
        # any number of positional and/or keyword arguments to be passed
        # to the callback (in addition to the first one, an Event instance).
        event_manager = player.event_manager()
        event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, end_callback)
        event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, pos_callback, player)

        def mspf():
            """Milliseconds per frame."""
            return int(1000 // (player.get_fps() or 25))

        def print_info():
            """Print information about the media"""
            try:
                print_version()
                media = player.get_media()
                print('State: %s' % player.get_state())
                print('Media: %s' % bytes_to_str(media.get_mrl()))
                print('Track: %s/%s' % (player.video_get_track(), player.video_get_track_count()))
                print('Current time: %s/%s' % (player.get_time(), media.get_duration()))
                print('Position: %s' % player.get_position())
                print('FPS: %s (%d ms)' % (player.get_fps(), mspf()))
                print('Rate: %s' % player.get_rate())
                print('Video size: %s' % str(player.video_get_size(0)))  # num=0
                print('Scale: %s' % player.video_get_scale())
                print('Aspect ratio: %s' % player.video_get_aspect_ratio())
                #print('Window:' % player.get_hwnd()
            except Exception:
                print('Error: %s' % sys.exc_info()[1])

        def sec_forward():
            """Go forward one sec"""
            player.set_time(player.get_time() + 1000)

        def sec_backward():
            """Go backward one sec"""
            player.set_time(player.get_time() - 1000)

        def frame_forward():
            """Go forward one frame"""
            player.set_time(player.get_time() + mspf())

        def frame_backward():
            """Go backward one frame"""
            player.set_time(player.get_time() - mspf())

        def print_help():
            """Print help"""
            print('Single-character commands:')
            for k, m in sorted(keybindings.items()):
                m = (m.__doc__ or m.__name__).splitlines()[0]
                print('  %s: %s.' % (k, m.rstrip('.')))
            print('0-9: go to that fraction of the movie')

        def quit_app():
            """Stop and exit"""
            sys.exit(0)

        def toggle_echo_position():
            """Toggle echoing of media position"""
            global echo_position
            echo_position = not echo_position

        keybindings = {
            ' ': player.pause,
            '+': sec_forward,
            '-': sec_backward,
            '.': frame_forward,
            ',': frame_backward,
            'f': player.toggle_fullscreen,
            'i': print_info,
            'p': toggle_echo_position,
            'q': quit_app,
            '?': print_help,
        }

        print('Press q to quit, ? to get help.%s' % os.linesep)
        while True:
            k = getch()
            print('> %s' % k)
            if k in keybindings:
                keybindings[k]()
            elif k.isdigit():
                # jump to fraction of the movie.
                player.set_position(float('0.' + k))


    def test(self):
        path = 'Friends - [2x02] - The One with the Breast Milk.mkv'
        movie = os.path.expanduser(path)
        print movie
        instance = vlc.Instance("--sub-source marq")
        media = instance.media_new(movie)
        player = instance.media_player_new()
        player.set_media(media)
        # player.play()
        # Some marquee examples.  Marquee requires '--sub-source marq' in the
        # Instance() call above.  See <http://www.videolan.org/doc/play-howto/en/ch04.html>
        # player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)



if __name__ == '__main__':
    vlcPath = r'C:\Program Files (x86)\VideoLAN\VLC'
    try:
        vlcplayer = VLCPlayer(vlcPath)
        vlcplayer.main()
    except Exception:
        print Exception.message

