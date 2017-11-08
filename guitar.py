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
import math,random

from mfcinstrument import *
DEBUG=False
class Guitar(MFCInstrument,java.awt.event.ActionListener,JPanel):
	def __init__(self,orch,hostname,W,H,x_pad,y_pad,W_bridge,W_nut,L0,SF):
		MFCInstrument.__init__(self,'Guitar',hostname,[Color.BLUE],False)
		
		self.channelNo=1
		
		self.orch=orch
		if DEBUG:self.debug_panel=self.orch.debug_panel
		
		self.setLayout(BorderLayout())
		
		self.cp=JPanel()
		self.cp.setLayout(FlowLayout())
		self.cp.add(JCheckBox('Active',self.ACTIVE,actionPerformed=self.activeCB))
		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,'Guitar')
		self.cp.setBorder(border)
		#self.add(self.cp,'South')
		
#		self.cb=JComboBox(self.instlist,actionListener=self)
#		self.cp.add(self.cb)

		#framesizeY=awt.Dimension(0,H)
		#vfill=Box.Filler(framesizeY,framesizeY,framesizeY)
		#self.add(vfill,'West')
				
		if DEBUG:print 'Guitar'
		self.SHOW_GUITAR=True
		self.LARGE_SPOTS=False
		
		self.x_pad=x_pad
		self.y_pad=y_pad
		self.W=W
		self.H=H
		self.W_bridge=W_bridge
		self.W_nut=W_nut
		self.L0=L0
		self.k=k=pow(2.,1./12.)
		
		self.SF=SF
		
		self.open_freqs=[659.25,587.33,493.86,392.0,220.0,164.81]
		self.open_midis=[76,71,67,62,57,52]
		self.open_names=['E','B','G','D','A','E']
		self.open_octaves=[5,4,4,4,3,3]
		self.strings=[]
		
		dy=self.W_bridge-self.W_nut
		
		self.octave_notes=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
		oidx_max=len(self.octave_notes)
		
		for sidx in range(len(self.open_freqs)):
			f0=self.open_freqs[sidx]
			string=[]
			
			oidx=self.octave_notes.index(self.open_names[sidx])
			octave=self.open_octaves[sidx]
			
			for fidx in range(24):
				
				notename=self.octave_notes[oidx]
				oidx+=1
				if oidx>=oidx_max:
					oidx=0
					octave+=1
					
				L_prev=self.L0*(1.-1./pow(k,fidx-1))
				L=self.L0*(1.-1./pow(k,fidx))
				
				y0=dy/2*(1.-L/L0)
				y1=self.W_bridge-dy/2*(1.-L/L0)
				
				fret={
					'x0':int(self.SF*L),
					'y0':int(self.SF*y0),
					'x1':int(self.SF*L),
					'y1':int(self.SF*y1),
					'xc':int((self.SF*L_prev+self.SF*L)/2.),
					'yc':int(self.SF*(y0+.15+(y1-y0-.25)*float(sidx)/5.)),
					'freq':f0*math.pow(k,fidx),
					'fretnum':fidx,
					'sidx':sidx,
					'notename':notename,
					'octave':octave,
					'midi':self.open_midis[sidx]+fidx,
					'xscroll':0.0,
					'played':False,
					'toff':0.
				}
				#if sidx==1:print fret['x0'],fret['y0'],fret['y1']
				string.append(fret)
			self.strings.append(string)
		
		self.tlcx=int((self.W+2*self.x_pad-self.strings[0][len(self.strings[0])-1]['x0'])/2.)
		self.tlcy=0#self.y_pad
		
		self.fretboard=awt.Polygon()
		self.fretboard.addPoint(self.tlcx,self.tlcy+self.strings[0][0]['y0'])
		self.fretboard.addPoint(self.tlcx+self.strings[0][22]['x0'],self.tlcy+self.strings[0][22]['y0'])
		self.fretboard.addPoint(self.tlcx+self.strings[0][22]['x0'],self.tlcy+self.strings[0][22]['y1'])
		self.fretboard.addPoint(self.tlcx,self.tlcy+self.strings[0][0]['y1'])
		self.fretboard.addPoint(self.tlcx,self.tlcy+self.strings[0][0]['y0'])
		
		self.dot_frets=[0,3,5,7,9,12,15,17,19,21]
		
		self.mousePressed=self.pressCB
		self.hilighted=[]
	
		
	def actionPerformed(self,e):
		self.instrumentCB(e)

	def pressCB(self,e):
		
		#mouse_position=self.getMousePosition()
		mouse_position=java.awt.Point(e.getX(),e.getY())
		
		mx=mouse_position.x
		my=mouse_position.y
		
		fret=self.getNote(mx,my)

		if not fret:return
		if DEBUG:print fret['notename'],fret['octave']
		
		self.clear_hilighted()
		while len(self.hilighted):
			self.hilighted.pop()
			
		self.hilighted.append(fret)
		
		#PLAY MIDI ON GTR CHANNEL w/GTR INSTRUMENT:
		self.orch.send(fret['midi'],-1)
		"""
		if self.keyboardChannel==None:
			msg=ShortMessage()
			msg.setMessage(ShortMessage.NOTE_ON,self.channelNo,fret['midi'],80)
			self.orch.send(msg,-1)
		else:
			self.keyboardChannel.noteOn(fret['midi'],80)
		"""
		
