"""
**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2014 Asymptopia Software

    License         :GPLv3

***********************************************************
"""
import java
from java.awt import Dimension,BorderLayout
from javax.swing import JApplet,JFrame,JMenuBar,Box,JOptionPane,ButtonGroup,JRadioButtonMenuItem
from javax.swing import JMenu,JMenuItem,JTabbedPane,JPanel,JRadioButton,JButton
from java.net import *

from orch import *
#from c5panel import *
from help import *
from debug import *
#from scan_pane import *
from help import *
from c5panel import *

import time,thread
DEBUG=False
class MFC(JApplet):
	def ViewCB(self,e):
		if e.getSource().getText()=='Keyboard':
			if e.getSource().getState():self.orch.boxes.add(self.orch.kbd)
			else:self.orch.boxes.remove(self.orch.kbd)
			self.repaint()
			return
		if e.getSource().getText()=='Guitar':
			if e.getSource().getState():self.orch.boxes.add(self.orch.gtr)
			else:self.orch.boxes.remove(self.orch.gtr)
			self.repaint()
			return
		if e.getSource().getText()=='Staff':
			if e.getSource().getState():self.orch.boxes.add(self.orch.tab_pane)
			else:self.orch.boxes.remove(self.orch.tab_pane)
			self.repaint()
			return
		if e.getSource().getText()=='LargeGtrSpots':
			if e.getSource().getState():self.orch.gtr.LARGE_SPOTS=True
			else:self.orch.gtr.LARGE_SPOTS=False
			self.repaint()
			return
		

	def __init__(self):
		
		content = self.getContentPane()

		menubar=JMenuBar()
		filemenu=JMenu('File')
		filemenu.add(JMenuItem('Save',actionPerformed=self.saveCB))
#		filemenu.add(JMenuItem('Exit',actionPerformed=self.OnClose))
		menubar.add(filemenu)

		viewmenu=JMenu('View')
		self.view_menu_items=[
			JCheckBoxMenuItem('Guitar',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('Keyboard',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('Staff',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('LargeGtrSpots',False,actionPerformed=self.ViewCB),
	   	]
		for vidx in range(len(self.view_menu_items)):
			viewmenu.add(self.view_menu_items[vidx])
		
		#don't want this reset upon reconfigure:
		#viewmenu.add(JCheckBoxMenuItem('StaffConfigToolbar',False,actionPerformed=self.ViewCB))
		
		#
		menubar.add(viewmenu)
		tab_pane=JTabbedPane()

		self.debug_panel=None
		if DEBUG:self.debug_panel=DebugPanel()
		
		orch=Orch("http://www.asymptopia.org",1200,700,self)
		self.orch=orch

		self.c5panel=C5Panel(orch.hostname)
		self.help_panel=HelpPanel()

		tab_pane.addTab('Orch',None,orch)
		tab_pane.addTab('CircleOfFifths',None,self.c5panel)
		tab_pane.addTab('Help',None,self.help_panel)
		if DEBUG:tab_pane.addTab('Debug',None,self.debug_panel)
		
		mainpanel=JPanel(BorderLayout())
		mainpanel.setDoubleBuffered(True)
		mainpanel.add(menubar,'North')
		mainpanel.add(tab_pane,'Center')
		

#		mainpanel=JPanel(BorderLayout())
		self.add(mainpanel)
		
	def saveCB(self,e):
		pass

class MFCApp(JFrame):
	def ViewCB(self,e):
		if e.getSource().getText()=='Keyboard':
			if e.getSource().getState():self.orch.boxes.add(self.orch.kbd)
			else:self.orch.boxes.remove(self.orch.kbd)
			self.repaint()
			return
		if e.getSource().getText()=='Guitar':
			if e.getSource().getState():self.orch.boxes.add(self.orch.gtr)
			else:self.orch.boxes.remove(self.orch.gtr)
			self.repaint()
			return
		if e.getSource().getText()=='Staff':
			if e.getSource().getState():self.orch.boxes.add(self.orch.tab_pane)
			else:self.orch.boxes.remove(self.orch.tab_pane)
			self.repaint()
			return
		if e.getSource().getText()=='LargeGtrSpots':
			if e.getSource().getState():self.orch.gtr.LARGE_SPOTS=True
			else:self.orch.gtr.LARGE_SPOTS=False
			self.repaint()
			return
		
	def __init__(self):
		
		JFrame.__init__(self,'MFC',visible=0)
		self.setEnabled(True)
		self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		menubar=JMenuBar()
		filemenu=JMenu('File')
#		filemenu.add(JMenuItem('Save',actionPerformed=self.saveCB))
		filemenu.add(JMenuItem('Exit',actionPerformed=self.OnClose))
		menubar.add(filemenu)

		viewmenu=JMenu('View')
		self.view_menu_items=[
			JCheckBoxMenuItem('Guitar',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('Keyboard',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('Staff',True,actionPerformed=self.ViewCB),
	   		JCheckBoxMenuItem('LargeGtrSpots',False,actionPerformed=self.ViewCB),
	   	]
		for vidx in range(len(self.view_menu_items)):
			viewmenu.add(self.view_menu_items[vidx])
		
		#don't want this reset upon reconfigure:
		#viewmenu.add(JCheckBoxMenuItem('StaffConfigToolbar',False,actionPerformed=self.ViewCB))
		
		#
		menubar.add(viewmenu)
		
		tab_pane=JTabbedPane()
		
		self.debug_panel=None
		if DEBUG:self.debug_panel=DebugPanel()

		
#		orch=Orch("http://new.asymptopia.org/",1200,800,self)
		orch=Orch("./",1200,800,self)
		self.orch=orch
		tab_pane.addTab('Orch',None,orch)

		self.c5panel=C5Panel(orch.hostname)
		self.help_panel=HelpPanel()

		tab_pane.addTab('CircleOfFifths',None,self.c5panel)
		tab_pane.addTab('Help',None,self.help_panel)
#		tab_pane.addTab('Debug',None,self.debug_panel)
		
		mainpanel=JPanel(BorderLayout())
		mainpanel.setDoubleBuffered(True)
		mainpanel.add(menubar,'North')
		mainpanel.add(tab_pane,'Center')
		

#		mainpanel=JPanel(BorderLayout())
		self.add(mainpanel)
		
		
		self.setSize(1200,750)
		self.setVisible(1)
	
	def OnClose(self,e):
		#print 'OnClose'
		sys.exit()
		
if __name__=='__main__':
	  x=MFCApp()
