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
    ct = ComTron( 'test 10-3-1' )
    ct.createNet( [('IN',11), ('CLASS',3), ('OUT',1)] )
    ct.setIOFile( 'testfile' )
    
    # IN:  [ { 'in':'', 'dat':[], 'target':int } ]
    # OUT: [ { 'in':'', 'target':int, 'out':[{'target':float}], 'win':int } ]
 
    # Vytvorim GUI
 #   gui = ComTronGui(ct)
    
    
    
    journal.O('ComTron test 01 end')
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
