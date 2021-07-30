#==============================================================================
# Layer of Complex neurons class
#------------------------------------------------------------------------------
#
#    
#    
#
#    
#    
#
#------------------------------------------------------------------------------
from siqo_lib   import *
from neuron     import Neuron


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class Layer
#------------------------------------------------------------------------------
class Layer():

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name, pos, size):
        "Call constructor of Layer and initialise it with neurons"

        journal.I( '<Layer> {} constructor...'.format(name), 10 )
        
        self.name     = name      # unique name for layer in Your project
        self.pos      = pos       #layer's  position in network <0,n>
        self.neurons  = []        # list of neurons in this layer
        
        for i in range(size): 
            self.neurons.append( Neuron( 'Neuron {}-{}'.format(str(self.pos), str(i)) ) )

        journal.O( '<Layer> {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"
        
        for neuron in self.neurons: neuron.clear()

        journal.M( '<Layer> {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return layer's name"
        
        return self.name

    #--------------------------------------------------------------------------
    def getPosition(self):
        "Return layer's position in net"
        
        return self.pos

    #==========================================================================
    # 
    #--------------------------------------------------------------------------


    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for layer"
        
        json = {'name':self.name }
        
        journal.M( '<Layer> {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def print(self):
        "Print layer's properties"
        
        print( "<Layer> '{} consists of {} Neurons".format(self.name, len(self.neurons))   )
        for neuron in self.neurons: neuron.print()
        print( "-----------------------------------------------------------------------" )
        
#------------------------------------------------------------------------------
journal.M('Layer class ver 0.11')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
