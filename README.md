# Booster-optimization

0608 update, (1) added KBtry; (2)implement new variant update through SEIYAHRD; (3) update epi_params.py update variants

(1): KBtry is a toy file to illustrate how to general the new variant by random number (using seeds in the real codes) 

(2): Implement new variants updating SEIYAHRD:
(2.1): random generate the date of new variant, around line 350
(2.2): global the start time of variants & prev_matrix, make the time & prevlance updates are consistant in simulate_t and simulate_vaccine, around line 120
(2.3): read historical prev from csv, estimate the future prev using random walk
(2.4): parameter updates through new prev matrix, line 340, 350 & 360
(2.5): random generate the immune_escape rate for the potential new variant, line 533.

(3): Update parameters like beta, YHR...for delta, omicron & new_variant, line 140, 190, 240 in epi_params

Next update will do:
(1) comfrim beta update logic; 
(2) improve the random seeds generating method through rnd_stream & seed_read from data process folder;
(3) try using code to generate future booster allocation csv

#############################################

0728 update, uploading booster data & willingness folder
(1) extract & visualize CDC vaccine & booster data in County and State level
(2) Calculate the 1st and 2nd booster willingness in TX state based on these data

#############################################

0801 update, uploading the KB_write_seed.py

Currently, 100 files(for 100 scenarios) * 100 random number follow uniform distribution each file

Which could generate mutiple seed.p files, as the test set for different scnarios for the future variant

#############################################

0802 update, load random seed through args on SEIYARD success:

(1) instances\_init_.py, define a new load_seeds2 function, (maybe windows & apple system have different directory logic, load_seeds doesnt work on my PC).
(2)
