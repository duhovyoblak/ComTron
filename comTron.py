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

    #--------------------------------------------------------------------------
    def getLayer(self, layPos):
        "Return ComTron's Layer at layPos"
        
        try   : toret = self.layers[layPos]
        except: 
            toret = '_nil_'
            journal.M( '<ComTron> {} getLayer error. Layer at {} does not exist'.format(self.name, layPos), 10)
        
        return toret

    #--------------------------------------------------------------------------
    def getNeuron(self, layPos, pos):
        "Return ComTron's neuron at [layPos, pos]"
        
        layer = self.getLayer(layPos)
        
        if layer != '_nil': return layer.getNeuron(pos)
        else              : return '_nil_'

    #==========================================================================
    # Tools for net initialisation
    #--------------------------------------------------------------------------
    def createNet(self, topo ):
        "Create net as list of layers and resolve neuron connections"
        
        journal.I( '<ComTron> {} createNet...'.format(self.name), 10)
        self.clear()

        #----------------------------------------------------------------------
        # Create input layer   [('IN',8), ('CLASS',3), ('OUT',2)]
        
        lay  = 0
        size = topo[0][1]
        
        prevLayer = Layer( 'Input_{}'.format(str(lay)), lay, size )
        self.layers.append( prevLayer )
        lay += 1

        #----------------------------------------------------------------------
        # Create list of others layers

        for typ, context in topo[1:]:

            if   typ == 'CLASS': prevLayer = prevLayer.addClassLayer( 'CLASS_{}'.format(str(lay)), lay, context )
            elif typ == 'OUT'  : prevLayer = prevLayer.addOutLayer  (   'OUT_{}'.format(str(lay)), lay, context )
            
            self.layers.append( prevLayer )
            lay += 1

        journal.M( '<ComTron> {} {} layers created'.format(self.name, lay), 10)
        
        #----------------------------------------------------------------------
        # Initialise weights and act
        self.annealing()

        journal.O( '<ComTron> {} net created'.format(self.name), 10)

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
        meta = { 'points': {
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
                   'abErr' :{'typ':'dat' ,'dim':'Err' , 'unit':'Abs', 'coeff':1}
                           },
            
                 'arrows':  {}
               }
        
        #----------------------------------------------------------------------
        # Data section
        data = { 'points':{ 'id'   :[], 'lay'  :[], 'pos'  :[],
                            'reAct':[], 'imAct':[], 'abAct':[],
                            'reTgt':[], 'imTgt':[], 'abTgt':[],
                            'reErr':[], 'imErr':[], 'abErr':[]  
                          },
                 'arrows':{ 'shape':'right',
                            'color':'blue',
                            'width':1,
                            'data':{}
                          }
               }
        
        toret = { 'meta':meta, 'data':data }
        
        #----------------------------------------------------------------------
        # Create data
        
        pts = 0
        lns = 0
        for lay in self.layers:
            
            layPos = lay.getLayPos()
            
            for neu in lay.neurons:
            
                idt = neu.getName()
                pos = neu.getPos()

                # Points data for neuron
                toret['data']['points']['id'   ].append( idt                )
                toret['data']['points']['lay'  ].append( layPos             )
                toret['data']['points']['pos'  ].append( pos                )
            
                toret['data']['points']['reAct'].append( neu.getAct().real  )
                toret['data']['points']['imAct'].append( neu.getAct().imag  )
                toret['data']['points']['abAct'].append( abs(neu.getAct())  )

                toret['data']['points']['reTgt'].append( neu.getTgt().real  )
                toret['data']['points']['imTgt'].append( neu.getTgt().imag  )
                toret['data']['points']['abTgt'].append( abs(neu.getTgt())  )

                toret['data']['points']['reErr'].append( neu.getErr().real  )
                toret['data']['points']['imErr'].append( neu.getErr().imag  )
                toret['data']['points']['abErr'].append( abs(neu.getErr())  )

                pts +=1
                
                #Arrows data for target neuron
                arrs = []
 
                for src in neu.getSources():
                    
                    arrs.append({'x' :         src.getLayPos(), 'y' :      src.getPos(), 
                                 'dx':layPos - src.getLayPos(), 'dy':pos - src.getPos() })
                    lns +=1
                    
                # Ak existuju sipky, zapisem ich do dat
                if len(arrs) > 0:
                    
                    toret['data']['arrows']['data'][idt] = arrs

        # end create datapoints
        #----------------------------------------------------------------------

        journal.M( '<ComTron> {} getPlotData created {} points and {} lines'.format(self.name, pts, lns), 10)
        
        #----------------------------------------------------------------------
        # Aggregation section
 
        for key, lst in toret['data']['points'].items():
            
            # agregujem iba hodnoty pre osi
            if toret['meta']['points'][key]['typ'] == 'axe':
            
                pL = list(lst)  # Urobim si kopiu listu na pokusy :-)
                pL.sort()
                
                toret['meta']['points'][key]['min'] = pL[ 0]
                toret['meta']['points'][key]['max'] = pL[-1]

        journal.M( '<ComTron> {} getPlotData created aggregations for points'.format(self.name), 10)
        
        #----------------------------------------------------------------------
        journal.M( '<ComTron> {} getPlotData done'.format(self.name), 10)
        return toret

    #--------------------------------------------------------------------------
    def print(self):
        "Print ComTron's properties"
        
        print( "<ComTron> {} consists of {} layers".format(self.name, len(self.layers) )   )
        print( "-----------------------------------------------------------------------" )
        for layer in self.layers: layer.print()
        print( "=======================================================================" )
        
#------------------------------------------------------------------------------
journal.M('ComTron class ver 0.20')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
