import numpy as np
import math as math

#calulate time in grid periods to move data across ther DDR
#in Kalray MPPA. x in B and output in ns
def DDRtoL2_datamove(x,gp):
    return int(np.ceil((0.068051*x+1015.8)/gp))
    
#calulate time in grid periods to move data across the DDR
#in Kalray MPPA. x in KB and output in ns
def L2toDDR_datamove(x,gp):
    return int(np.ceil((0.068051*x+1015.8)/gp))

#calulate time in grid periods to move data across the
#L2 to L2 interface 
#in Kalray MPPA. x in KB and output in ns
#DEFINED TO BE 1/10th OF DDR WITH SAME SET UP FOR NOW
def L2toL2_datamove(x,gp):
    return int(np.ceil((0.0626*x+213.5)/gp))
    
#calulate time in grid periods to prefetch a buffer of size x Bytes
def DDRtoL3_prefetch(x,gp):
    return int(np.ceil((355+math.ceil(9*x))/gp))

#calulate time in grid periods to flush a buffer of size x Bytes
def L3toDDR_flush(x,gp):
    return int(np.ceil((355+math.ceil(9*x))/gp))
    #return int(0) #assume the cache makes this irrelevant for now

#calulate the time in grid periods to move data from L3 to L2
#for a buffer of size x Bytes
def L3toL2_datamove(x,gp):
    return int(np.ceil(x/(gp)))

#calulate the time in grid periods to move data from L2 to L3
#for a buffer of size x Bytes
def L2toL3_datamove(x,gp):
    return int(np.ceil(x/(gp)))
    #return int(0) #assume cache coherence makes thus irrelevant for now

#calulate the time in grid periods to move data from L2 to L3
#for a buffer of size x Bytes
def PCIx_datamove(x,gp):
    return int(np.ceil((355+math.ceil(9*x))/gp)) #10x DDR to L3 for now
