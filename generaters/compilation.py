
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
        # Return a final boolean value
        result = False

    return result


def convert_to_cython(src, dst):
    """Function to convert python code to Cython, with python interpreter embed"""
    # Command line equivalent : 
    # cython -3 -v --embed hello.py -o hello.c

    command = f"cython -3 -v --embed {src} -o {dst}"

    process = Popen(command.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error = process.communicate()
    returnCode = process.returncode

    if returnCode == 0:
        print(f'Successfully conversion to {dst}')
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

    includes = parseInclude('python3')

    if includes is not False:

        command = f"gcc {src} -o {dst} {includes}"
        process = Popen(command.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()
        returnCode = process.returncode

        if returnCode == 0:
            print(f"Successfully compilation to {dst}")
            result = True
        elif returnCode != 0:
            print(f"An error occured during compilation : ")
            print(error.decode())
            result = False

    elif includes is False:
        print("Compilation aborted")        
        os.remove(src)
        result = False

    
    return result
