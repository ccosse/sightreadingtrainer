import java,javax
from java.net import *
from java import awt
from java.awt import FlowLayout,BorderLayout,Dimension
from javax import swing
from javax.swing import JButton,JLabel,JPanel,JSlider,JScrollPane,JEditorPane,JScrollPane,ImageIcon,Box,SwingConstants,JComboBox
from javax.sound.midi import *
from javax.imageio import *
from java.io import *
from javax.sound.midi import *

import time

from keyboard import *
from staff import *
from pyld import *

DEBUG=False

class foo(java.awt.event.ActionListener):
	def __init__(self,parent,callback):
		self.parent=parent
		self.callback=callback
		
	def actionPerformed(self,e):
		self.callback(e)



class MyMetaEventListener(javax.sound.midi.MetaEventListener):
	def __init__(self,parent,sequencer,keyboard):
		self.parent=parent
		self.sequencer=sequencer
		self.keyboard=keyboard
		
	def meta(self,meta):
		data=meta.getData()
		cmd=''
		for idx in range(len(data)):
			cmd+=chr(data[idx])
		#print cmd
		try:
			self.parent.frame.debug_panel.append('MyMetaEventListener:'+cmd)
			
			#exec(cmd)
			if cmd[0:3]=="ON:":
				MIDI=int(cmd[3:])
				self.parent.frame.debug_panel.append('->self.keyboard.midiOn('+`int(MIDI)`+')')
				self.keyboard.midiOn(MIDI)
				
			elif cmd[0:3]=="OFF":
				MIDI=int(cmd[4:])
				self.parent.frame.debug_panel.append('->self.keyboard.midiOff('+`int(MIDI)`+')')
				self.keyboard.midiOff(MIDI)
			else:
				self.parent.frame.debug_panel.append('MyMetaEventListener:'+cmd)
				
			self.parent.frame.debug_panel.append('MyMetaEventListener:'+'success')
			self.parent.frame.scan_pane.updateUI()
			pass
		except Exception,e:
			self.parent.frame.debug_panel.append('EXCEPTION@MyMetaEventListener')
			self.parent.frame.debug_panel.append(`e`)

