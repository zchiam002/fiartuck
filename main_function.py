##This function runs the scheduling assignment
    ##First the ILP problem is written and solved using GLPK
    
def schedule_workforce ():
    
    from auxillary_functions import scheduling_1
    from auxillary_functions import scheduling_2
    from auxillary_functions import call_GLPK
    from auxillary_functions import extract_GLPK_results
    from auxillary_functions import convert_glpk_results
    
    ##We first break down the problem which is to be optimized on a weekly basis, as each week seems independent of the other.  
        ##wd --- weekday 
        ##we --- weekend 
        ##ph --- public holiday 
    week1 = ['wd', 'wd', 'wd', 'wd', 'wd', 'we', 'we']      
    week2 = ['wd', 'wd', 'wd', 'wd', 'wd', 'we', 'we']
    week3 = ['wd', 'ph', 'ph', 'wd', 'wd', 'we', 'we']
    week4 = ['wd', 'ph', 'ph', 'wd', 'wd', 'we', 'we']
    
    ##This function takes in 1 week and solves for the assignment problem by considering 
        ##Staff 1, 3 and 6 MUST take 1 4 hour shift in the week 
        ##The groupings of the staff
        ##The nature of the shifts 
        ##The required number of staff per day 
    #scheduling_1(week1)       

    ##This function takes in 1 week and incorporates the 9 constraints 
    scheduling_2(week1)                                          
    ##After the script is written, we solve it by calling GLPK
    o, convergence = call_GLPK ()    
    ##Extracting the GLPK results
    obj_value, results_final = extract_GLPK_results()
    ##Convert GLPK results to readable form 
    convert_glpk_results (results_final)
    
    
    print(obj_value)
    print(results_final)
    

        
    return 

###################################################################################################################################################################################
###################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    schedule_workforce()
    