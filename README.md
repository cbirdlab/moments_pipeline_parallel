# moments_pipeline_parallel
dportik's 2D moments script modified to accept a SFS as input and for parallelization in linux

---

## USAGE

The strategy is to run all of the models and identify which one has the most support

1. Make sfs with easySFS
	* get vcf and popmap
	* convert popmap to the format required by easySFS (swap the columns)
	* run the preview
	* select the number of individuals
	* make the sfs
2. Make sure all dependencies are installed
3. Make sure the proper anaconda environment is activated
4. Run the following lines of code (modify variables as necessary)
  ```bash
  screen -S moments2D
  #deactivate any undesired python envs
  THREADS=4
  sfsPATH=../../easySFS/pfalcifer/output_28_80/dadi/Sekong-Mekong.sfs
  POP1ID="pop1"
  POP2ID="pop2"
  ls moments_Run_2D_??_*py | parallel --no-notice -j $THREADS "python {} $sfsPATH $POP1ID $POP2ID"
  ```

The `screen` command is optional.  Duckduckgo it.  To detach from the screen, `ctrl+a`  then `d`

### THREADS

set this to the number of cpu cores available / 8

### sfsPATH

path to the site freq spectrum file

### POP1ID

The name of population sample 1 used in the sfs

### POP2ID

The name of hte population sample 2 used in the sfs

