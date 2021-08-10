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
from siqo_lib   import journal
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
    def __init__(self, name, lay, size, maxSize, joins):
        "Call constructor of Layer and initialise it with neurons"

        journal.I( '<Layer> {} constructor...'.format(name), 10 )
        
        self.name     = name      # unique name for layer in Your project
        self.lay      = lay       #layer's  position in network <0,n>
        self.neurons  = []        # list of neurons in this layer
        
        # Creating list of neurons
        startPos = int( (maxSize-size)/2 )
        
        journal.M( '<Layer> {} maxSize={}, size={}, startPos={}'.format(self.name, maxSize, size, startPos), 10 )

        for pos in range(startPos, startPos+size): 
            self.neurons.append( Neuron( 'Neuron {}-{}'.format(str(self.lay), str(pos)), pos ) )

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
    def getLayPos(self):
        "Return layer's position in net"
        
        return self.lay

    #==========================================================================
    # 
    #--------------------------------------------------------------------------
    def annealing(self):
        
        journal.I( '<Layer> {} annealing'.format(self.name), 10)

        for neu in self.neurons: neu.annealing()

        journal.O( '<Layer> {} annealed'.format(self.name), 10)


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
journal.M('Layer class ver 0.14')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
