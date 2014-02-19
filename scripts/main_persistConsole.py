
""" Launch the LCCEditor with a command window from windows explorer

    Command window persists to display messages

"""



ERROR_MSG = "\nERROR: {0}\n"
NO_ERROR_MSG = "\n\nNo Errors!  You are awesome!  :-)\n"
PAUSE_MSG = "\nPress the Enter key to continue..."


try:
    import main
    print __file__
    main.main()
    print NO_ERROR_MSG
    
except Exception, err:
    print ERROR_MSG.format(str(err))
    

raw_input(PAUSE_MSG)   
 

    


