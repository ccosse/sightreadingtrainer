import java,javax
from java import awt
from java.awt import *
from javax import swing
from javax.swing import *
import math,random,thread,time

from mfcinstrument import *
DEBUG=0

class PopupActionListener(awt.event.ActionListener):
	def __init__(self,parent,callback):
		self.callback=callback
		self.parent=parent
	
	def actionPerformed(self,e):
		if DEBUG:print 'actionPerformed'
		print e.getSource().getText()
		self.callback(e)	

class Staff(MFCInstrument,JPanel,awt.event.KeyListener,javax.swing.event.ChangeListener,java.awt.event.ActionListener):
	
	def __init__(self,orch,hostname,W,resolution,nbars,barwidth):
		
		MFCInstrument.__init__(self,'Staff',hostname,[Color.ORANGE])
		self.setLayout(BorderLayout())
		
		self.RUNNING=False
		self.orch=orch
		self.debug_panel=self.orch.debug_panel
		self.W=W
		self.H=320
		self.resolution=resolution
		self.nbars=nbars
		self.barwidth=barwidth
		
		self.char_width=10#in place of spot width?
		self.staff_width_for_centering=self.nbars*(4*resolution+1)*self.char_width*3
		self.debug_panel.append("self.staff_width_for_centering: "+`self.staff_width_for_centering`)
		
		self.xplay=int(self.W/2)
		self.debug_panel.append("self.xplay: "+`self.xplay`)
		
		self.dxdt=-20
		self.dt=0

		framesizeY=awt.Dimension(0,self.H)
		vfill=Box.Filler(framesizeY,framesizeY,framesizeY)
		self.add(vfill,'West')
		
		self.cp=JPanel()
		self.cp.setLayout(FlowLayout())
		self.cp.add(JCheckBox('Active',self.ACTIVE,actionPerformed=self.activeCB))
		self.cp.add(JButton('Scroll',actionPerformed=self.runCB))
		
		self.dxdtSlider=JSlider(-100,0,self.dxdt)
		self.dxdtSlider.addChangeListener(self)
		self.cp.add(self.dxdtSlider)
		
		self.rate=10
		self.rateSlider=JSlider(9,30,self.rate)
		self.rateSlider.addChangeListener(self)
		self.cp.add(self.rateSlider)

		self.cb=JComboBox(self.instlist,actionListener=self)
		self.cp.add(self.cb)

		greenLine=BorderFactory.createLineBorder(java.awt.Color(0,200,0))
		border=BorderFactory.createTitledBorder(greenLine,'Staff')
		self.cp.setBorder(border)
		self.add(self.cp,'South')
		self.hilighted=[]
		
	def actionPerformed(self,e):
		self.instrumentCB(e)
			
	def paintComponent(self,g):
		g.setColor(awt.Color.WHITE)
		#g.fillRect(self.W/2-50,self.H/2-15+100,100,120)
		g.fillRect(0,0,self.W,self.H)
		g.setColor(awt.Color.BLACK)
		
		#since drawing staff/tab lines between moving notes 
		#need to keep running index per string of current
		#xprogress/staff_length_for_centering
		x0=self.W/2-self.staff_width_for_centering/2
		xmax=self.W/2+self.staff_width_for_centering/2
		xprogress=[x0,x0,x0,x0,x0,x0]
		
		#loop over all notes and give them chance to fill-up staff/tab
		for idx in range(len(self.hilighted)):
			
			for sidx in range(6):
				if self.hilighted[idx]['sidx']==sidx:
					y1=self.H/2-30+10*sidx
					g.drawLine(int(xprogress[sidx]),y1,int(self.hilighted[idx]['xscroll']),y1)
					g.drawChars(
						`self.hilighted[idx]['fretnum']`,0,
						len(`self.hilighted[idx]['fretnum']`),
						int(self.hilighted[idx]['xscroll']),
						self.H/2-25+10*sidx
					)#NOTE: 25 centers char on staff lines
					
					if self.hilighted[idx]['fretnum']>9:xprogress[sidx]=int(self.hilighted[idx]['xscroll'])+20.
					else:xprogress[sidx]=int(self.hilighted[idx]['xscroll'])+10.
					
					self.hilighted[idx]['xscroll']+=self.dxdt*self.dt
					
		#don't want to pop while looping (ie above)
		for idx in range(len(self.hilighted)):
			if self.hilighted[idx]['xscroll']<x0:
				popped_note=self.hilighted.pop(idx)
				if DEBUG:self.debug_panel.append(`popped_note`)
				break#idx max just changed.
		
		for idx in range(len(self.hilighted)):
			if self.hilighted[idx]['played']==2:continue
			elif self.hilighted[idx]['played']==1:
				if time.time()-self.hilighted[idx]['toff']>0:
					#MIDI NOTE OFF:
					if self.keyboardChannel:
						self.keyboardChannel.noteOff(self.hilighted[idx]['midi'],80)
						self.hilighted[idx]['played']=2
					else:
						msg=ShortMessage()
						msg.setMessage(ShortMessage.NOTE_OFF,0,self.hilighted[idx]['midi'],80)
						self.rcv.send(msg,-1)
						self.hilighted[idx]['played']=2
					
				continue
			
			dx=self.hilighted[idx]['xscroll']-self.xplay
			#self.debug_panel.append(`dx`)
			if dx<10:
				if dx>0:
					self.debug_panel.append('PLAYING NOTE')
					self.cpCB(self.hilighted[idx])
					self.hilighted[idx]['played']=True
					
					#PLAY MIDI:
					if self.keyboardChannel:
						print 'play on channel',self.highlighted[idx]['fretnum']
						self.keyboardChannel.noteOn(self.hilighted[idx]['midi'],80)
						self.hilighted[idx]['played']=1
						self.hilighted[idx]['toff']=time.time()+1.
					else:
						msg=ShortMessage()
						msg.setMessage(ShortMessage.NOTE_ON,0,self.hilighted[idx]['midi'],80)
						self.rcv.send(msg,-1)
						self.hilighted[idx]['played']=1
						self.hilighted[idx]['toff']=time.time()+1.
					
		#fill the remainder of staff/tab lines
		for sidx in range(6):
			y1=self.H/2-30+10*sidx
			g.drawLine(min(int(xprogress[sidx]),xmax),y1,xmax,y1)
			
	def stateChanged(self,e):
		#print 'staff.stateChanged'
		#print e.getSource().getValue()
		if e.getSource()==self.dxdtSlider:
			self.dxdt=e.getSource().getValue()
		elif e.getSource()==self.rateSlider:
			self.rate=e.getSource().getValue()/10.
			if DEBUG:self.debug_panel.append(self.rate)
		else:
			print 'unknown src'
			
	def runThread(self,*args):
		if DEBUG:self.debug_panel.append('staff.runThread')
		if len(args)<1:return
		msg=args[0]
		
		t0=time.time()
		tlast=time.time()
		self.dt=0
		
		tnext=t0
		
		while self.RUNNING:
			
			#keep running for smoothe updateUI; schedule time for next note.
			t=time.time()
			
			if t>=tnext:
				
				note=self.orch.generate()
				note['xscroll']=self.W/2+self.staff_width_for_centering/2
				self.hilighted.append(note)
				
				msg="NewNote: %s%s, %s, %s"%(note['sidx']+1,note['fretnum'],note['notename'],note['midi'])
				self.debug_panel.append(msg)
				
				tnext=t+self.rate
				
			self.dt=t-tlast
			tlast=t
			self.updateUI()
			time.sleep(.1)
			
		if DEBUG:self.debug_panel.append("staff.runThread exited cleanly")
		
	def dxdtCB(self,e):
		print 'dxdtCB'
		
	def registerCB(self,cpCB):
		self.cpCB=cpCB

	def runCB(self,e):
		if DEBUG:self.debug_panel.append('staff.runCB')
		if self.RUNNING==True:
			self.RUNNING=False
		else:
			self.RUNNING=True
			thread.start_new_thread(self.runThread,("this is gonna be a keeper",))

		"""
		#from __init__ above:
		self.synth=MidiSystem.getSynthesizer()
		if not self.synth.isOpen():self.synth.open()
		self.rcv=self.synth.getReceiver()
		
		self.keyboardChannel=None#NEED:for app
		
		if hostname[0:7]=='http://':
			self.sb=MidiSystem.getSoundbank(URL(hostname+"soundbank-deluxe.gm"))
		else:
			self.sb=MidiSystem.getSoundbank(File(hostname+"soundbank.gm"))
			try:self.keyboardChannel=self.synth.getChannels()[0]
			except Exception,e:print e
		
		instruments=self.sb.getInstruments()
		#if DEBUG:print instruments
		instlist=[]
		for idx in range(len(instruments)):
			inst=instruments[idx]
			instlist.append(inst.getName())
		self.cb=JComboBox(instlist,actionListener=self)
		self.cp.add(self.cb)
		self.instruments=instruments
		self.instlist=instlist
		self.bank=self.instruments[0].getPatch().getBank()
		self.program=self.instruments[0].getPatch().getProgram()
		"""
