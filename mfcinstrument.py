"""
**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2011 Asymptopia Software

    License         :GPLv3

***********************************************************
"""
import java,javax,javax.swing,java.awt
from java.awt import Color,BorderLayout,FlowLayout
from javax.swing import JPanel
from javax.swing import *
from javax.sound.midi import *
from javax.imageio import ImageIO
from java.io import *
from java.net import *

from java.io import File
from java.net import URL

DEBUG=False

class MFCInstrument:

	def __init__(self,name,hostname,hilight_colors,INITIALIZE_MIDI):
		
		self.name=name
		if DEBUG:print self.name
		
		self.hostname=hostname
			
		self.hilight_colors=hilight_colors
		self.hilighted=[]
		self.cpCB=None
		self.cp=None
		self.orch=None
		self.ACTIVE=True
		self.keyboardChannel=None
		
		#COMMON MIDI STUFF:
		if not INITIALIZE_MIDI:return
		self.synth=MidiSystem.getSynthesizer()
		if not self.synth.isOpen():self.synth.open()
		self.rcv=self.synth.getReceiver()
		
		self.keyboardChannel=None#NEED:for app
		self.channelNo=0
		
		if hostname[0:7]=='http://':
			#self.sb=MidiSystem.getSoundbank(URL(hostname+"/static/MFC/soundbank.gm"))
			self.sb=MidiSystem.getSoundbank(URL(hostname+"/static/MFC/soundbank-emg.sf2"))
		else:
			#self.sb=MidiSystem.getSoundbank(File(hostname+"soundbank.gm"))
			self.sb=MidiSystem.getSoundbank(File(hostname+"soundbank-emg.sf2"))
			try:self.keyboardChannel=self.synth.getChannels()[0]
			except Exception,e:print e
		
		instruments=self.sb.getInstruments()
		#if DEBUG:print instruments
		instlist=[]
		for idx in range(len(instruments)):
			inst=instruments[idx]
			instlist.append(inst.getName())

		self.instruments=instruments
		self.instlist=instlist
		self.bank=self.instruments[0].getPatch().getBank()
		self.program=self.instruments[0].getPatch().getProgram()

	def registerCB(self,cpCB):
		self.cpCB=cpCB;	
	
	def clear_hilighted(self):
		while len(self.hilighted):
			self.hilighted.pop()
	
	def activeCB(self,e):
		if DEBUG:print self.name,'activeCB'
		if self.ACTIVE:
			self.ACTIVE=False
			self.clear_hilighted()
			self.updateUI()
			#NEED:self.clear_hilighted() <-reqs kbd use hilighted[]
		else:
			self.ACTIVE=True

	def actionPerformed(self,e):
		self.instrumentCB(e)

	def instrumentCB(self,e):
		if DEBUG:print 'mfcinstrument.instrumentCB'
		
		#name=self.cb.getSelectedItem()
		name=e.getSource().getSelectedItem()
		
		idx=self.instlist.index(name)
		if DEBUG:print 'loading: ',self.instruments[idx]
		self.synth.loadInstrument(self.instruments[idx])
		bank=self.instruments[idx].getPatch().getBank()
		program=self.instruments[idx].getPatch().getProgram()
		self.bank=bank
		self.program=program
		
		#"""
		if self.keyboardChannel:
			c=self.synth.getChannels()
			cmc=c[0]
			cmc.programChange(bank,program)
			self.keyboardChannel.programChange(bank,program)
		#"""
		if DEBUG:print 'done.'
