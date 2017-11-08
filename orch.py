"""
**********************************************************

    Author          :Charles Brissac

    Email           :cdbrissac@gmail.com

    License         :GPLv3

***********************************************************
"""
import java,javax,javax.swing,java.awt
import java,javax
from java.net import *
from java import awt
from java.awt import FlowLayout,BorderLayout,Dimension
from javax import swing
from javax.swing import *

from javax.sound.midi import *
from javax.imageio import *
from java.io import *
from javax.sound.midi import *

import math,random,thread,time,sys,copy
from random import random

from keyboard import *
from guitar import *
from scroll_tab import *
from scroll_staff import *
from gstaff import *

DEBUG=False

class Orch(JPanel):
	def __init__(self,hostname,W,H,mfc):
		self.hostname=hostname
		self.mfc=mfc
		self.debug_panel=self.mfc.debug_panel
		self.scroll_staff=None

		self.setLayout(BorderLayout())

		boxes=JPanel()
		boxes.setLayout(BoxLayout(boxes,BoxLayout.Y_AXIS))

		x_pad=20
		y_pad=50
		W_nut=13./8.
		W_bridge=2.5
		L0=25.5
		self.SF=SF=50
		self.gtr=Guitar(self,hostname,W,int(SF/50.*H/3),x_pad,y_pad,W_bridge,W_nut,L0,SF)
		self.gtr.registerCB(self.gtrCB)

		SF=1.
		self.kbd=Keyboard(self,hostname,W,int(SF*H/6.),0,SF)
		self.kbd.registerCB(self.kbdCB)

		resolution=1#spots-per-quarter-note
		num_bars=2
		barwidth=200
		self.scroll_tab=ScrollTab(self,hostname,W,resolution,num_bars,barwidth)
		self.scroll_tab.registerCB(self.scroll_tabCB)

		self.scroll_staff=ScrollStaff(self,hostname,W,resolution,num_bars,barwidth)
		self.scroll_staff.registerCB(self.scroll_staffCB)

		#self.gstaff=GStaff(self,hostname,W,resolution,num_bars,barwidth)

		tab_pane=JTabbedPane()
		tab_pane.addTab('ScrollStaff',None,self.scroll_staff)
		tab_pane.addTab('ScrollTab',None,self.scroll_tab)
		#tab_pane.addTab('ScanStaff',None,self.gstaff)
		self.tab_pane=tab_pane

		boxes.add(self.gtr)
		boxes.add(self.tab_pane)
		boxes.add(self.kbd)
		self.add(boxes,'Center')
		self.boxes=boxes

		#self.add(self.cp,'South')

		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,self.name)
		self.setBorder(border)

	def generate(self,ntype,*args):

		#if args:print args
		if ntype=='Tab':
			sfidx=self.gtr.randNote()
			sidx=sfidx[0]
			fidx=sfidx[1]
			note=copy.copy(self.gtr.strings[sidx][fidx])
			return note
		elif ntype=='Staff':
			#sfidx=self.gtr.randNote()
			#sidx=sfidx[0]
			#fidx=sfidx[1]
			#note=self.gtr.strings[sidx][fidx]

			if not args:
				note=self.kbd.randNote()#returns 1 of 88 {key_dict}
			else:
				note=copy.copy(self.kbd.getKeyByMidi(args[0]))#returns specific {key_dict}

			#NEED: staff information; (sidx,fidx) -> midi -> kbd
			#staff.generate() -> staff/spots/midi -> kbd
			return note

		return None

	def send(self,midi,tstamp):
		if not self.scroll_staff:return
		self.scroll_staff.send(midi,tstamp)

	def sendOFF(self,midi,tstamp):
		if not self.scroll_staff:return
		self.scroll_staff.sendOFF(midi,tstamp)

	def scroll_staffCB(self,note):
		if DEBUG:print 'orch.scroll_staffCB'
		if self.kbd.ACTIVE:
			#self.kbd.allOff(None)
			if note:
				if DEBUG:print 'orch.scroll_staffCB calling keyboard.clear_hilighted'
				self.kbd.clear_hilighted()
				if DEBUG:print 'orch.scroll_staffCB calling keyboard.keyOn'
				self.kbd.keyOn(self.kbd.getKeyByMidi(note['midi']))
		if self.gtr.ACTIVE:
			self.gtr.clear_hilighted()
			if note:
				try:self.gtr.take_sfidx(note['sidx'],note['fretnum'])
				except Exception,e:pass
				#NEED: add sidx,fretnum to {note} ...
		self.updateUI()

	def scroll_tabCB(self,note):
		if DEBUG:print 'orch.scroll_tabCB'
		if self.kbd.ACTIVE:
			self.kbd.allOff(None)
			self.kbd.clear_hilighted()
			self.kbd.keyOn(self.kbd.getKeyByMidi(note['midi']))
		if self.gtr.ACTIVE:
			self.gtr.clear_hilighted()
			self.gtr.take_sfidx(note['sidx'],note['fretnum'])
		self.updateUI()

	def gtrCB(self,midi):
		if not self.kbd.ACTIVE:return
		if DEBUG:print 'orch.gtrCB'
		self.kbd.allOff(None)
		self.kbd.keyOn(self.kbd.getKeyByMidi(midi))
		self.updateUI()

	def kbdCB(self,midi):
		if not self.gtr.ACTIVE:return
		if DEBUG:print 'orch.kbdCB'
		self.gtr.clear_hilighted()
		self.gtr.hilight_by_midi(midi)
		self.updateUI()
