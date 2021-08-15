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
    def __init__(self, name, lay, size, context, startPos, srcLayer):
        "Call constructor of Layer and initialise it with neurons"

        journal.I( '<Layer> {} constructor...'.format(name), 10 )
        
        self.name      = name      # unique name for layer in Your project
        self.lay       = lay       # layer's  position in network <0,n>
        self.neurons   = []        # list of neurons in this layer
        self.context   = context   # number of neuron's sources in prevoius layer for both sides
        self.startPos  = startPos  # starting position = position of first neuron in layer
        self.srcLayer  = srcLayer  # reference to source Layer for neurons activation
        
        journal.M( '<Layer> {} lay={}, size={}, context={}, startPos={}'.format(self.name, self.lay, size, self.context, self.startPos), 10 )

        #----------------------------------------------------------------------
        # Create list of neurons belong to this layer

        for pos in range(startPos, startPos+size): 
            self.neurons.append( Neuron( 'Neuron {}-{}'.format(str(self.lay), str(pos)), pos, context ) )

        #----------------------------------------------------------------------
        # Create joins between neurons and theirs sources

        if self.srcLayer != '_nil_':

            journal.I( '<Layer> {} creating sources...'.format(self.name), 10)
            i = 0
        
            #------------------------------------------------------------------
            # Prejdem vsetky neurony vo vrstve
            for tgtNeu in self.neurons:
                
                tgtPos = tgtNeu.getPos()
                journal.M( 'Targte neuron {} at {} sources...'.format(tgtNeu.getName(), tgtPos), 10)
                
                # Vytvorim context na obe strany
                for srcPos in range( tgtPos-context, tgtPos+context+1):
                
                    # Ak je to mozne, vytvorim vazbu tgt-src
                    srcNeu = self.srcLayer.getNeuron(srcPos)
                    tgtNeu.addSource(srcNeu)
                
                i += 1
                #--------------------------------------------------------------

            journal.O( '<Layer> {} sources for {} neurons created'.format(self.name, i), 10)
            
        else:
            journal.M( '<Layer> {} has no source Layer'.format(self.name), 10)

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

    #--------------------------------------------------------------------------
    def getContext(self):
        "Return value of context for this layer"
        
        return self.context

    #--------------------------------------------------------------------------
    def getNeuron(self, pos):
        "Return Layer's neuron at layPos"
        
        for neu in self.neurons:
            if neu.getPos() == pos: return neu

        journal.M( '<Layer> {} getNeuron error. Neuron at {} does not exist'.format(self.name, pos), 10)
        return '_nil_'

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
journal.M('Layer class ver 0.16')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
