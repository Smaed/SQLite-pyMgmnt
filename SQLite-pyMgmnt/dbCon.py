
import sqlite3 as sqlite, Tkinter, ttk, tkFileDialog, tkMessageBox, time, sys, gui

class database(object):
    
    def __init__(self,db):
        self.db = db
        self.dbSplit = self.db.split('/') # FIXME: Unix-specific code
        self.dbName = self.dbSplit[-1]
        self.tables = []
        try:
            self.con = sqlite.connect(self.db)
            try:
                self.con.execute('pragma foreign_keys = on')
            except:
                print 'No Foreign'                                        #Placeholder, could be a popup informing the user
            self.cur = self.con.cursor()
        except:
            log('Error','Could not open database' + db)
