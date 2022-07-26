12JUL22
-- LDPC Pooling (only one define with multiple streams)
-- Comma added after phase field in CCL file e.g. [phase = 0],
-- Internal memory allocation feature turned on in Gabriel
-- Internal memory location addedd to CCL file
-- RDSL and CCL file: for Rx BLP v9LDPCpool	
	--- data_cblk_list is an output stream from cb_segmentation that 
            is then the "info" input to the other two flows, instead of 
            blp_info being fed from top level to all three sub flows. 
            (Note: changes the broadast behavior of the two "info" streams)
-- HW Discovery XML and System Constraints XML also included for reference

Cirrus360 Internal note:
Generated using :
python3 Gabriel_Bipartite_v4.py ../test_regression/NRBLP_2cluster_Ringo_mp_superPE_poolv0/inputfiles_NRBLP_2cluster_Ringo_pool_intMem

Cirrus360 Confidential and Proprietary
