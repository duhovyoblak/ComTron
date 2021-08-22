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
    def __init__(self, name, lay, size, startPos=0):
        "Call constructor of Layer and initialise it with neurons"

        journal.I( '<Layer> {} constructor...'.format(name), 10 )
        
        self.name      = name     # unique name for layer in Your project
        self.lay       = lay      # layer's  position in net coordinates
        self.type      = 'IN'     # type of layer [IN, CLASS, OUT]
        self.neurons   = []       # list of neurons in this layer
        self.context   = 0        # number of neuron's sources in prevoius layer for both sides
        self.startPos  = startPos # starting position = position for first neuron in list
        self.srcLayer  = '_nil'   # reference to source Layer for neurons activation
        
        journal.M( '<Layer> {} lay={}, size={}, startPos={}'.format(self.name, self.lay, size, self.startPos), 10 )

        #----------------------------------------------------------------------
        # Create list of neurons belong to this layer

        for pos in range(startPos, startPos+size): 
            self.neurons.append( Neuron( 'Neuron {}-{}'.format(str(self.lay), str(pos)), lay, pos ) )

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
    # Creating new various type of layer's connections
    #--------------------------------------------------------------------------
    def addClassLayer(self, name, lay, context):
        "From source layer create classification layer and return it"
    
        journal.I( '<Layer> {} addClassLayer name={} for {} sources with context={}'.format(self.name, name, len(self.neurons), context), 10 )
        
        startPos = self.neurons[0].getPos()+context
        size     = len(self.neurons) - 2*context
        
        if size < 1:
            journal.O( '<Layer> {} addClassLayer failed, context={} is too big'.format(self.name, context), 10 )
            return '_nil_'
            
        #----------------------------------------------------------------------
        # Create new layer
        
        toret = Layer(name, lay, size, startPos )
        
        toret.type      = 'CLASS'
        toret.context   = context   # number of neuron's sources in prevoius layer for both sides
        toret.srcLayer  = self      # reference to source Layer for neurons activation
        
        #----------------------------------------------------------------------
        # Create joins between neurons and theirs sources

        journal.M( '<Layer> {} creating sources...'.format(toret.name), 10)
        
        #----------------------------------------------------------------------
        # Prejdem vsetky neurony vo vrstve
        for tgtNeu in toret.neurons:
                
            tgtPos = tgtNeu.getPos()
            journal.I( 'Target neuron {} at {} creating sources...'.format(tgtNeu.getName(), tgtPos), 10)
                
            i = 0
            # Vytvorim context na obe strany
            for srcPos in range( tgtPos-context, tgtPos+context+1):
                
                # Ak je to mozne, vytvorim vazbu tgt-src
                srcNeu = self.getNeuron(srcPos)
                tgtNeu.addSource(srcNeu)
                
                i += 1
            #--------------------------------------------------------------

            journal.O( 'Target neuron {} has {} sources'.format(toret.name, i), 10)
        #----------------------------------------------------------------------

        journal.O( '<Layer> {} created as type {}'.format(toret.name, toret.type), 10 )
        return toret
    
    #--------------------------------------------------------------------------
    def addOutLayer(self, name, lay, context):
        "From source layer create output layer and return it"
    
        journal.I( '<Layer> {} addOutLayer name={} with context={}'.format(self.name, name, context), 10 )
        
        #----------------------------------------------------------------------
        # Create output layer
        
        toret = self.addClassLayer(name, lay, context )
        toret.type      = 'OUT'

        journal.O( '<Layer> {} created as type {}'.format(toret.name, toret.type), 10 )
        return toret
    
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
        
        print( "<Layer> '{} type {} consists of {} Neurons".format(self.name, self.type, len(self.neurons))   )
        for neuron in self.neurons: neuron.print()
        print( "-----------------------------------------------------------------------" )
        
#------------------------------------------------------------------------------
journal.M('Layer class ver 0.17')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
