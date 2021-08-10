#==============================================================================
# Complex perceptron class
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
#from neuron     import Neuron
from layer      import Layer


#==============================================================================
# package's constants
#------------------------------------------------------------------------------


#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#==============================================================================
# class ComTron
#------------------------------------------------------------------------------
class ComTron():

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, name):
        "Call constructor of ComTron and initialise it"

        journal.I( '<ComTron> {} constructor...'.format(name), 10 )
        
        self.name     = name   # unique name for ComTron in Your project 
        self.inFile   = ''     # input   [ { 'in':'', 'tgt':int, 'dat':[ {'cat':int  } ]            } ]
        self.outFile  = ''     # output  [ { 'in':'', 'tgt':int, 'out':[ {'tgt':float} ], 'win':tgt } ]
        self.layers   = []     # network of neurons as a list of layers      


        journal.O( '<ComTron> {} created'.format(self.name), 10 )

    #--------------------------------------------------------------------------
    def clear(self):
        "Clear all data content and set default transformation parameters"

        self.inFile   = ''
        self.outFile  = ''
        
        for layer in self.layers: layer.clear()

        journal.M( '<ComTron> {} ALL cleared'.format(self.name), 10)
        
    #==========================================================================
    # Tools for selecting & editing
    #--------------------------------------------------------------------------
    def getName(self):
        "Return ComTron's name"
        
        return self.name

    #==========================================================================
    # Tools for net initialisation
    #--------------------------------------------------------------------------
    def createNet(self, layersSize ):
        "Create net as list of layers and resolve neuron connections"
        
        journal.I( '<ComTron> {} createNet...'.format(self.name), 10)
        
        pL = list(layersSize[0])
        pL.sort()
        maxSize = pL[-1]

        #----------------------------------------------------------------------
        # Create list of layers
        self.clear()
        
        lay = 0
        for size, joins in layersSize:
            self.layers.append( Layer( 'Layer {}'.format(str(lay)), lay, size, maxSize, joins ) )
            lay += 1

        #----------------------------------------------------------------------
        # Create joins between neurons
        

        #----------------------------------------------------------------------
        # Initialise weights and act
        self.annealing()

        journal.O( '<ComTron> {} created net of {} layers'.format(self.name, str(lay)), 10)

    #--------------------------------------------------------------------------
    def annealing(self):
        
        journal.I( '<ComTron> {} annealing'.format(self.name), 10)

        for lay in self.layers: lay.annealing()

        journal.O( '<ComTron> {} annealed'.format(self.name), 10)

    #--------------------------------------------------------------------------

    #==========================================================================
    # 
    #--------------------------------------------------------------------------


    #==========================================================================
    # Tools for data extraction & persistency
    #--------------------------------------------------------------------------
    def setIOFile(self, name):
        "Set name for Input/Output json file"
        
        self.inFile  = name+'.json'
        self.outFile = name+'_out.json'

        journal.M( '<ComTron> {} setIOFile to {} / {}'.format(self.name, self.inFile, self.outFile), 10)

    #--------------------------------------------------------------------------
    def getJson(self):
        "Create and return Json record for ComTron"
        
        json = {'name':self.name }
        
        journal.M( '<ComTron> {} getJson created'.format(self.name), 10)
        
        return json
        
    #--------------------------------------------------------------------------
    def getPlotData(self):
        "Create and return numpy arrays for plotting data"
        
        #----------------------------------------------------------------------
        # Metadata section
        meta = { 
                 'id'    :{'typ':'id'  ,'dim':'id'                           },
                 'lay'   :{'typ':'axe' ,'dim':'Lay' , 'unit':'Int', 'coeff':1, 'min':0, 'max':0 },
                 'pos'   :{'typ':'axe' ,'dim':'Pos' , 'unit':'Int', 'coeff':1, 'min':0, 'max':0 },
                 
                 'reAct' :{'typ':'dat' ,'dim':'Act' , 'unit':'Re' , 'coeff':1},
                 'imAct' :{'typ':'dat' ,'dim':'Act' , 'unit':'Im' , 'coeff':1},
                 'abAct' :{'typ':'dat' ,'dim':'Act' , 'unit':'Abs', 'coeff':1},

                 'reTgt' :{'typ':'dat' ,'dim':'Tgt' , 'unit':'Re' , 'coeff':1},
                 'imTgt' :{'typ':'dat' ,'dim':'Tgt' , 'unit':'Im' , 'coeff':1},
                 'abTgt' :{'typ':'dat' ,'dim':'Tgt' , 'unit':'Abs', 'coeff':1},
                 
                 'reErr' :{'typ':'dat' ,'dim':'Err' , 'unit':'Re' , 'coeff':1},
                 'imErr' :{'typ':'dat' ,'dim':'Err' , 'unit':'Im' , 'coeff':1},  
                 'abErr' :{'typ':'dat' ,'dim':'Err' , 'unit':'Abs', 'coeff':1},  
               }
        
        #----------------------------------------------------------------------
        # Data section
        data = { 'id'   :[], 'lay'  :[], 'pos'  :[],
                 'reAct':[], 'imAct':[], 'abAct':[],
                 'reTgt':[], 'imTgt':[], 'abTgt':[],
                 'reErr':[], 'imErr':[], 'abErr':[]  }
        
        toret = { 'meta':meta, 'data':data }
        
        i = 0
        for lay in self.layers:
            for neu in lay.neurons:
            
                toret['data']['id'   ].append( neu.getName()             )
                toret['data']['lay'  ].append( lay.getLayPos()           )
                toret['data']['pos'  ].append( neu.getPosition()         )
            
                toret['data']['reAct'].append( neu.getAct().real         )
                toret['data']['imAct'].append( neu.getAct().imag         )
                toret['data']['abAct'].append( abs(neu.getAct())         )

                toret['data']['reTgt'].append( neu.getTgt().real         )
                toret['data']['imTgt'].append( neu.getTgt().imag         )
                toret['data']['abTgt'].append( abs(neu.getTgt())         )

                toret['data']['reErr'].append( neu.getErr().real         )
                toret['data']['imErr'].append( neu.getErr().imag         )
                toret['data']['abErr'].append( abs(neu.getErr())         )

                i +=1
        
        #----------------------------------------------------------------------
        # Aggregation section
 
        for key, lst in toret['data'].items():
            
            # agregujem iba hodnoty pre osi
            if toret['meta'][key]['typ'] == 'axe':
            
                pL = list(lst)  # Urobim si kopiu listu na pokusy :-)
                pL.sort()
                
                toret['meta'][key]['min'] = pL[ 0]
                toret['meta'][key]['max'] = pL[-1]
        
        #----------------------------------------------------------------------
        journal.M( '<ComTron> {} getPlotData created {} records'.format(self.name, i), 10)
        return toret

    #--------------------------------------------------------------------------
    def print(self):
        "Print ComTron's properties"
        
        print( "<ComTron> {} consists of {} layers".format(self.name, len(self.layers) )   )
        print( "-----------------------------------------------------------------------" )
        for layer in self.layers: layer.print()
        print( "=======================================================================" )
        
#------------------------------------------------------------------------------
journal.M('ComTron class ver 0.13')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