#		if DEBUG:self.debug_panel.append("gtr -> cpCB")
		self.cpCB(fret['midi'])
#		if DEBUG:self.debug_panel.append("gtr -> updateUI")
		self.updateUI()
		
	def getNote(self,xc,yc):
		for string in self.strings:
			for fret in string:
				if math.sqrt(math.pow(self.tlcx+fret['xc']-xc,2)+math.pow(self.tlcy+fret['yc']-yc,2)) < 10.:
					return fret
				
		return None
		
	def randNote(self):
		sidx=int(random.random()*6)
		fidx=int(random.random()*23)
		if DEBUG:print 'gtr.randNote: ',sidx,fidx
		return(sidx,fidx)
	
	
	def take_sfidx(self,sidx,fidx):
		self.hilighted.append(self.strings[sidx][fidx])
		self.updateUI()
		#print dir(self)
	
	def hilight_by_midi(self,midi):
		if DEBUG:print 'GTR: hilight_by_midi'
		for sidx in range(6):
			for fidx in range(len(self.strings[0])):
				if self.strings[sidx][fidx]['midi']==midi:
					self.hilighted.append(self.strings[sidx][fidx])
				
	def apply_dots(self,g):
		if DEBUG:print 'apply_dots'
		g.setColor(awt.Color.WHITE)	
		for dfidx in range(len(self.dot_frets)):
			fretnum=self.dot_frets[dfidx]
			xc=self.tlcx+self.strings[3][fretnum]['xc']
			yc=self.tlcy
			if fretnum==12 or fretnum==0:
				yc=int(self.tlcy+(self.strings[1][fretnum]['yc']+self.strings[2][fretnum]['yc'])/2.)
				g.fillOval(xc-4,yc-4,8,8)
				yc=int(self.tlcy+(self.strings[3][fretnum]['yc']+self.strings[4][fretnum]['yc'])/2.)
				g.fillOval(xc-4,yc-4,8,8)
					
			else:
				yc=int(self.tlcy+(self.strings[3][fretnum]['yc']+self.strings[2][fretnum]['yc'])/2.)
				g.fillOval(xc-4,yc-4,8,8)
		
		
		
	def paintComponent(self,g):
		
		if DEBUG:print 'GTR:paintComponent'
		
		if self.LARGE_SPOTS:dr2=9
		else:dr2=4#spot halfsize
		
		g.setColor(awt.Color.BLACK)
		g.fillPolygon(self.fretboard)
		self.apply_dots(g)
		
		g.setColor(awt.Color.GREEN)
		for fidx in range(22):
			x0=self.tlcx+self.strings[0][fidx]['x0']
			y0=self.tlcy+self.strings[0][fidx]['y0']
			x1=self.tlcx+self.strings[0][fidx]['x1']
			y1=self.tlcy+self.strings[0][fidx]['y1']
			g.drawLine(x0,y0,x1,y1)
		
		g.setColor(awt.Color.GRAY)
		for sidx in range(6):
			x0=self.tlcx+self.strings[sidx][0]['xc']
			y0=self.tlcy+self.strings[sidx][0]['yc']
			x1=self.tlcx+self.strings[sidx][23]['xc']
			y1=self.tlcy+self.strings[sidx][23]['yc']
			g.drawLine(x0,y0,x1,y1)
		
		"""
		g.setColor(awt.Color.GREEN)
		for sidx in range(6):
			for fidx in range(0,22):
				xc=self.tlcx+self.strings[sidx][fidx]['xc']
				yc=self.tlcy+self.strings[sidx][fidx]['yc']
				g.fillOval(xc-dr2,yc-dr2,2*dr2,2*dr2)
		"""
		
		g.setColor(awt.Color.RED)
		
		"""
		if not len(self.hilighted):
			sidx,fidx=self.randNote()
			self.take_sfidx(sidx,fidx)
		"""
		msg=""
		for idx in range(len(self.hilighted)):
			xc=self.tlcx+self.hilighted[idx]['xc']
			yc=self.tlcy+self.hilighted[idx]['yc']
			g.fillOval(xc-dr2,yc-dr2,2*dr2,2*dr2)
		
			msg="%s%d %d %d"%(self.hilighted[idx]['notename'],self.hilighted[idx]['octave'],self.hilighted[idx]['sidx']+1,self.hilighted[idx]['fretnum'])
			#print "%s%d"%(self.hilighted[idx]['notename'],self.hilighted[idx]['octave'])
			if DEBUG:print msg
		
		g.setColor(awt.Color.WHITE)
		g.fillRect(self.W/2-50,int(self.W_bridge*self.SF),100,20)
		g.setColor(awt.Color.BLACK)
		g.drawChars(msg,0,len(msg),self.W/2-50,int(self.W_bridge*self.SF)+11)#11=offset to align inside label
		#print dir(g)
		
		
if __name__=='__main__':
	x=Guitar()
