import os
import pkgconfig
from cyther import core
from subprocess import Popen, PIPE



def parseInclude(flag):
    """Function to parse include from pkgconfig module"""
    # Equivalent command line : 
    # pkg-config --libs --cflags python3
    # Return : -I/usr/include/python3.7m -I/usr/include/x86_64-linux-gnu/python3.7m -lpython3.7m
    # Function transform to (parsable content for Popen): 
    # -I /usr/include/python3.7m -I /usr/include/x86_64-linux-gnu/python3.7m -l python3.7m

    try:
        # Parse includes from a dict, which contains list as values
        parseDict = pkgconfig.parse(flag)
        # Initialize empty array
        includes = []
        # Parse 1st list and concatene str with -I
        for dirs in parseDict['include_dirs']:
            includes.append(f'-I {dirs}')
        # Idem for libraries and concatene str with -l
        for lib in parseDict['libraries']:
            includes.append(f'-l {lib}')

        # Concatene all element of list with space
        finalInclude = ' '.join(includes)
        # Return a final boolean value
        result = True

    except pkgconfig.PackageNotFoundError as error:
        print(f"Includes for {flag} not founds")
        # Return a final boolean value and empty finalInclude
        finalInclude = ''
        result = False

    return result, finalInclude


def convert_to_cython(src, dst):
    """Function to convert python code to Cython, with python interpreter embed"""
    # Command line equivalent : 
    # cython -3 -v --embed hello.py -o hello.c

    # Define command
    command = f"cython -3 -v --embed {src} -o {dst}"
    # split it and launch it with Popen
    process = Popen(command.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # Get output stout and stderr of the command
    output, error = process.communicate()
    # Get return code
    returnCode = process.returncode

    # Check return code 
    if returnCode == 0:
        print(f'Successfully conversion to {dst}')
        # Initialize a boolean result of function
        result = True

    elif returnCode != 0:
        print('An error occured during agent conversion to C')
        print(output.decode())
        result = False


    return result



def compile_to_elf(src, dst):
    """Function to compile Cython code to ELF binary"""
    # Command line equivalent : 
    # gcc CSOURCE -o ELFDEST $(pkg-config --libs --cflags python3)

    # Parse python3 includes for gcc command (receive boolean and string)
    state, includes = parseInclude('python3')
    print(includes)

    # If includes are valid
    if state is not False:
        # Define a gcc command and launch it with Popen
        command = f"gcc {src} -o {dst} {includes}"
        process = Popen(command.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # Get stdout and stderr of command
        output, error = process.communicate()
        # Get return code
        returnCode = process.returncode

        # Parse return code
        if returnCode == 0:
            print(f"Successfully compilation to {dst}")
            result = True
        elif returnCode != 0:
            print(f"An error occured during compilation : ")
            print(error.decode())
            result = False

    # If includes are invalid
    elif state is False:
        print("Compilation aborted")        
        os.remove(src)
        result = False

    
    return result


def main_compile(src):
    """Main function to launch compilation"""

    parentFolder = os.path.dirname(src)
    basename = os.path.basename(src)
    name = os.path.splitext(basename)[0]
    
    cFile = f"{parentFolder}/{name}.c"
    elfFile = f"{parentFolder}/{name}"

    cythonResult = convert_to_cython(src, cFile)
    if cythonResult is True:
        compileResult = compile_to_elf(cFile, elfFile)
        if compileResult is True:
            os.remove(cFile)
            os.remove(src)
    elif cythonResult is False:
        os.remove(cFile)