class Orch(JPanel):
	def __init__(self,hostname,frame):
		self.hostname=hostname#for pyld
		self.frame=frame
		self.staff=None
		self.keyboard=None
		JPanel.__init__(self,BorderLayout())
				
		self.overlay_flags={
			'StaffLineNotes':False,
			'StaffSpaceNotes':False,
			'MajorScaleNotes':False,
			'MinorScaleNotes':False,
		}
		
		tb00=JPanel()
		tb00.setLayout(BorderLayout())
		
		tb01=JPanel()
		tb01.setLayout(FlowLayout(FlowLayout.CENTER))
		tb02=JPanel()
		tb02.setLayout(FlowLayout(FlowLayout.CENTER))
		
		self.synth=MidiSystem.getSynthesizer()
		self.synth.open()
		self.rcv=self.synth.getReceiver()
		
		if hostname[0:7]=='http://':
			self.sb=MidiSystem.getSoundbank(URL(hostname+"/static/MFC/soundbank-deluxe.gm"))
		else:
			self.sb=MidiSystem.getSoundbank(File(hostname+"/static/MFC/soundbank.gm"))
		
		self.sequencer=MidiSystem.getSequencer()
		self.sequencer.open()
		if DEBUG:print self.sequencer.getDeviceInfo()
		
		instruments=self.sb.getInstruments()
		instActionListener=foo(self,self.instrumentCB)
		#if DEBUG:print instruments
		instlist=[]
		for idx in range(len(instruments)):
			inst=instruments[idx]
			instlist.append(inst.getName())
		cb=JComboBox(instlist,actionListener=instActionListener)
		tb01.add(cb)
		self.instruments=instruments
		self.instlist=instlist
		
		self.bank=self.instruments[0].getPatch().getBank()
		self.program=self.instruments[0].getPatch().getProgram()
		
		resolution=1#spots-per-quarter-note
		num_bars=2
		barwidth=200
		W=800
		
		self.staff=Staff(self.frame,hostname,W,resolution,num_bars,barwidth)
		keysigActionListener=foo(self,self.SetKeySig)
		
		cb=JComboBox(self.staff.keysigs,actionListener=keysigActionListener)
		cb.setSelectedIndex(self.staff.sig_idx)
		tb01.add(cb)
		
		generateB=JButton('Generate', actionPerformed=self.generateCB)
		tb01.add(generateB)
		
		clearB=JButton('Clear', actionPerformed=self.clearCB)
		tb01.add(clearB)
		
		self.playB=JButton('Loop', actionPerformed=self.playCB)
		tb01.add(self.playB)
		
		self.tempo_slider=JSlider(SwingConstants.HORIZONTAL,1,20,10)
		self.tempo_slider.stateChanged=self.tempoCB
		tb01.add(self.tempo_slider)
		
		#TB02:
		self.timing_resolution_spinner=JSpinner(SpinnerNumberModel(resolution,1,25,1))
		#self.timing_resolution_spinner.addChangeListener(self.myListener)
		self.timing_resolution_spinner.setToolTipText('Timing resolution in spots per quarter note')
		tb02.add(self.timing_resolution_spinner)
		
		self.num_measures_spinner=JSpinner(SpinnerNumberModel(num_bars,1,8,1))
		#self.num_measures_spinner.addChangeListener(self.myListener)
		self.num_measures_spinner.setToolTipText('Number of measures this structure')
		tb02.add(self.num_measures_spinner)

		self.barwidth_spinner=JSpinner(SpinnerNumberModel(barwidth,100,400,10))
		#self.barwidth_spinner.addChangeListener(self.myListener)
		self.barwidth_spinner.setToolTipText('Pixel width occupied by 1 measure')
		tb02.add(self.barwidth_spinner)
		
		reconfigB=JButton('Reconfigure', actionPerformed=self.reconfigCB)
		reconfigB.setToolTipText('Rebuild the staff (all notes will be lost!)')
		tb02.add(reconfigB)


		tb00.add(tb01,'North')
		#tb02 not visible by default
		#tb00.add(tb02,'Center')
		self.add(tb00,'North')
		
		self.add(self.staff,'Center')
		
		USE_CHANNELS=False
		self.keyboardChannel=None
		if USE_CHANNELS:
			channels=self.synth.getChannels()
			self.keyboardChannel=self.synth.getChannels()[0]
		
		self.keyboard=Keyboard(W,200,self.keyboardChannel)
		self.add(self.keyboard,'South')
		
		#self.getFocusTraversalPolicy().getDefaultComponent(self.staff).requestFocus()
		self.mmel=MyMetaEventListener(self,self.sequencer,self.keyboard)
		self.sequencer.addMetaEventListener(self.mmel)
		
		self.SHOW_SCANLINE=False
		self.tb00=tb00
		self.tb01=tb01
		self.tb02=tb02
	
	def toggle_staff_config_toolbar(self):
		if self.tb00.getComponentCount()==1:
			self.tb00.add(self.tb02,'Center')
		else:
			self.tb00.remove(self.tb02)
		
	def reconfigCB(self,e):
		
		self.sequencer.removeMetaEventListener(self.mmel)
		
		resolution=self.timing_resolution_spinner.getValue()
		barwidth=self.barwidth_spinner.getValue()
		num_measures=self.num_measures_spinner.getValue()
		print resolution,barwidth,num_measures
		self.remove(self.staff)
		self.staff=Staff(self.hostname,self.getSize().width,resolution,num_measures,barwidth)
		self.add(self.staff,'Center')

		self.remove(self.keyboard)
		self.keyboard=Keyboard(self.getSize().width,200,self.keyboardChannel)
		self.add(self.keyboard,'South')

		self.mmel=MyMetaEventListener(self,self.sequencer,self.keyboard)
		self.sequencer.addMetaEventListener(self.mmel)
		
		#NEED:set all View menu items -> Off
		for item in self.frame.view_menu_items:
			item.setSelected(False)
		self.updateUI()
		
	def generateCB(self,e):
		pyld=Pyld(self.hostname)
		self.staff.take_pyld(pyld)
		self.updateUI()
		
	def clearCB(self,e):
		self.staff.clear()
		self.keyboard.allOff(e)
		self.updateUI()
	
	def update_overlays(self):
		if DEBUG:print 'Orchestrator.set_overlay: ',text
		#self.keyboard.set_overlay(text,state)
		
		self.setCursor(java.awt.Cursor(java.awt.Cursor.WAIT_CURSOR))
			
		for overlay_name in self.overlay_flags.keys():
			if self.overlay_flags[overlay_name]:
				
				#default colors in case key-change (necessary here and later, both)
				try:
					for midi in self.keyboard.overlays[overlay_name]:
						key=self.keyboard.getKeyByMidi(midi)
						if key['isBlack']:key['default_color']=java.awt.Color.BLACK
						else:key['default_color']=java.awt.Color.WHITE
						self.keyboard.midiOff(midi)
					self.keyboard.allOff()
					self.updateUI()
				except Exception,e:print e
						
				if False:pass
				elif overlay_name=='StaffLineNotes':
					midi_vals=[43,47,50,53,57,64,67,71,74,77]
					self.keyboard.overlays[overlay_name]=[]
					for midi_val in midi_vals:
						for xidx in range(1,self.staff.xoffset):
							for yidx in range(0,self.staff.H):
								spot=self.staff.FindSpotByIdx(xidx,yidx)
								if not spot:continue
								if spot.note['midi']==midi_val:
									if spot.note['sharp']:
										midi_val+=1
										break
									elif spot.note['flat']:
										midi_val-=1
										break
						self.keyboard.overlays[overlay_name].append(midi_val)
						key=self.keyboard.getKeyByMidi(midi_val)
						key['default_color']=java.awt.Color.PINK
						self.keyboard.midiOff(midi_val)
						
				elif overlay_name=='StaffSpaceNotes':
					midi_vals=[45,48,52,55,65,69,72,76]
					self.keyboard.overlays[overlay_name]=[]
					for midi_val in midi_vals:
						for xidx in range(1,self.staff.xoffset):
							for yidx in range(0,self.staff.H):
								spot=self.staff.FindSpotByIdx(xidx,yidx)
								if not spot:continue
								if spot.note['midi']==midi_val:
									if spot.note['sharp']:
										midi_val+=1
										break
									elif spot.note['flat']:
										midi_val-=1
										break
						
						self.keyboard.overlays[overlay_name].append(midi_val)
						key=self.keyboard.getKeyByMidi(midi_val)
						key['default_color']=java.awt.Color.CYAN
						self.keyboard.midiOff(midi_val)
						
				elif overlay_name=='MajorScaleNotes':
					
					print overlay_name,self.staff.sig_idx
					offsets=[-1,6,1,8,3,-2,5,0,7,2,9,4,-1,6,1]
					midi_root=60+offsets[self.staff.sig_idx]#C+/- sig_idx
					
					print 'midi_root',midi_root
					midi_val=midi_root
					self.keyboard.overlays[overlay_name]=[midi_val,]
					
					key=self.keyboard.getKeyByMidi(midi_val)
					key['default_color']=java.awt.Color.YELLOW
					self.keyboard.midiOff(midi_root)
					
					maj_scale_intervals=[2,2,1,2,2,2,1]
					for idx in range(len(maj_scale_intervals)):
						midi_val+=maj_scale_intervals[idx]
						self.keyboard.overlays[overlay_name].append(midi_val)
						key=self.keyboard.getKeyByMidi(midi_val)
						key['default_color']=java.awt.Color.YELLOW
						self.keyboard.midiOff(midi_val)
					print self.keyboard.overlays[overlay_name]
					
				elif overlay_name=='MinorScaleNotes':
					
					print overlay_name,self.staff.sig_idx
					offsets=[8,3,-2,5,0,7,2,-3,4,-1,6,1,8,3,-2]
					midi_root=60+offsets[self.staff.sig_idx]#C+/- sig_idx
					
					print 'midi_root',midi_root
					midi_val=midi_root
					self.keyboard.overlays[overlay_name]=[midi_val,]
					
					key=self.keyboard.getKeyByMidi(midi_val)
					key['default_color']=java.awt.Color.YELLOW
					self.keyboard.midiOff(midi_root)
					
					maj_scale_intervals=[2,1,2,2,1,2,2]
					for idx in range(len(maj_scale_intervals)):
						midi_val+=maj_scale_intervals[idx]
						self.keyboard.overlays[overlay_name].append(midi_val)
						key=self.keyboard.getKeyByMidi(midi_val)
						key['default_color']=java.awt.Color.YELLOW
						self.keyboard.midiOff(midi_val)
					print self.keyboard.overlays[overlay_name]
					
			else:
				
				try:
					for midi in self.keyboard.overlays[overlay_name]:
						key=self.keyboard.getKeyByMidi(midi)
						if key['isBlack']:
							key['default_color']=java.awt.Color.BLACK
						else:
							key['default_color']=java.awt.Color.WHITE
						self.keyboard.midiOff(midi)
						
				except Exception,e:
					print 'exception while resetting default colors:\n',e
				
				self.keyboard.overlays[overlay_name]=None
		
		self.updateUI()
		self.setCursor(java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR))
		
			
	def instrumentCB(self,e):
		if DEBUG:print 'instrumentCB'
		
		#name=self.cb.getSelectedItem()
		name=e.getSource().getSelectedItem()
		
		idx=self.instlist.index(name)
		if DEBUG:print 'loading: ',self.instruments[idx]
		self.synth.loadInstrument(self.instruments[idx])
		bank=self.instruments[idx].getPatch().getBank()
		program=self.instruments[idx].getPatch().getProgram()
		self.bank=bank
		self.program=program
		
		if self.keyboardChannel:
			c=self.synth.getChannels()
			cmc=c[0]
			cmc.programChange(bank,program)
			self.keyboardChannel.programChange(bank,program)
		
	def tempoCB(self,e):
		if DEBUG:print 'tempoCB',self.tempo_slider.getValue()
		self.sequencer.setTempoFactor(self.tempo_slider.getValue()/10.)
	
	def SetKeySig(self,e):
		self.setCursor(java.awt.Cursor(java.awt.Cursor.WAIT_CURSOR))
		self.staff.setKeySig(e.getSource().getSelectedItem())
		self.setCursor(java.awt.Cursor(java.awt.Cursor.DEFAULT_CURSOR))
		if not self.keyboard:return
		self.keyboard.allOff(None)
		self.updateUI()
		self.update_overlays()
		
	def paintComponent(self,g):
		if DEBUG:print 'orch.paintComponent'
	
	def playCB(self,e):
	
		if DEBUG:self.frame.debug_panel.append('playCB')
		
		if self.playB.getText()=='Loop':
			self.playB.setText('Stop')
		else:
			self.sequencer.stop()
			self.playB.setText('Loop')
			return
		
		try:
			LH=self.staff.GetLHNotes()
			if DEBUG:self.frame.debug_panel.append(`LH`)
			RH=self.staff.GetRHNotes()
			if DEBUG:self.frame.debug_panel.append(`RH`)

		except Exception,e:
			self.frame.debug_panel.append(`e`)
			return
			
		if DEBUG:print LH
		if DEBUG:print RH
		try:
			self.keyboard.allOff(e)
			self.updateUI()
		except:pass
		
		hands=[LH,RH]
		
		self.current_sequence=Sequence(Sequence.PPQ,4)
		self.current_track=self.current_sequence.createTrack()
		
		msg=ShortMessage()
		msg.setMessage(ShortMessage.PROGRAM_CHANGE,0,self.program,self.bank)
		event=MidiEvent(msg,0)
		self.current_track.add(event)
		
		if DEBUG:self.frame.debug_panel.append('building track ...')

		for hidx in range(len(hands)):
			hand=hands[hidx]
			for dmsg in hand:
				
				try:MIDI=int(dmsg['note'])
				except:continue#rest
				
				#NOTE,KEY ON:
				if DEBUG:self.frame.debug_panel.append('NOTE_ON')
				msg=ShortMessage()
				msg.setMessage(ShortMessage.NOTE_ON,0,MIDI,100)
				self.current_track.add(MidiEvent(msg,dmsg['xidx']))
				
				MARKER=0x06
				cmd="self.keyboard.midiOn(%s)"%(MIDI)
				cmd="ON:%s"%MIDI
				if DEBUG:self.frame.debug_panel.append(cmd)
				metaMessage=MetaMessage()
				metaMessage.setMessage(MARKER,cmd,len(cmd))
				midiEvent=MidiEvent(metaMessage,dmsg['xidx'])
				self.current_track.add(midiEvent)
				
				#NOTE,KEY OFF:
				if DEBUG:self.frame.debug_panel.append('NOTE_OFF')
				msg=ShortMessage()
				msg.setMessage(ShortMessage.NOTE_OFF,0,MIDI,0)
				self.current_track.add(MidiEvent(msg,dmsg['xidx']+int(dmsg['duration'])))
				
				MARKER=0x06
				cmd="self.keyboard.midiOff(%s)"%(MIDI)
				cmd="OFF:%s"%MIDI
				if DEBUG:self.frame.debug_panel.append(cmd)
				metaMessage=MetaMessage()
				metaMessage.setMessage(MARKER,cmd,len(cmd))
				midiEvent=MidiEvent(metaMessage,dmsg['xidx']+int(dmsg['duration']))
				self.current_track.add(midiEvent)
		
		if DEBUG:self.frame.debug_panel.append('adding marker message ...')

		MARKER=0x06
		markerMessage='self.sequencer.setTickPosition(0)'
		metaMessage=MetaMessage()		
		metaMessage.setMessage(MARKER,markerMessage,len(markerMessage))
		
		xidx_last_spot=self.staff.xidx_last_spot()-self.staff.xoffset
		midiEvent=MidiEvent(metaMessage,xidx_last_spot)#self.track_length_spinner.getValue()
		#self.current_track.add(midiEvent)
		
		if DEBUG:self.frame.debug_panel.append('setting sequence ...')
		self.sequencer.setSequence(self.current_sequence)
		
		if DEBUG:self.frame.debug_panel.append('setting LoopStartPoint ...')
		self.sequencer.setLoopStartPoint(0)
		self.sequencer.setLoopEndPoint(-1)
		self.sequencer.setLoopCount(Sequencer.LOOP_CONTINUOUSLY)
		
		if DEBUG:self.frame.debug_panel.append('starting sequencer ...')
		self.sequencer.start()
		if self.SHOW_SCANLINE:
			self.frame.RunScan(time.time(),self.sequencer.getMicrosecondLength()/self.sequencer.getTempoFactor(),self.staff.scan_xmin,self.staff.scan_xmax,self.staff.scan_ymin,self.staff.scan_ymax)
		
		
		
