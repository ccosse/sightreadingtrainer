import java,os
from java import awt
from javax import swing
from javax.swing import JLabel,JPanel,JSlider,JScrollPane,JEditorPane,JScrollPane,ImageIcon,JComboBox
from java.awt import FlowLayout,BorderLayout,Dimension
from java.net import *
from java.io import File
from javax.imageio import ImageIO

DEBUG=True

class foo2(awt.event.ActionListener):
	def __init__(self,parent):
		self.parent=parent
		
	def actionPerformed(self,e):
		self.parent.cbCB(e)

class C5Panel(JPanel):
	def __init__(self,hostname):
		
		self.hostname=hostname
		
		JPanel.__init__(self,BorderLayout())
		self.cbActionListener=foo2(self)
		
		#imglist=os.listdir('./img')
		#try:imglist.remove('.svn')
		#except:pass
		imglist=['01-CircleOfFifths.gif','Fifths.png','circle-o-fifths.jpg','Circle_Of_Fifths.gif','Keywheel.gif','circle-of-fifths.gif','ColorFifths.jpg','cof.gif']
		
		self.cb=JComboBox(imglist,actionListener=self.cbActionListener)#
		#self.cb.addItemListener(self.cbCB)
		tb=JPanel()
		tb.setLayout(FlowLayout(FlowLayout.CENTER))
		tb.add(self.cb)
		self.add(tb,'Center')
		
		self.img=None
		if hostname[0:7]=='http://':
			self.img=ImageIO.read(URL(self.hostname+'/static/sightreadingtrainer/img/'+imglist[0]))
		else:
			self.img=ImageIO.read(File(self.hostname+'img/'+imglist[0]))
		
		icon=ImageIcon(self.img)
		self.label=JLabel(icon)
		self.add(self.label,'North')
	
	
	def cbCB(self,e):
		try:
			item=self.cb.getSelectedItem()
			if DEBUG:print item
			if self.hostname[0:7]=='http://':
				self.img=ImageIO.read(URL(self.hostname+'/static/sightreadingtrainer/img/'+item))
			else:
				self.img=ImageIO.read(File(self.hostname+'img/'+item))
			
			if DEBUG:print self.img
			icon=ImageIcon(self.img)
			self.label.setIcon(icon)
		except Exception,e:
			if DEBUG:print e
		
		
