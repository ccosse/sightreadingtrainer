import java,os
from java import awt
from javax import swing
from javax.swing import JLabel,JPanel,JSlider,JScrollPane,JEditorPane,JScrollPane,ImageIcon,JComboBox
from java.awt import FlowLayout,BorderLayout,Dimension

DEBUG=0

class DebugPanel(JPanel):
	def __init__(self):
		
		JPanel.__init__(self,BorderLayout())
		self.editor=JEditorPane()
		self.editor.setEditable(0)
		#self.editor.setContentType('text/html')
		self.editor.setContentType('text/plain')
		sp=JScrollPane(self.editor,
			JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
			JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED)
		self.add(sp,'Center')
		
		#html="<html><h1>Test</h1></html>"
		#self.editor.setText(html)
		self.lines='DEBUG OUTPUT:'
		self.editor.setText(self.lines)
		
	def append(self,line):
		try:
			self.lines="%s\n%s"%(self.lines,line)
			self.editor.setText(self.lines)
		except Exception,e:
			print e	
