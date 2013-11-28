
import sqlite3 as sqlite, Tkinter, ttk, tkFileDialog, tkMessageBox, time, sys, dbCon, gui


try:
    ScreenW = int(sys.argv[1])
    ScreenH = int(sys.argv[2])
except:        
    ScreenW = 1280                                                        #Change to your liking
    ScreenH = 600                                                        #Same here, this should be in a config as well

def main():
    global ScreenW,ScreenH
    root = Tkinter.Tk()
    root.geometry(("%dx%d")%(ScreenW,ScreenH))
    gui.MmntInterface(root)
    root.mainloop()
#    for database in databases:
#        dbCon.database.con.commit()
#        dbCon.database.con.close()
#        print 'closing', database.dbName
    return 0

if __name__ == '__main__':
    main()