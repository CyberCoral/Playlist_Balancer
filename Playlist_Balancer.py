###
### Name of project: Playlist_Balancer.py
###
### Author: CyberCoral
###
### Description: It first distributes the songs of a playlist
###              into smaller subfolders. Then, it shuffles through
###              each subfolder randomly, so every subset of songs
###              has been selected at least once per cycle.
###
### Date of start of project: 17 / 08 / 2025
###
### Version of the project: 1.0
###

import os

def ListBalancer(array: list = [1,2,3,4,5,6,7,8,9,10], number_sections: int | None = 5,*, no_remainder: bool = False) -> list[list]:
    '''
    Distributes the elements
    of the array in the specified
    number of sections.
    
    If no_remainder (a bool)
    is True and there exists
    a remainder between the
    number of elements of the array
    and the number of sections, 
    it will raise an
    AttributeError, else it will
    do nothing.
    
    array: list
    array of elements.
    
    number_sections: int | None
    must be a positive integer, not 0;
    or None for dynamic number of sections.
    
    no_remainder: bool
    '''
    
    # Check the variables.
    
    # array check.
    if isinstance(array, list) == False:
        raise TypeError("array must be a list.")
    elif len(array) == 0:
        return None # There is no distribution for a zero element array.
    
    # number_sections check.
    if number_sections == None:
        number_sections = int(len(array) ** (1/2))    
    elif isinstance(number_sections, int) == False:
        raise TypeError("number_sections must be an integer or None.")
    elif number_sections <= 0:
        raise ValueError("number_sections must be a natural number (neither negative nor 0).")
        
    # An exception.
    if number_sections >= len(array):
        print("The number of sections is greater than the number of elements,\nso it will return the same array.")
        return array
    
    # no_remainder check.
    if isinstance(no_remainder, bool) == False: 
        raise TypeError("no_remainder must be a boolean value.")
        
    #
    # The algorithm part.
    #
    
    # If the number of elements is not divisible by number_sections
    if no_remainder == True and len(array) % number_sections != 0:
        raise AttributeError("If no_remainder is True,\nand the division between the number of elements and number_sections must return an integer.")
        
    cycles = len(array) // number_sections
    remainder = len(array) % number_sections 
    
    # Contains the subdivisions of the array
    subarrays = [array[i * number_sections : (i + 1) * number_sections] for i in range(cycles)]
    subarrays += [array[::-1][:remainder][::-1]]
    
    return subarrays

def FindPlaylistPath(path: str) -> list[str]:
    '''
    Finds the playlist folder and
    gets all the filenames as 
    a list with str.
    
    path: str
    the path of the folder (playlist),
    must be a folder.
    '''
    
    cwd = os.getcwd()
        
    # Checks if path is a str.
    if isinstance(path, str) == False:
        raise TypeError("path must be a str of the path of a folder.")
    
    # Goes to the specified folder, if the folder is a 
    os.chdir("/")
    if os.path.isdir(path) == True: # Inspired by Zeth
        os.chdir(path)
    else:
        print("There was an error while finding the folder specified in path.")
        raise AttributeError("The path either does not exist or it is not a folder.")
    
    # Obtains all the filenames of the folder.
    files = [entry.name for entry in os.scandir(path)]
    
    # Goes to the directory of the project.
    os.chdir("/"); os.chdir(cwd)
    
    return files

def PlaylistBalancer(path: str, number_sections: int | None = None,*, no_remainder: bool = False, only_return_array: bool = True):
    '''
    Finds the playlist folder,
    gets all the filenames
    and distributes the files
    in the specified number 
    of sections.
    
    If no_remainder
    is True and there exists
    a remainder between the
    number of elements of the array
    and the number of sections, 
    it will raise an
    AttributeError, else it will
    do nothing.
    
    If only_return_array is True,
    it will return the array but
    it will not create the folder,
    else it will create that folder.
    
    path: str | list
    the path of the folder (playlist),
    must be a folder file or an array.
    
    number_sections: int | None
    must be a positive integer, not 0;
    or None for dynamic number of sections.
    
    no_remainder: bool
    
    only_return_array: bool
    '''
    
    if isinstance(only_return_array, bool) == False:
        raise TypeError("only_return_array must be a boolean value.")
    
    if isinstance(path, list) != True:    
        array = FindPlaylistPath(path)        
    else:
        array = list(path) # Proposed by Ayrton_E
        
    subarrays = ListBalancer(array, number_sections, no_remainder = no_remainder)
    
    def RandomCycleSelect(subarray):
        '''
        Select elements of an array
        with subarrays using 
        a cycle algorithm.
        Specialized in playlists
        (no None elements in the array)
        '''
        import random
        
        result_arr = []
        
        len_subarrs = [len(arr) for arr in subarray]
        maximum = max(len_subarrs)
        
        # Adds None elements to the exception, if it exists,
        # to make the process easier.
        if len_subarrs.count(len_subarrs[0]) != len(len_subarrs):
            exception = subarray[::-1][0]
            exception += [None for i in range(len_subarrs[0] - len(exception))]
            
        for index in range(maximum):
            # Picks a random element of each subarray and arranges it into an element.
            element = [subarray[i].pop(random.randint(0,len(subarray[i])-1)) for i in range(len(subarray))]
            
            # Filter the None elements
            element = [i for i in element if i != None]
            result_arr += element
            
        return result_arr
    
    if only_return_array == True:
        return RandomCycleSelect(subarrays)