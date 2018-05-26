from distutils.core import setup
import py2exe
import os
import sys
 
sys.argv.append('py2exe')
 
# The filename of the script you use to start your program.
target_file = 'main.py'
 
# The root directory containing your assets, libraries, etc.
assets_dir = '.\\'
 
# Filetypes not to be included in the above.
excluded_file_types = ['md','py','pyc','project','pydevproject']
 
def get_data_files(base_dir, target_dir, list=[]):
    """
    " * get_data_files
    " *    base_dir:    The full path to the current working directory.
    " *    target_dir:  The directory of assets to include.
    " *    list:        Current list of assets. Used for recursion.
    " *
    " *    returns:     A list of relative and full path pairs. This is 
    " *                 specified by distutils.
    """
    for file in os.listdir(base_dir + target_dir):
 
        full_path = base_dir + target_dir + file
        if os.path.isdir(full_path):
            get_data_files(base_dir, target_dir + file + '\\', list)
        elif os.path.isfile(full_path):
            if (len(file.split('.')) == 2 and file.split('.')[1] not in excluded_file_types):
                list.append((target_dir, [full_path]))
 
    return list
 
# The directory of assets to include.
my_files = get_data_files(sys.path[0] + '\\', assets_dir)
 
# Build a dictionary of the options we want.
opts = { 'py2exe': {
                    'ascii':'True',
                    'excludes':['_ssl','_hashlib'],
                    'includes' : ['anydbm', 'dbhash'],
                    'bundle_files':'1',
                    'compressed':'True'}}
 
# Run the setup utility.
setup(windows=[target_file],
      data_files=my_files,
      zipfile=None,
      options=opts)
      
os.rename('dist/main.exe','dist/MonsterGenetics.exe')
os.rename('dist','Monster Genetics')
