#Ty Davisson - Project 4
import wx
import requests
import sqlite3 as db
import datetime

class Frame(wx.Frame):
    def __init__(self): 
        super().__init__(None, id=-1, title='Tech Stocks', size =(800, 600))

        panel = wx.Panel(self, -1)
        
        # Labels - top row
        self.dateLbl = wx.StaticText(panel, -1, "Today's Date: ")
        self.totalLbl = wx.StaticText(panel, -1, 'Total: ')
        
        # List Control - middle row
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, size=(732, 300))
        
        # Columns
        self.list.InsertColumn(0, 'Comapany', width=122) 
        self.list.InsertColumn(1, 'Symbol', width=122)
        self.list.InsertColumn(2, 'Purchase Price', width=122) 
        self.list.InsertColumn(3, 'Current Price', width=122) 
        self.list.InsertColumn(4, 'Shares', width=122) 
        self.list.InsertColumn(5, 'Gain/Loss', width=122)

        # Buttons - bottom row
        self.displayBtn = wx.Button(panel, -1, 'Display', size=(-1, 30))  
        self.cancelBtn = wx.Button(panel, -1, 'Cancel', size=(-1, 30)) 
        
        self.displayBtn.Bind(wx.EVT_BUTTON, self.onDisplay)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel) 
        
        # Box Sizers
        # top - labels
        lblSizer = wx.BoxSizer(wx.VERTICAL)

        lblSizer.Add(self.dateLbl, 1, wx.ALIGN_CENTER |wx.ALL, border= 15)
        lblSizer.Add(self.totalLbl, 1, wx.ALIGN_CENTER | wx.ALL, border= 15)                                                               
        # bottom - buttons
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btnSizer.Add(self.displayBtn, 1, wx.ALIGN_CENTER |wx.ALL, border= 15)
        btnSizer.Add(self.cancelBtn, 1, wx.ALIGN_CENTER |wx.ALL, border= 15)
        # all - labels, list, buttons
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        mainSizer.Add(lblSizer, 1, wx.ALIGN_CENTER |wx.ALL, border= 10)
        mainSizer.Add(self.list, 1, wx.ALIGN_CENTER |wx.ALL, border= 10)
        mainSizer.Add(btnSizer, 1, wx.ALIGN_CENTER |wx.ALL, border= 10)

        panel.SetSizer(mainSizer)
        
    # Methods
    def setTime(self):
        x = datetime.datetime.now()
        date = x.strftime("%A %B %d, %Y : %I:%M %p")
        self.dateLbl.SetLabel(f"Date: {date}")
        
    def onDisplay(self, event):
        self.setTime()
        # Connect to db
        try:
            conn = db.connect('tech_stocks.db')
            cur = conn.cursor()
                
            cur.execute('SELECT * FROM dow_stocks')
            dbData = cur.fetchall()      
        except db.Error as error:
            dlg = wx.MessageDialog(self, str(error), 'Error occurred')
            dlg.ShowModal()
                  
        # Make api calls   
        #API key 
        tok = 'xyz' #removed for security, add your own by claiming it at https://finnhub.io/
        # Total gain/loss
        totalGainLoss = 0
        for row in dbData:
            url = 'https://finnhub.io/api/v1/quote?symbol='+ row[3] + '&token=' + tok
            response = requests.get(url)
        # Get Prices
            apiData = response.json()
            currentPrice = apiData['c']
            purchasePrice = row[5]
            shares = row[4]
            gainLoss = round((currentPrice - purchasePrice) * shares, 2)
            totalGainLoss += gainLoss
        # Append to list 
            self.list.Append((row[1], row[3], purchasePrice, currentPrice, shares, gainLoss))
        
        # Set total label
        self.totalLbl.SetLabel(f"Total: {totalGainLoss}")
    def onCancel(self, event):
        self.Close()    
    
if __name__ == "__main__":
    app = wx.App()
    frame = Frame()
    frame.Show(True)
    app.MainLoop()      