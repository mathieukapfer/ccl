04AUG22
-- Changes since 02AUG22
-- Updated timing as per included timings*.csv
-- Fixed issue with multiple internal memory offset defined per function
-- Changed cluster SMEM to 2MB
-- Phase 3.1 RDSL and CCL package for CV1 (SW LDPC in super PE)
-- Rx and Tx scheduled together. Two CCL files, one each for Rx and Tx
-- Both CCL can be run separately (for testing purposes) or together
-- LDPC Pooling for decoder (only one define with multiple streams)
-- LDPC encoding in same super PE
-- Internal memory allocation feature turned on in Gabriel
-- RDSL and CCL file: for Rx BLP v9LDPCpool	
-- HW Discovery XML, latency model (equations) and System Constraints XML also included for reference

Cirrus360 Internal note:
Generated using :
python3 Gabriel_Bipartite_v4.py ../test_regression/NRBLP_2cluster_Ringo_mp_superPE_poolv0/inputfiles_NRBLP_TxRx_2cluster_Ringo_pool_intMem_autogen_base

Cirrus360 Confidential and Proprietary
