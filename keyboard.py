"""
**********************************************************

    Author          :Charles Brissac

    Email           :cdbrissac@gmail.com

    License         :GPLv3

***********************************************************
"""
import java
from javax.swing import *
from java import awt
from java.awt import *
import math,random,copy
from random import random
from mfcinstrument import *

DEBUG=False
class Keyboard(MFCInstrument,java.awt.event.ActionListener,JPanel):
	def __init__(self,orch,hostname,W,H,channel,SF):
		MFCInstrument.__init__(self,'Keyboard',hostname,[Color.GREEN],False)
		self.orch=orch
		self.debug_panel=self.orch.debug_panel
		self.hostname=hostname
		self.setLayout(BorderLayout())

		self.cp=JPanel()
		self.cp.setLayout(FlowLayout())
		self.cp.add(JCheckBox('Active',self.ACTIVE,actionPerformed=self.activeCB))
		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,'Keyboard')
		self.cp.setBorder(border)
		#self.add(self.cp,'South')

#		self.cb=JComboBox(self.instlist,actionListener=self)
#		self.cp.add(self.cb)

		self.W=W
		self.H=H
		self.channel=None
		if not channel:
			self.channelNo=2

		#self.setSize(W,H)
		#self.g=self.getGraphics()

		self.SHOW_KEYBOARD=True
		#self.setBackground(awt.Color.ORANGE)

		#framesizeY=awt.Dimension(0,H)
		#vfill=Box.Filler(framesizeY,framesizeY,framesizeY)
		#self.add(vfill,'West')

		#52 white notes, 36 black
		self.kw1=int(self.W*SF/52)
		self.kw=self.kw1*52
		self.kh=int(self.kw/9.15)

		self.tlcx=(self.W-self.kw)/2
		self.tlcy=0#(self.H-self.kh)/2

		self.lines=[]
		self.lines.append([self.tlcx,self.tlcy,self.tlcx+self.kw,self.tlcy])
		self.lines.append([self.tlcx+self.kw,self.tlcy,self.tlcx+self.kw,self.tlcy+self.kh])
		self.lines.append([self.tlcx+self.kw,self.tlcy+self.kh,self.tlcx,self.tlcy+self.kh])
		self.lines.append([self.tlcx,self.tlcy+self.kh,self.tlcx,self.tlcy])

		self.keys=[]
		self.kidxByMidi={}

		#B+W Keys:
		self.bw=int(self.kw1/2.2)
		self.bh=int(self.kh/1.7)

		count=10#A
		ws=[1,3,5,6,8,10,12]
		bx=[2,4,7,9,11]

		names=['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
		freq=27.5
		midi=21
		oidx=0
		nidx=11
		fact=pow(2.,1./12.)

		tlcx=self.tlcx
		for kidx in range(0,88):
			#if DEBUG:print kidx
			ktype=None
			if kidx==0:ktype='left'
			elif kidx==87:ktype='blank'
			elif count==1:ktype='left'
			elif count==2:ktype='black'
			elif count==3:ktype='center'
			elif count==4:ktype='black'
			elif count==5:ktype='right'
			elif count==6:ktype='left'
			elif count==7:ktype='black'
			elif count==8:ktype='center'
			elif count==9:ktype='black'
			elif count==10:ktype='center'
			elif count==11:ktype='black'
			elif count==12:ktype='right'

			if ktype=='left':dx=self.bw/2
			elif ktype=='center':dx=+self.bw/2
			elif ktype=='right':dx=+self.bw/2
			elif ktype=='black':dx=+self.bw/2
			elif ktype=='blank':dx=0

			if ktype=='black':
				default_color=awt.Color.BLACK
				isBlack=True
			else:
				default_color=awt.Color.WHITE
				isBlack=False
			kidx+=1

			nidx+=1
			if nidx>11:nidx=0
			if nidx==0:oidx+=1
			freq*=fact

			self.keys.append(
				{
					'polygon':self.mkKey(ktype,tlcx,dx),
					'ktype':ktype,
					'kidx':kidx,
					'isBlack':isBlack,
					'name':names[nidx],
					'octave':oidx,
					'midi':midi,
					'freq':freq,
					'default_color':default_color,
					'color':default_color,
					'hilight_color':awt.Color.ORANGE,
					#
					'y1':0,
					'played':0,
					'xscroll':0,
					'xplay':0,
					'ylist':None,
					'isaccidental':0,
					'sharp':0,
					'flat':0
				}
			)

			#if DEBUG:print 'kidx=',kidx,midi,names[nidx]

			self.kidxByMidi[`midi`]=len(self.keys)-1

			midi+=1
			count+=1
			if count>12:count=1

			if ws.count(count)>0 and kidx!=0:
				tlcx+=self.kw1

		"""
		self.synth=MidiSystem.getSynthesizer()
		if not self.synth.isOpen():self.synth.open()
		self.rcv=self.synth.getReceiver()

		#self.channel=self.synth.getChannels()[0]
		"""
		self.mousePressed=self.pressCB
		self.mouseReleased=self.releaseCB

		self.mouseMoved=self.moveCB
		self.last_key=None

		self.update_mode=0

		self.overlays={
			'StaffLineNotes':None,
			'StaffSpaceNotes':None,
			'MajorScaleNotes':None
		}

	def randNote(self):
		idx=int(random()*len(self.keys))
		return copy.copy(self.keys[idx])

	def actionPerformed(self,e):
		self.instrumentCB(e)

	def registerCB(self,cpCB):
		self.cpCB=cpCB

	def moveCB(self,e):
		return
		pass

		#Offer this via checkbox menu
		mouse_position=self.getMousePosition()
		for k in self.keys:
			if k['polygon'].contains(mouse_position):

				if k==self.last_key:return
				if self.last_key:
					self.keyOff(self.last_key)
					self.midiOff(self.last_key['midi'])

				self.last_key=k
				self.keyOn(k)
				if not self.channel:
					msg=ShortMessage()
					msg.setMessage(ShortMessage.NOTE_ON,self.channelNo,k['midi'],100)
					self.orch.send(msg,-1)
				else:
					self.channel.noteOn(k['midi'],100)

				self.updateUI()
				return

		if self.last_key:
			self.midiOff(self.last_key['midi'])
			self.keyOff(self.last_key)
			if self.channel:
				self.channel.allNotesOff()

	def getKeyByMousePosition(self,mouse_position):
		for k in self.keys:
			if k['polygon'].contains(mouse_position):return k
		return None


	def pressCB(self,e):
		try:

			self.allOff(None)#no painting; sets k['color']

			mouseX=e.getX()
			mouseY=e.getY()
			p=java.awt.Point(mouseX,mouseY)
			k=self.getKeyByMousePosition(p)
			if k:
				self.keyOn(k)
				#PLAY MIDI ON GTR CHANNEL w/GTR INSTRUMENT:
				self.orch.send(k['midi'],-1)
				self.cpCB(k['midi'])
				self.updateUI()
		except Exception,e:
			#self.debug_panel.append("Exception!")
			#self.debug_panel.append(`e`)
			pass

	def releaseCB(self,e):
		if DEBUG:print 'keyboard:releaseCB'
		self.allOff(None)
		mouseX=e.getX()
		mouseY=e.getY()
		p=java.awt.Point(mouseX,mouseY)
		k=self.getKeyByMousePosition(p)
		self.orch.sendOFF(k['midi'],-1)
		self.orch.updateUI()

	def hilight_by_midi(self,midi):
		if DEBUG:print 'keyboard: hilight_by_midi'
		self.keyOn(midi)


	def getKeyByMidi(self,midi):
		if DEBUG:print 'keyboard.getKeyByMidi'
		return self.keys[self.kidxByMidi[`midi`]]
		#for ptr in self.midi_ptrs:
		#	if k['midi']==midi:return k


	def keyOff(self,k):
		if not k:return
		if DEBUG:print 'keyboard.keyOff'
		k['color']=k['default_color']


	def allOn(self,e):
		for k in self.keys:
			k['color']=k['hilight_color']


	def allOff(self,e):
		if DEBUG:print 'keyboard.allOff'
		if self.channel:
			self.channel.allNotesOff()
		for k in self.keys:
			k['color']=k['default_color']
			#msg=ShortMessage()
			#msg.setMessage(ShortMessage.NOTE_OFF,self.channelNo,k['midi'],80)
			#self.orch.sendOFF(k['midi'],-1)

	def keyOn(self,k):
		if DEBUG:print 'keyboard.keyOn'
		#self.debug_panel.append(k['hilight_color'])
		k['color']=k['hilight_color']

	def midiOn(self,midi):
		if DEBUG:print 'keyboard:midiOn',midi
		#k=self.getKeyByMidi(midi)
		k=self.keys[self.kidxByMidi[`midi`]]
		k['color']=k['hilight_color']
		#msg=ShortMessage()
		#msg.setMessage(ShortMessage.NOTE_ON,self.channelNo,k['midi'],80)
		self.orch.send(k['midi'],-1)

	def midiOff(self,midi):
		print 'keyboard:midiOff',midi
		#k=self.getKeyByMidi(midi)
		k=self.keys[self.kidxByMidi[`midi`]]
		k['color']=k['default_color']

	def paintComponent(self,g):
		#return
		if DEBUG:print 'keyboard:paintComponent'

		#NEED: This needs to be ON (but only when NOT playCB, else slows scan_pane)
		self.update_mode=3
		#self.super__paintComponent(g)#passing THIS "g" is causing the staff-rendering-on-keyboard problem

		g.setColor(awt.Color(0,1,0,1))
		g.fillRect(0,0,self.getWidth(),self.getHeight())

		if not self.SHOW_KEYBOARD:return

		#self.g=g

		for line in self.lines:
		   g.drawLine(line[0],line[1],line[2],line[3])

		for k in self.keys:

			if k['color']==k['default_color']:pass
			g.setColor(k['color'])
			g.fillPolygon(k['polygon'])
			g.setColor(awt.Color.BLACK)
			g.drawPolygon(k['polygon'])#black outline

		#self.super_updateUI()
		#print dir(self)

	def mkKey(self,ktype,tlcx,dx):
		msg="(%d,%d,%d,%d)"%(tlcx,self.tlcy,tlcx+dx,self.tlcy+self.kh)
		#print msg
		#if DEBUG:self.debug_panel.append(msg)

		tlcy=self.tlcy
		kw1=self.kw1
		kh=self.kh
		bw=self.bw
		bh=self.bh

		p=awt.Polygon()
		if ktype!='black':#l/c/r
			if ktype=='left':
				p.addPoint(tlcx,tlcy)
				p.addPoint(tlcx+kw1-dx,tlcy)
				p.addPoint(tlcx+kw1-dx,tlcy+bh)
				p.addPoint(tlcx+kw1,tlcy+bh)
				p.addPoint(tlcx+kw1,tlcy+kh)
				p.addPoint(tlcx,tlcy+kh)
				p.addPoint(tlcx,tlcy)

			elif ktype=='right':
				p.addPoint(tlcx+dx,tlcy)
				p.addPoint(tlcx+kw1,tlcy)
				p.addPoint(tlcx+kw1,tlcy+kh)
				p.addPoint(tlcx,tlcy+kh)
				p.addPoint(tlcx,tlcy+bh)
				p.addPoint(tlcx+dx,tlcy+bh)
				p.addPoint(tlcx+dx,tlcy)

			elif ktype=='center':
				p.addPoint(tlcx+dx,tlcy)
				p.addPoint(tlcx+kw1-dx,tlcy)
				p.addPoint(tlcx+kw1-dx,tlcy+bh)
				p.addPoint(tlcx+kw1,tlcy+bh)
				p.addPoint(tlcx+kw1,tlcy+kh)
				p.addPoint(tlcx,tlcy+kh)
				p.addPoint(tlcx,tlcy+bh)
				p.addPoint(tlcx+dx,tlcy+bh)
				p.addPoint(tlcx+dx,tlcy)

			elif ktype=='blank':
				p.addPoint(tlcx,tlcy)
				p.addPoint(tlcx+kw1,tlcy)
				p.addPoint(tlcx+kw1,tlcy+kh)
				p.addPoint(tlcx,tlcy+kh)
				p.addPoint(tlcx,tlcy)

		else:
			p.addPoint(tlcx+kw1-dx,tlcy)
			p.addPoint(tlcx+kw1+dx,tlcy)
			p.addPoint(tlcx+kw1+dx,tlcy+bh)
			p.addPoint(tlcx+kw1-dx,tlcy+bh)
			p.addPoint(tlcx+kw1-dx,tlcy)

		return p
