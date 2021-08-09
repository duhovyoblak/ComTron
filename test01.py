#==============================================================================
# :ComTron test file
#------------------------------------------------------------------------------
from siqo_lib   import journal
#from neuron     import Neuron
#from layer      import Layer
from comTron    import ComTron
from comTronGui import ComTronGui

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# Functions
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ =='__main__':
  
    journal.I( 'ComTron test 01' )
    
    # Vytvorim testovaci ComTron
    ct = ComTron( 'test 5-8-2' )
    ct.createNet([5, 8, 2])
    ct.setIOFile( 'testfile' )
    
    # IN:  [ { 'in':'', 'dat':[], 'target':int } ]
    # OUT: [ { 'in':'', 'target':int, 'out':[{'target':float}], 'win':int } ]
 
    # Vytvorim GUI
    gui = ComTronGui(ct)
	
    
    
    
    journal.O('ComTron test 01 end')
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
