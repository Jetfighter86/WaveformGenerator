import wx  # 2.8
import vlc

# import standard libraries
import os
import user


class Player(wx.Frame):
    """The main window has to deal with events.
    """
    ID_NEXT = 1 # Next button
    ID_END = 2 # End button
    ID_VOCAL = 3 # Vocal Button

    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, pos=wx.DefaultPosition, size=(200, 350))
        # Menu Bar
        # File Menu
        self.frame_menubar = wx.MenuBar()
        self.file_menu = wx.Menu()
        self.file_about = wx.Menu()
        self.file_menu.Append(1, "&Open", "Open from file..")
        self.file_menu.AppendSeparator()
        self.file_menu.Append(2, "&Close", "Quit")
        self.frame_menubar.Append(self.file_menu, "File")
        self.frame_menubar.Append(self.file_about, "About")
        self.file_about.Append(3, "&About", "me")
        self.SetMenuBar(self.frame_menubar)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=1)
        self.Bind(wx.EVT_MENU, self.OnExit, id=2)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=3)


        # Search  Panels
        searchpanel = wx.Panel(self, -1)
        searchlabel = wx.Panel(self, -1)
        self.searchlabel = wx.StaticText(searchlabel, -1, "Search Artist/Song")
        self.searchfield = wx.TextCtrl(searchpanel, -1, size=(140, -1))

        # Creating a display for search Results
        searchdispanel = wx.Panel(self, -1)
        searchdispanelbox = wx.BoxSizer(wx.HORIZONTAL)
        self.searchdispanelbox = wx.ListBox(searchdispanel, -1)


        # The second panel holds controls
        ctrlpanel = wx.Panel(self, -1)
        self.timeslider = wx.Slider(ctrlpanel, -1, 0, 0, 1000)
        self.timeslider.SetRange(0, 1000)
        pause = wx.Button(ctrlpanel, label="Pause")
        play = wx.Button(ctrlpanel, label="Play")
        stop = wx.Button(ctrlpanel, label="Stop")
        volume = wx.Button(ctrlpanel, label="Volume")
        self.volslider = wx.Slider(ctrlpanel, -1, 0, 0, 100, size=(100, -1))

        # Creating List box for  queue list
        qpanel = wx.Panel(self, -1, size=(1,300))
        qhbox = wx.BoxSizer(wx.HORIZONTAL)
        self.qhbox = wx.ListBox(qpanel, -1)
        qhbox.Add(self.qhbox, 1, wx.EXPAND | wx.ALL, 20)
        qbtnpanel = wx.Panel(qpanel, -1)
        qvbox = wx.BoxSizer(wx.VERTICAL)
        nextbtn = wx.Button(qbtnpanel, self.ID_NEXT, 'NEXT', size=(50,30))
        endbtn = wx.Button(qbtnpanel, self.ID_END, 'END', size=(50,30))
        vocalbtn = wx.Button(qbtnpanel, self.ID_VOCAL, 'VOCAL', size=(50,30))
        qvbox.Add((-1,20))
        qvbox.Add(nextbtn)
        qvbox.Add(endbtn, 0 , wx.TOP, 5)
        qvbox.Add(vocalbtn, 0 , wx.TOP, 5)
        qbtnpanel.SetSizer(qvbox)
        qhbox.Add(qbtnpanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        qpanel.SetSizer(qhbox)

        # Give a pretty layout to the controls
        ctrlbox = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        # box1 contains the timeslider
        box1.Add(self.timeslider, 1)
        # box2 contains some buttons and the volume controls
        box2.Add(play, flag=wx.RIGHT, border=5)
        box2.Add(pause)
        box2.Add(stop)
        box2.Add((-1, -1), 1)
        box2.Add(volume)
        box2.Add(self.volslider, flag=wx.TOP | wx.LEFT, border=5)
        # Merge box1 and box2 to the ctrlsizer
        ctrlbox.Add(box1, flag=wx.EXPAND | wx.BOTTOM, border=10)
        ctrlbox.Add(box2, 1, wx.EXPAND)
        ctrlpanel.SetSizer(ctrlbox)

        # Bind controls to events
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        self.Bind(wx.EVT_BUTTON, self.OnStop, stop)
        self.Bind(wx.EVT_BUTTON, self.OnToggleVolume, volume)
        self.Bind(wx.EVT_BUTTON, self.VocalToggle, vocalbtn)
        self.Bind(wx.EVT_SLIDER, self.OnSetVolume, self.volslider)
        self.Bind(wx.EVT_TEXT, self.Search, self.searchfield)

        # Put everything togheter
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(searchlabel, flag=wx.EXPAND | wx.LEFT)
        sizer.Add(searchpanel, flag=wx.EXPAND | wx.CENTER | wx.TOP)
        sizer.Add(searchdispanel, flag=wx.EXPAND | wx.LEFT)
        sizer.Add(ctrlpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP)
        sizer.Add(qpanel, flag=wx.EXPAND | wx.BOTTOM)
        self.SetSizer(sizer)
        self.SetMinSize((480, 300))

        # finally create the timer, which updates the timeslider
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        # VLC player controls
        self.Instance = vlc.Instance("--sub-source marq")
        self.player = self.Instance.media_player_new()
    def OnAbout(self, evt):
        """
        Show about menu in a separate box
        :param evt:
        :return:
        """
        message = """ My First Karaoke program. To my beloved dad!!!! """
        wx.MessageBox(message, 'Info')
    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()
    def OnOpen(self, evt):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        # self.OnStop(None)

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        dlg = wx.FileDialog(self, "Choose a file", "L:/temp/kara", "",
                            "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            # Creation
            self.Media = self.Instance.media_new(unicode(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            # Report the title of the file chosen
            title = self.player.get_title()
            # if an error was encountred while retriving the title, then use
            # filename
            if title == -1:
                title = filename
            self.SetTitle("%s - PhillipKARAOKplayer" % title)

            # set the window id where to render VLC's video output
            # self.player.set_xwindow(self.videopanel.getHandle())

            # FIXME: this should be made cross-platform
            self.OnPlay(None)

            # set the volume slider to the current volume
            self.volslider.SetValue(self.player.audio_get_volume() / 2)

        # finally destroy the dialog
        dlg.Destroy()
    def OnPlay(self, evt):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # wx.FileDialog to select a file
        if not self.player.get_media():
            self.OnOpen(None)
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")
                self.player.play()
            else:
                self.timer.Start()
    def OnPause(self, evt):
        """Pause the player.
        """
        self.player.pause()
    def OnStop(self, evt):
        """Stop the player.
        """
        self.player.stop()
        # reset the time slider
        self.timeslider.SetValue(0)
        self.timer.Stop()
    def VocalToggle(self,evt):
        """
        toggle vocal on/off
        :param evt:
        :return:
        :info:libvlc_audio_output_channel_t {
            libvlc_AudioChannel_Error = -1, libvlc_AudioChannel_Stereo = 1, libvlc_AudioChannel_RStereo = 2, libvlc_AudioChannel_Left = 3,
            libvlc_AudioChannel_Right = 4, libvlc_AudioChannel_Dolbys = 5
        """
        audio_channel = self.player.audio_get_channel()
        print audio_channel
        if audio_channel == 1:
            self.player.audio_set_channel(2)
        elif audio_channel == 2:
            self.player.audio_set_channel(3)
        else:
            self.player.audio_set_channel(1)
    def OnTimer(self, evt):
        """Update the time slider according to the current movie time.
        """
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        length = self.player.get_length()
        self.timeslider.SetRange(-1, length)

        # update the time on the slider
        time = self.player.get_time()
        self.timeslider.SetValue(time)
    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volslider.SetValue(self.player.audio_get_volume() / 2)
    def OnSetVolume(self, evt):
        """Set the volume according to the volume sider.
        """
        volume = self.volslider.GetValue() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")
    def Queuelist(self,evt):
        pass

    def Search(self,evt):
        dir = "C:/Users/Phillip/PycharmProjects/WaveformGenerator/karoke/listsong.txt"
        print self.searchfield.GetValue()
        value = self.searchfield.GetValue()
        self.searchdispanelbox.Append(value)
        pass



    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = wx.MessageDialog(self, errormessage, 'Error', wx.OK |
                                   wx.ICON_ERROR)
        edialog.ShowModal()


if __name__ == "__main__":
    # Create a wx.App(), which handles the windowing system event loop
    app = wx.App(False)
    # Create the window containing our small media player
    player = Player("Phillip Karaok Player")
    # show the player window centred and run the application
    player.Centre()
    player.Show()
    app.MainLoop() 
