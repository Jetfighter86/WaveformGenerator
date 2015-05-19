__author__ = 'Phillip'

import wx

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example,self).__init__(*args,**kwargs)
        self.InitUI()
    def InitUI(self):
        menubar = wx.MenuBar()
# Creating item Object to file menu
        fileMenu = wx.Menu()
        aboutMenu = wx.Menu()
        viewMenu = wx.Menu()
# Adding item to file menu
        menubar.Append(fileMenu, '&File')
        menubar.Append(aboutMenu,'&About')
        menubar.Append(viewMenu, '&View')
# Adding items or submenu to the menu
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
# Create a sub menu to be attached to main menu
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mails...')
# Attached to the main menu called import
        fileMenu.AppendMenu(wx.ID_ANY, 'I&mport', imp)
# Quit function is bound to this object
        fitem= fileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q')
        Aitem= aboutMenu.Append(wx.ID_ABOUT, 'About\tAlt+A')
# Creating a ITEM-CHECKED MENU
        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shst1 = viewMenu.Append(wx.ID_ANY, 'Show statusbar1', 'Show Statusbar', kind=wx.ITEM_RADIO)


# Bind def Quit to fitem, which is an object being append to Filemenu
        self.Bind(wx.EVT_MENU,self.OnQuit,fitem)
        self.Bind(wx.EVT_MENU,None,Aitem)

# Set title, default size and position
        self.SetMenuBar(menubar)
        self.SetSize((300,300))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)

    def OnQuit(self,e):
        self.Close()

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()