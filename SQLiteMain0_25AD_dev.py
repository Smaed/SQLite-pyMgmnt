#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as sqlite, Tkinter, ttk, tkFileDialog, tkMessageBox, time, sys


try:
	ScreenW = int(sys.argv[1])
	ScreenH = int(sys.argv[2])
except:		
	ScreenW = 1280														#Change to your liking
	ScreenH = 600														#Same here, this should be in a config as well

databases = []															#Central for it to work, this contains all Database connections

class database:
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
				print 'No Foreign'										#Placeholder, could be a popup informing the user
			self.cur = self.con.cursor()
		except:
			log('Error','Could not open database' + db)

class MmntInterface:
	def __init__(self,parent):
		self.parent = parent
		self.parent.title("SQLiteMgment v0.25AD")
		self.CreateWidgets(self.parent)
		
	def CreateWidgets(self, parent):
		self.parent = parent
		s1 = ttk.Style()
#		s1.configure('f1.TFrame', background='grey')					
		s2 = ttk.Style()
#		s2.configure('f2.TFrame', background='grey')
		s3 = ttk.Style()
#		s3.configure('f3.TFrame', background='grey')
		s4 = ttk.Style()
#		s4.configure('f4.TFrame', background='grey')
		s5 = ttk.Style()
#		s4.configure('Disabled.TCheckbutton', relief='sunken')
		
		self.frame1 = ttk.Frame(self.parent, style='f1.TFrame')
		self.frame1.pack(fil='x')
		
		self.load = ttk.Button(self.frame1)
		self.load["text"] = "Load DB"
		self.load["command"] = lambda: self.LoadDB('load')
		self.load.pack(side='left', padx = 5, pady = 5)
		
		self.create = ttk.Button(self.frame1)
		self.create["text"] = "Create DB"
		self.create["command"] = lambda: self.LoadDB('create')
		self.create.pack(side='left', padx = 5, pady = 5)

		self.frame2 = ttk.Frame(self.parent, style='f2.TFrame')
		self.frame2.pack(side='left', fill='both')

		self.tree = ttk.Treeview(self.frame2, selectmode='browse')
		self.vsb = ttk.Scrollbar(self.frame2, orient="vertical", command = self.tree.yview)
		self.tree.config(yscrollcommand=self.vsb.set)
		
		self.tree.pack(side='left', fill='both', padx=3, pady=8)
		self.vsb.pack(side='left', fill='both')
		self.tree.bind("<<TreeviewSelect>>", self.OnClick)

		self.frame3 = ttk.Frame(self.parent, style='f3.TFrame')
		self.frame3.pack(side='left', fill='both', expand='yes')
		
		self.n = ttk.Notebook(self.frame3)		
		self.n.pack(side='left', fill='both', expand='yes', padx=5, pady=5)
		
		self.f1 = ttk.Frame(self.n, style='f1.TFrame')
		self.f2 = ttk.Frame(self.n)
		self.f3 = ttk.Frame(self.n)
		self.f4 = ttk.Frame(self.n)
		
		self.f1.pack(side='top', fill='both', expand='yes')
		self.f2.pack(side='top', fill='both', expand='yes')
		self.f3.pack(side='top', fill='both', expand='yes')
		
		self.n.add(self.f1, text='Data')
		self.n.add(self.f2, text='Edit')
		self.n.add(self.f3, text='SQL')
		self.n.add(self.f4, text='Create')
		
		self.frame5 = ttk.Frame(self.f3, style='f2.TFrame')
		self.frame5.pack()
		
		self.SQLEntry = ttk.Entry(self.frame5)
		self.SQLEntry.pack(side='left')
		
		self.SQLButton = ttk.Button(self.frame5,text='Knapp')
		self.SQLButton["command"] = self.sql
		self.SQLButton.pack(side='left')
		
		self.SQLMessage = ttk.Label(self.frame5, text='Message: ')
		self.SQLMessage.pack(side='left')
		
		self.frame6 = ttk.Frame(self.f2, style='f2.TFrame')
		self.frame6.pack(fill='x')
		
		self.NameChange = Tkinter.StringVar()
		self.TableEntry = ttk.Entry(self.frame6, textvariable=self.NameChange)
		self.TableEntry.pack()
		
		self.EditTableName = ttk.Button(self.frame6)
		self.EditTableName["command"] = self.ChangeName
		self.EditTableName["text"] = "Rename"
		self.EditTableName.pack()
		
		self.NumOfCol = Tkinter.IntVar()
		Cols = (0,0,1,2,3,4,5)
		self.AddCols = ttk.OptionMenu(self.frame6, self.NumOfCol, *Cols)
		self.NumOfCol.set(0)
		self.AddCols.pack(side='left', padx=10, pady=10)		
		
		self.AddColsButton = ttk.Button(self.frame6)
		self.AddColsButton["text"] = "Add"
		self.AddColsButton["command"] = lambda: self.AddColumn(self.canvasf2)
		self.AddColsButton.pack(side='left', padx = 5, pady = 5)
		
		self.EditMessage = ttk.Label(self.frame6, text='Message: ')
		self.EditMessage.pack(side='left')
		
		self.frame7 = ttk.Frame(self.f4, style='f2.TFrame')
		self.frame7 = ttk.Frame(self.f4, style='f2.TFrame')
		self.frame7.pack(fill='x')
		
		self.TableName = Tkinter.StringVar()
		self.NewTable = ttk.Entry(self.frame7, textvariable=self.TableName)
		self.NewTable.pack()
		
		self.NewTableName = ttk.Label(self.frame7)
		self.NewTableName["text"] = "Name"
		self.NewTableName.pack()
		
		self.NewTableCol = Tkinter.IntVar()
		Cols = (0,0,1,2,3,4,5)
		self.TableCols = ttk.OptionMenu(self.frame7, self.NumOfCol, *Cols)
		self.NewTableCol.set(0)
		self.TableCols.pack(side='left', padx=10, pady=10)		
		
		self.TableColsButton = ttk.Button(self.frame7)
		self.TableColsButton["text"] = "Add"
		self.TableColsButton["command"] = lambda: self.AddColumn(self.canvasf4)
		self.TableColsButton.pack(side='left', padx = 5, pady = 5)
		
		self.NewTableMessage = ttk.Label(self.frame7, text='Message: ')
		self.NewTableMessage.pack(side='left')

		self.canvasf1 = Tkinter.Canvas(self.f1)
		self.canvasf2 = Tkinter.Canvas(self.f2)
		self.canvasf3 = Tkinter.Canvas(self.f3)
		self.canvasf4 = Tkinter.Canvas(self.f4)
		
		self.c1vsb = ttk.Scrollbar(self.f1, orient="vertical", command = self.canvasf1.yview)
		self.c2vsb = ttk.Scrollbar(self.f2, orient="vertical", command = self.canvasf2.yview)
		self.c3vsb = ttk.Scrollbar(self.f3, orient="vertical", command = self.canvasf3.yview)
		self.c4vsb = ttk.Scrollbar(self.f4, orient="vertical", command = self.canvasf4.yview)

		self.c1hsb = ttk.Scrollbar(self.f1, orient="horizontal", command = self.canvasf1.xview)
		self.c2hsb = ttk.Scrollbar(self.f2, orient="horizontal", command = self.canvasf2.xview)
		self.c3hsb = ttk.Scrollbar(self.f3, orient="horizontal", command = self.canvasf3.xview)
		self.c4hsb = ttk.Scrollbar(self.f4, orient="horizontal", command = self.canvasf4.xview)		
				
		self.canvasf1.config(yscrollcommand=self.c1vsb.set)
		self.canvasf2.config(yscrollcommand=self.c2vsb.set)
		self.canvasf3.config(yscrollcommand=self.c3vsb.set)
		self.canvasf4.config(yscrollcommand=self.c4vsb.set)
		
		self.canvasf1.config(xscrollcommand=self.c1hsb.set)
		self.canvasf2.config(xscrollcommand=self.c2hsb.set)
		self.canvasf3.config(xscrollcommand=self.c3hsb.set)
		self.canvasf4.config(xscrollcommand=self.c4hsb.set)

		self.c1hsb.pack(side='bottom', fill='x')
		self.c2hsb.pack(side='bottom', fill='x')
		self.c3hsb.pack(side='bottom', fill='x')
		self.c4hsb.pack(side='bottom', fill='x')

		self.c1vsb.pack(side='right', fill='y')
		self.c2vsb.pack(side='right', fill='y')
		self.c3vsb.pack(side='right', fill='y')
		self.c4vsb.pack(side='right', fill='y')
		
		self.canvasf1.pack(side='top', fill='both', expand = 'yes')
		self.canvasf2.pack(side='top', fill ='both', expand = 'yes')
		self.canvasf3.pack(side='top', fill='both', expand = 'yes')
		self.canvasf4.pack(side='top', fill='both', expand = 'yes')
		
	def OnClick(self,event):
		parent = self.getParent()[0]
		ChildIndex = self.getParent()[2]

		if self.tree.parent(self.tree.selection()[0]) != '':
			self.CreateData(parent,ChildIndex)
			self.NameChange.set(databases[parent].tables[ChildIndex])
		
	def	getParent(self):
		try:
			item = self.tree.selection()[0]
			parentIndex = self.tree.parent(item)
			ChildIndex = self.tree.index(item)
		except:
			return '','',''
	
		if parentIndex != '':
			return int(parentIndex)-1,parentIndex, ChildIndex
		else:
			return int(item) - 1,item, ChildIndex
	
	def AddTable(self, Columns):
		parent = self.getParent()[0]
		if parent != '':
			table = self.TableName.get()
			
			for Column in Columns:
				name = Column[0].get()
				DataType = Column[1].get()
				Prim ,Auto ,NNull ,Uni = '','','',''
				
				if Column[2].get() == 1:
					Prim = 'PRIMARY KEY'
				if Column[4].get()	 == 1:
					Auto = 'AUTOINCREMENT'
				if Column[8].get() == 1:
					NNull =	'NOT NULL'
				if Column[10].get() == 1:
					Uni = 'UNIQUE'
					
				if Column[6].get() == 0:
					Col = name, DataType, Prim, Auto, NNull, Uni
				else:		
					RefTable = Column[12].get()
					RefCol = Column[13].get()
					Col = name, DataType, Prim, Auto, NNull, Uni, 'REFERENCES %s(%s)' % (RefTable,RefCol)
				print Col	
												
	def EditTable(self, Columns):
		parent = self.getParent()[0]
		ChildIndex = self.getParent()[2]
		if parent != '' or ChildIndex != '':
