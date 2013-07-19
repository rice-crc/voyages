import os

os.chdir("./csvdumps")

execfile('load_broadregion.py')
execfile('load_region.py')
execfile('load_places.py')
execfile('load_fate.py')
execfile('load_owner_outcome.py')
execfile('load_slave_outcome.py')
execfile('load_vessel_outcome.py')
execfile('load_resistance.py')
execfile('load_nations.py')
execfile('load_rig_of_vessel.py')
execfile('load_sources.py')
execfile('load_tontype.py')
execfile('load_voyage.py')
execfile('load_groupings.py')
#execfile('update_voyage_fks.py')
execfile('update_voyage_groupings_cd_rom.py')

os.chdir("./..")