import wx

app=wx.App()
dc=wx.ScreenDC()

# set line and fill style
dc.SetBrush(wx.TRANSPARENT_BRUSH) 
dc.SetPen(wx.Pen((255, 0, 0), width=3, style=wx.PENSTYLE_SOLID))


# draw (x, y, width, height)
while True:
    dc.DrawRectangle(100, 100, 200, 100)