#		if self.tree.parent(self.tree.selection()[0]) != '':
			table = databases[parent].tables[ChildIndex]
			for Column in Columns:
				name = Column[0].get()
				DataType = Column[1].get()
				Prim = ''
				Auto = ''
				Forign = ''
				NNull = ''
				Uni = ''
				
				if Column[2].get() == 1:
					Prim = 'PRIMARY KEY'
				if Column[4].get()	 == 1:
					Auto = 'AUTOINCREMENT'
				if Column[8].get() == 1:
					NNull =	'NOT NULL'
				if Column[10].get() == 1:
					Uni = 'UNIQUE'
				try:
					if Column[6].get() == 0:
#						print u'ALTER TABLE {t} ADD COLUMN {n} {d} {a} {nn} {u}'.format(t=table,n=name,d=DataType,a=Auto,nn=NNull,u=Uni)
						databases[parent].cur.execute(u"ALTER TABLE {t} ADD COLUMN {n} {d} {p} {a} {nn} {u}".format(t=table,n=name,d=DataType,p=Prim,a=Auto,nn=NNull,u=Uni))
					
					else:
						RefTable = Column[12].get()
						RefCol = Column[13].get()
#						print u"ALTER TABLE {t} ADD COLUMN {n} {d} {nn} {u} REFERENCES {RF}({RC})".format(t=table,n=name,d=DataType,nn=NNull,u=Uni,RF=RefTable,RC=RefCol)
						databases[parent].cur.execute(u"ALTER TABLE {t} ADD COLUMN {n} {d} {nn} {u} REFERENCES {RF}({RC})".format(t=table,n=name,d=DataType,nn=NNull,u=Uni,RF=RefTable,RC=RefCol))
					self.EditMessage.configure(text='Message: ')
				except (sqlite.OperationalError,sqlite.IntegrityError), e:
						self.EditMessage.configure(text='Message:%s' % (unicode(e.message).encode("utf-8")))
		else:
			self.EditMessage.configure(text='Choose a table to configure')
			
	def ChangeName(self):												#Currently not working as intended, looking into it at the moment
		parent = self.getParent()[0]
		ChildIndex = self.getParent()[2]
		if !(parent == '' or ChildIndex == ''):
			table = databases[parent].tables[ChildIndex]
			NewName = self.TableEntry.get()
			try:
				databases[parent].cur.execute(u"ALTER TABLE {t} RENAME TO {n}".format(t=table, n=NewName))
				self.changeTables(parent)
			except (sqlite.OperationalError,sqlite.IntegrityError), e:
				self.EditMessage.configure(text='Message:%s' % (unicode(e.message).encode("utf-8")))
		else:
			self.EditMessage.configure(text='Open a database first')
				
	def CreateData(self,parent,ChildIndex):
		table = databases[parent].tables[ChildIndex]
		command = u"SELECT * FROM {t}".format(t=table)
		self.ShowResult(parent, command, self.canvasf1)
		
	def sql(self):
		parent = self.getParent()[0]
		command = self.SQLEntry.get()
		
		try:
			self.ShowResult(parent, command, self.canvasf3)
			self.SQLMessage.configure(text='Message: ')
		except (sqlite.OperationalError,sqlite.IntegrityError), e:
			self.SQLMessage.configure(text='Message:\n%s\n%s' % (command,unicode(e.message).encode("utf-8")))
			
	def AddColumn(self,Canvas):
		try:
			self.frame4.destroy()										#Needed to destroy the old instance 
		except AttributeError:
			pass
		Canvas.delete("all")
		self.frame4 = ttk.Frame(Canvas, style='f1.TFrame')	
		self.frame4.grid()
		Canvas.create_window(0, 0, anchor='nw' ,window=self.frame4)
		NumOfColumns = self.NumOfCol.get()
	
		Columns = []
		
		ttk.Label(self.frame4, text='Name').grid(column=0, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Data Type').grid(column=1, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Primary key').grid(column=2, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Auo Increment').grid(column=3, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Foreign Key').grid(column=4, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Not Null').grid(column=5, row=0, sticky='n,s,w,e')
		ttk.Label(self.frame4, text='Uni').grid(column=6, row=0, sticky='n,s,w,e')
		
		self.ForignTable = ttk.Label(self.frame4, text='From Table')
		self.ForignCol = ttk.Label(self.frame4, text='Refering to')
		self.ForignTable.grid(column=7, row=0, sticky='n,s,w,e')
		self.ForignCol.grid(column=8, row=0, sticky='n,s,w,e')
		self.ForignTable.grid_remove()
		self.ForignCol.grid_remove()
		
		for Col in range(NumOfColumns):
			Columns.append([]) 											#For readabillity it could be better to use a dictionary
			
			Columns[Col].append(ttk.Entry(self.frame4))
			Columns[Col][0].grid(column=0, row=Col +1, sticky='n,s,w,e')
			
			Columns[Col].append(Tkinter.StringVar())
			Values = ('TEXT','TEXT','INTEGER','REAL','NUMERIC','NONE')
			datatypes = ttk.OptionMenu(self.frame4, Columns[Col][1], *Values)
			Columns[Col][1].set('TEXT')
			datatypes.grid(column=1, row=Col +1, sticky='n,s,w,e')
			
			Columns[Col].append(Tkinter.IntVar())	#Prime, [2] IntVar, [3] CheckBox
			Columns[Col].append(ttk.Checkbutton(self.frame4, variable=Columns[Col][2], command=lambda: self.UpdateCheck(Columns)))
			Columns[Col][3].grid(column=2, row=Col +1)
			
			Columns[Col].append(Tkinter.IntVar())  #Auto, [4] IntVar, [5] CheckBox
			Columns[Col].append(ttk.Checkbutton(self.frame4, variable=Columns[Col][4], command=lambda: self.UpdateCheck(Columns)))
			Columns[Col][5].grid(column=3, row=Col +1)
			
			Columns[Col].append(Tkinter.IntVar())  #Foreign, [6] IntVar, [7] CheckBox
			Columns[Col].append(ttk.Checkbutton(self.frame4, variable=Columns[Col][6], command=lambda: self.UpdateCheck(Columns)))
			Columns[Col][7].grid(column=4, row=Col +1)
			
			Columns[Col].append(Tkinter.IntVar())  #Not null, [8] IntVar, [9] CheckBox
			Columns[Col].append(ttk.Checkbutton(self.frame4, variable=Columns[Col][8], command=lambda: self.UpdateCheck(Columns)))
			Columns[Col][9].grid(column=5, row=Col +1)
			
			Columns[Col].append(Tkinter.IntVar())  #uni, [10] IntVar, [11] CheckBox
			Columns[Col].append(ttk.Checkbutton(self.frame4, variable=Columns[Col][10], command=lambda: self.UpdateCheck(Columns)))
			Columns[Col][11].grid(column=6, row=Col +1)
			
			Columns[Col].append(ttk.Entry(self.frame4))
			Columns[Col][12].grid(column=7, row=Col +1, sticky='n,s,w,e')
			Columns[Col][12].grid_remove()
			
			Columns[Col].append(ttk.Entry(self.frame4))
			Columns[Col][13].grid(column=8,row=Col +1, sticky='n,s,w,e')
			Columns[Col][13].grid_remove()
			
#			self.frame4.update_idletasks()
#			Canvas.config(scrollregion=self.canvasf2.bbox('all'))					
		
		if NumOfColumns != 0 and Canvas == self.canvasf2:
			self.Add = ttk.Button(self.frame4, text='Add', command=lambda: self.EditTable(Columns)).grid(column=1, row=Col +2)
		if NumOfColumns != 0 and Canvas == self.canvasf4:	
			self.Add = ttk.Button(self.frame4, text='Add', command=lambda: self.AddTable(Columns)).grid(column=1, row=Col +2)
			
		self.frame4.update_idletasks()
		Canvas.config(scrollregion=self.canvasf2.bbox('all'))
			
	def UpdateCheck(self, Columns):										#This need extentions for the working combinations
			self.ForignTable.grid_remove()
			self.ForignCol.grid_remove()
			for Col in Columns:
				#Primary or Auto disable Foreign
				if Col[2].get() == 1 or Col[4].get() == 1:
					Col[6].set(0)
					Col[7].state(['disabled'])
					Col[7]['style'] = 'Disabled.TCheckbutton'	
				else:
					Col[7].state(['!disabled'])
					Col[7]['style'] = 'TCheckbutton'
				
				#Foreign disable Primary and Auto
				if Col[6].get() == 1:
					Col[2].set(0)
					Col[4].set(0)
					Col[3].state(['disabled'])
					Col[3]['style'] = 'Disabled.TCheckbutton'	
					Col[5].state(['disabled'])
					Col[5]['style'] = 'Disabled.TCheckbutton'
					self.ForignTable.grid()
					self.ForignCol.grid()
					Col[12].grid()
					Col[13].grid()		
				else:
					Col[3].state(['!disabled'])
					Col[3]['style'] = 'TCheckbutton'
					Col[5].state(['!disabled'])
					Col[5]['style'] = 'TCheckbutton'
					Col[12].grid_remove()
					Col[13].grid_remove()
	
	def ShowResult(self, parent, command, canvas):
		try:
			self.frame4.destroy()										#Needed to destroy the old instance 
		except AttributeError:
			pass
		canvas.delete("all")											#Makes sure the canvas is empty before data is drawn on it

		self.frame4 = ttk.Frame(canvas, style='f4.TFrame')	
		self.frame4.grid()
		
		canvas.create_window(0, 0, anchor='nw' ,window=self.frame4)
		
		oldValue = len(databases[parent].tables)
		databases[parent].cur.execute(command)
		databases[parent].con.commit()
		rows = databases[parent].cur.fetchall()
		try:
			ColNames = [tuple[0] for tuple in databases[parent].cur.description]
		except TypeError:
			ColNames = ''
		databases[parent].cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
		newValue = len(databases[parent].cur.fetchall())
		
		if newValue != oldValue:
			self.changeTables(parent)			
		else:	
			for key,Name in enumerate(ColNames):
				lab = ttk.Label(self.frame4, text=Name)
				lab.grid(column=key, row=0, sticky='n,s,w,e')

			for RowKey,Row in enumerate(rows[:50]):
				for ColKey,Col in enumerate(Row):
					if Col == None:
						Col = ''
					lab = ttk.Entry(self.frame4)
					lab.insert(ColKey,Col)
					lab.grid(column=ColKey, row=RowKey + 1, sticky='n,s,w,e')
#				time.sleep(0.002)	
			self.frame4.update_idletasks()
			canvas.config(scrollregion=canvas.bbox('all'))

	def TreeviewUpdate(self):
		if databases != []:
			id = str(len(databases))
			self.tree.insert('', 'end', id, text=databases[-1].dbName)
			for value in databases[-1].tables:
				self.tree.insert(id, 'end', text=value)

	def changeTables(self, parent):
		parentIndex = self.getParent()[1]
		databases[parent].tables = []
		
		databases[parent].cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
		rows = databases[parent].cur.fetchall()
		if rows != []:
			for row in rows:
				databases[parent].tables.append(row[1])
		
		self.tree.delete(parentIndex)
		self.tree.insert('', 'end', parentIndex, text=databases[parent].dbName)
		for value in databases[parent].tables:
			self.tree.insert(parentIndex, 'end', text=value)
		
	def LoadDB(self, Type):
		Type = Type
		connect = False
		if Type == 'load':
			filename = tkFileDialog.askopenfilename()
		elif Type == 'create':
			filename = tkFileDialog.asksaveasfilename()
		try:
			con = sqlite.connect(filename)
			cur = con.cursor()
			cur.execute('SELECT * FROM sqlite_master')
			con.close()
			connect = True
			if len(filename) == 0:
				connect = False
		except:
			try:
				tkMessageBox.showwarning("Can't open file","%s is not a supported database file" % filename)	#Warnings will be moved to error function
				error('error','not a database',1)
			except TypeError:
				pass
			except:
				error('error','could not display warning window',151)
		if connect == True:
			try:
				databases.append(database(filename))
				index = len(databases) -1

				databases[index].cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
				rows = databases[index].cur.fetchall()
				if rows != []:
					for row in rows:
						databases[index].tables.append(row[1])
			except:
				error('error','could not get tables from db',160)				
			self.TreeviewUpdate()
			
def error(x,y,z):
	if z > 150:
		log(x,y)

def log(x,y):
	Time = time.strftime("%Y-%m-%d %H:%M")
	log = (x,y)
	con = sqlite.connect('log.db')
	cur = con.cursor()
	try:																#This will be overlooked at a later stage, CREATE TABLE IF NOT EXISTS	
		cur.execute("CREATE TABLE Log(Id INTEGER primary key AUTOINCREMENT, Time NUMERIC, Error TEXT, Message TEXT)")
	except:
		pass
	cur.execute("INSERT INTO Log (Time,Error,Message) VALUES(strftime('%Y-%m-%d %H:%M','now'),?,?)", log)
	con.commit()
	cur.execute("SELECT * FROM Log")
	rows = cur.fetchall()
	print row[-1][0],row[-1][1],row[-1][2],row[-1][3]
	con.close()

def main():
	global ScreenW,ScreenH
	root = Tkinter.Tk()
	root.geometry(("%dx%d")%(ScreenW,ScreenH))
	MmntInterface(root)
	root.mainloop()
	for database in databases:
		database.con.commit()
		database.con.close()
		print 'closing', database.dbName
	return 0

if __name__ == '__main__':
	main()

