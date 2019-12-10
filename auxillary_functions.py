##This script contains auxillary functions for the scheduling assignment 

##This function schedules the staff by including one constraint at a time until all 9 are used 
def scheduling_2 (week):
    
    ##week      --- an array containing the type of days 
    
    import os 
    current_directory = os.path.dirname(__file__) + '//' 
    import numpy as np    
    
    ##Defining the staff information 
    staff = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    ag1 = ['s0', 's1', 's2', 's3']
    ag2 = ['s4', 's5']
    ag3 = ['s6', 's7', 's8']
    fg = ['s1', 's2', 's3', 's8']
    always_off_ph = ['s1', 's2', 's3', 's8']
    req_4hr_shift_per_week = ['s0', 's2', 's5']
    
    
    ##Predefining soft constraint terms
    soft_c_ag1 = []
    soft_c_ag2 = []
    soft_c_ag3 = []
    
    penalty_value = 0.5
        ##Morning shift soft constraints 
    for i in range (0, len(week)):
        soft_c_ag1.append('soft_c_ag1' + '_' + str(i))
        soft_c_ag2.append('soft_c_ag2' + '_' + str(i))    
        soft_c_ag3.append('soft_c_ag3' + '_' + str(i))
        
    script_loc = current_directory + 'working_folder//script.lp'    
    
    f_data_set = open(script_loc, 'w')
    
    ##Writing the objective function 
        ##We want to minimize the number of staff working at any given period
    f_data_set.write('\\\\ Objective function \n \n')
    f_data_set.write('Minimize \n')
    f_data_set.write('\n')       
    
    obj_func_input = ''
    
    ##Adding the soft constraint penalty terms to the objective function 
    obj_func_input = obj_func_input + '-' + str(penalty_value) + ' ' + soft_c_ag1[0] + ' - '
    for i in range (1, len(soft_c_ag1)):
        obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag1[i] + ' - '
    for i in range (0, len(soft_c_ag2)):
        obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag2[i] + ' - '        
    for i in range (0, len(soft_c_ag3)):   
        if i == len(soft_c_ag3) - 1:
            obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag3[i] + ' + '   
        else:              
            obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag3[i] + ' - '    
            
    ##Since this is solved on a weekly basis, we need to index the staff based on the day 
        ##The m(i) and a(i) attached to the end are to denote morning and afternoon shifts 
        
    for i in range (0, len(week)):
        ##Writing the number of staff
        for j in range (0, len(staff)):
            ##Writing the number of morning shifts 
            for k in range (0, 3):
                obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_m' + str(k) + ' + '
            ##Writing the number of afternoon shifts 
            for k in range (0, 2):
                if (i == len(week) - 1) and (j == len(staff) - 1) and (k == 1):
                    obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_a' + str(k)
                else:
                    obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_a' + str(k) + ' + '        
                    
    f_data_set.write('obj: ' + obj_func_input) 
    f_data_set.write('\n \n')    
    
    ##Writing the constraints 
        ##As a first step, we write the constraints without taking into consideration the number of hours each staff works 
        ##Just the daily requirement fulfilled.
        
    ##Writing the constraints  
    f_data_set.write('Subject To \n \n')

    ##A running index to label the constraints 
    current_index = 0
    
    ##Writing the morning/afternoon shifts constraints 
    f_data_set.write('\\\\ Writing the morning/afternoon shifts constraints \n \n')
    
    for i in range (0, len(week)):
        ##If it is a weekday 
        if week[i] == 'wd':
            ##Morning shift requirements 
            cons = 'c' + str(current_index) + ': '
            ##For the morning shift 
                
            ##Writing the total staff constraints for the morning shifts 
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' >= 4 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '      

            ##Afternoon shift requirements
            cons = 'c' + str(current_index) + ': '
            ##For the afternoon shift 
            
            ##Writing the total staff constraints for the afternoon shifts 
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the afternoon shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag1)- 1) and (k == 1):
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag2)- 1) and (k == 1):
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '
                        
        ##If it is a weekend or public holiday 
        else:
            ##Morning shift requirements 
            cons = 'c' + str(current_index) + ': '
            ##For the morning shift 
                
            ##Writing the total staff constraints for the morning shifts 
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' >= 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the morning shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag1)- 1) and (k == 2):
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' < ' + str(len(ag1))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag2)- 1) and (k == 2):
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag2))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag3))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '                      

            ##Afternoon shift requirements
            cons = 'c' + str(current_index) + ': '
            ##For the afternoon shift 
            
            ##Writing the total staff constraints for the afternoon shifts 
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the afternoon shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag1)- 1) and (k == 1):
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag2)- 1) and (k == 1):
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '
                        
    ##Writing penalty functions for the violation of soft constraints 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the penalty functions for the violation of soft constraints \n \n')
    
    ##Writing the morning shift constraints  
    for i in range (0, len(week)):
        
        ##For the first morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag1)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag1)- 1) and (k == 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag1[i] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '                
        
        ##For the second morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag2)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag2)- 1) and (k == 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag2[i] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '     

        ##For the third morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag3)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag3)- 1) and (k == 2):
                    cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag2[3] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '   

    ##Writing the constraints that allow only 1 shift per day 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the constraints that allow only 1 shift per day \n \n')
    for i in range (0, len(week)):
        for j in range (0, len(staff)):
            cons = 'c' + str(current_index) + ': '
            ##Writing the number of morning shifts 
            for k in range (0, 3):
                cons = cons + staff[j] + '_' + str(i) + '_m' + str(k) + ' + '
            ##Writing the number of afternoon shifts 
            for k in range (0, 2):
                if k == 1:
                    cons = cons + staff[j] + '_' + str(i) + '_a' + str(k) + ' <= 1' 
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1    
                else:
                    cons = cons + staff[j] + '_' + str(i) + '_a' + str(k) + ' + '    
    
    ##All staff must have 1 day off 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the constraints that ensures that each staff has at least 1 day off \n \n') 
    
    for i in range (0, len(staff)):
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(week)):
            ##Morning shift 
            for k in range (0, 3):
                cons = cons + staff[i] + '_' + str(j) + '_m' + str(k) + ' + '
            ##Afternoon shoft 
            for k in range (0, 2):
                if (k == 1) and (j == len(week) - 1):
                    cons = cons + staff[i] + '_' + str(j) + '_a' + str(k) + ' = 6 '
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                      
                else:
                    cons = cons + staff[i] + '_' + str(j) + '_a' + str(k) + ' + '                
                
    ##All staff must have exactly 44 working hours per week 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the constraints that ensures that each staff must have 44 working hours \n \n')     
    
    morning = [9, 8, 4]         ##Number of working hours in each shift
    afternoon = [9, 8]          
    
    for i in range (0, len(staff)):
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(week)):
            ##Morning shift 
            for k in range (0, 3):
                cons = cons +  str(morning[k]) + ' ' + staff[i] + '_' + str(j) + '_m' + str(k) + ' + '
            ##Afternoon shoft 
            for k in range (0, 2):
                if (k == 1) and (j == len(week) - 1):
                    cons = cons + str(afternoon[k]) + ' ' + staff[i] + '_' + str(j) + '_a' + str(k) + ' = 44 '
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                      
                else:
                    cons = cons + str(afternoon[k]) + ' ' + staff[i] + '_' + str(j) + '_a' + str(k) + ' + '                              
    
    ##Writing constraints that makes sure that a staff is always off on a public holiday 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the constraints that ensures the stipulated staff have to be off on public holidays \n \n')   
    for i in range (0, len(week)):
        if week[i] == 'ph':
            for j in range (0, len(always_off_ph)):
                cons = 'c' + str(current_index) + ': '
                ##Writing the number of morning shifts 
                for k in range (0, 3):
                    cons = cons + always_off_ph[j] + '_' + str(i) + '_m' + str(k) + ' + '
                ##Writing the number of afternoon shifts 
                for k in range (0, 2):
                    if k == 1:
                        cons = cons + always_off_ph[j] + '_' + str(i) + '_a' + str(k) + ' = 0' 
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1    
                    else:
                        cons = cons + always_off_ph[j] + '_' + str(i) + '_a' + str(k) + ' + '     
    
    
    ##The staffs are binary variables 
    f_data_set.write('\n')
    f_data_set.write('Binary \n \n')   

    for i in range (0, len(week)):
        for j in range (0, len(staff)):
            for k in range (0, 3):
                f_data_set.write(staff[j] + '_' + str(i) + '_m' + str(k))
                f_data_set.write('\n')            
            for k in range (0,2):
                f_data_set.write(staff[j] + '_' + str(i) + '_a' + str(k))
                f_data_set.write('\n')                  
    
    for i in range (0, len(soft_c_ag1)):
        f_data_set.write(soft_c_ag1[i])
        f_data_set.write('\n')            

    for i in range (0, len(soft_c_ag2)):
        f_data_set.write(soft_c_ag2[i])
        f_data_set.write('\n')  
        
    for i in range (0, len(soft_c_ag3)):
        f_data_set.write(soft_c_ag3[i])
        f_data_set.write('\n')  
    
    ##Wrapping up 
    f_data_set.write('\n') 
    f_data_set.write('End \n')    
    f_data_set.close        
 
    return 

##This function schedules the staff based on the consideration of 
    ##The groupings of the staff
    ##The nature of the shifts 
    ##The required number of staff per day
    ##Hard and soft constraints
def scheduling_1 (week):
    
    ##week      --- an array containing the type of days 
    
    import os 
    current_directory = os.path.dirname(__file__) + '//' 
    import numpy as np    
    
    ##Defining the staff information 
    staff = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    ag1 = ['s0', 's1', 's2', 's3']
    ag2 = ['s4', 's5']
    ag3 = ['s6', 's7', 's8']
    fg = ['s1', 's2', 's3', 's8']
    always_off_ph = []
    req_4hr_shift_per_week = ['s0', 's2', 's5']
    
    
    ##Predefining soft constraint terms
    soft_c_ag1 = []
    soft_c_ag2 = []
    soft_c_ag3 = []
    
    penalty_value = 0.5
        ##Morning shift soft constraints 
    for i in range (0, len(week)):
        soft_c_ag1.append('soft_c_ag1' + '_' + str(i))
        soft_c_ag2.append('soft_c_ag2' + '_' + str(i))    
        soft_c_ag3.append('soft_c_ag3' + '_' + str(i))
        
    script_loc = current_directory + 'working_folder//script.lp'    
    
    f_data_set = open(script_loc, 'w')
    
    ##Writing the objective function 
        ##We want to minimize the number of staff working at any given period
    f_data_set.write('\\\\ Objective function \n \n')
    f_data_set.write('Minimize \n')
    f_data_set.write('\n')       
    
    obj_func_input = ''
    
    ##Adding the soft constraint penalty terms to the objective function 
    obj_func_input = obj_func_input + '-' + str(penalty_value) + ' ' + soft_c_ag1[0] + ' - '
    for i in range (1, len(soft_c_ag1)):
        obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag1[i] + ' - '
    for i in range (0, len(soft_c_ag2)):
        obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag2[i] + ' - '        
    for i in range (0, len(soft_c_ag3)):   
        if i == len(soft_c_ag3) - 1:
            obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag3[i] + ' + '   
        else:              
            obj_func_input = obj_func_input + str(penalty_value) + ' ' + soft_c_ag3[i] + ' - '    
            
    ##Since this is solved on a weekly basis, we need to index the staff based on the day 
        ##The m(i) and a(i) attached to the end are to denote morning and afternoon shifts 
        
    for i in range (0, len(week)):
        ##Writing the number of staff
        for j in range (0, len(staff)):
            ##Writing the number of morning shifts 
            for k in range (0, 3):
                obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_m' + str(k) + ' + '
            ##Writing the number of afternoon shifts 
            for k in range (0, 2):
                if (i == len(week) - 1) and (j == len(staff) - 1) and (k == 1):
                    obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_a' + str(k)
                else:
                    obj_func_input = obj_func_input + staff[j] + '_' + str(i) + '_a' + str(k) + ' + '        
                    
    f_data_set.write('obj: ' + obj_func_input) 
    f_data_set.write('\n \n')    
    
    ##Writing the constraints 
        ##As a first step, we write the constraints without taking into consideration the number of hours each staff works 
        ##Just the daily requirement fulfilled.
        
    ##Writing the constraints  
    f_data_set.write('Subject To \n \n')

    ##A running index to label the constraints 
    current_index = 0
    
    ##Writing the morning/afternoon shifts constraints 
    f_data_set.write('\\\\ Writing the morning/afternoon shifts constraints \n \n')
    
    for i in range (0, len(week)):
        ##If it is a weekday 
        if week[i] == 'wd':
            ##Morning shift requirements 
            cons = 'c' + str(current_index) + ': '
            ##For the morning shift 
                
            ##Writing the total staff constraints for the morning shifts 
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' = 4 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the morning shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag1)- 1) and (k == 2):
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' < ' + str(len(ag1))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag2)- 1) and (k == 2):
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag2))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag3))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '                      

            ##Afternoon shift requirements
            cons = 'c' + str(current_index) + ': '
            ##For the afternoon shift 
            
            ##Writing the total staff constraints for the afternoon shifts 
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' = 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the afternoon shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag1)- 1) and (k == 1):
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag2)- 1) and (k == 1):
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '
                        
        ##If it is a weekend or public holiday 
        else:
            ##Morning shift requirements 
            cons = 'c' + str(current_index) + ': '
            ##For the morning shift 
                
            ##Writing the total staff constraints for the morning shifts 
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' = 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the morning shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag1)- 1) and (k == 2):
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' < ' + str(len(ag1))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag2)- 1) and (k == 2):
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag2))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of morning shifts 
                for k in range (0, 3):
                    if (j == len(ag3)- 1) and (k == 2):
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) +  ' < ' + str(len(ag3))
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '                      

            ##Afternoon shift requirements
            cons = 'c' + str(current_index) + ': '
            ##For the afternoon shift 
            
            ##Writing the total staff constraints for the afternoon shifts 
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' = 3 '                         
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1     
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '      
                
                ##Writing the number of staff required from each group in the afternoon shift 
                    ##From ag1
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag1)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag1)- 1) and (k == 1):
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag1[j] + '_' + str(i) + '_a' + str(k) + ' + '                        
                    ##From ag2
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag2)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag2)- 1) and (k == 1):
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag2[j] + '_' + str(i) + '_a' + str(k) + ' + '              
                    ##From ag3
            cons = 'c' + str(current_index) + ': '            
            for j in range (0, len(ag3)):
                ##The number of afternoon shifts 
                for k in range (0, 2):
                    if (j == len(ag3)- 1) and (k == 1):
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' >= 1'
                        f_data_set.write(cons + '\n')  
                        current_index = current_index + 1  
                    else:
                        cons = cons + ag3[j] + '_' + str(i) + '_a' + str(k) + ' + '
                        
    ##Writing penalty functions for the violation of soft constraints 
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the penalty functions for the violation of soft constraints \n \n')
    
    ##Writing the morning shift constraints  
    for i in range (0, len(week)):
        
        ##For the first morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag1)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag1)- 1) and (k == 2):
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag1[i] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag1[j] + '_' + str(i) + '_m' + str(k) + ' + '                
        
        ##For the second morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag2)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag2)- 1) and (k == 2):
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag2[i] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag2[j] + '_' + str(i) + '_m' + str(k) + ' + '     

        ##For the third morning group
        cons = 'c' + str(current_index) + ': '
        for j in range (0, len(ag3)):
            ##The number of morning shifts 
            for k in range (0, 3):             
                if (j == len(ag3)- 1) and (k == 2):
                    cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' - ' + soft_c_ag2[3] + ' >= 0'
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1                    
                    
                else:
                    cons = cons + ag3[j] + '_' + str(i) + '_m' + str(k) + ' + '   

    ##Writing the constraints that allow only 1 shift per day for each of the staffs
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing the constraints that allow only 1 shift per day for each of the staffs \n \n')
    for i in range (0, len(week)):
        for j in range (0, len(staff)):
            cons = 'c' + str(current_index) + ': '
            ##Writing the number of morning shifts 
            for k in range (0, 3):
                cons = cons + staff[j] + '_' + str(i) + '_m' + str(k) + ' + '
            ##Writing the number of afternoon shifts 
            for k in range (0, 2):
                if k == 1:
                    cons = cons + staff[j] + '_' + str(i) + '_a' + str(k) + ' <= 1' 
                    f_data_set.write(cons + '\n')  
                    current_index = current_index + 1    
                else:
                    cons = cons + staff[j] + '_' + str(i) + '_a' + str(k) + ' + '                          
  
    ##The staffs are binary variables 
    f_data_set.write('\n')
    f_data_set.write('Binary \n \n')   

    for i in range (0, len(week)):
        for j in range (0, len(staff)):
            for k in range (0, 3):
                f_data_set.write(staff[j] + '_' + str(i) + '_m' + str(k))
                f_data_set.write('\n')            
            for k in range (0,2):
                f_data_set.write(staff[j] + '_' + str(i) + '_a' + str(k))
                f_data_set.write('\n')                  
    
    for i in range (0, len(soft_c_ag1)):
        f_data_set.write(soft_c_ag1[i])
        f_data_set.write('\n')            

    for i in range (0, len(soft_c_ag2)):
        f_data_set.write(soft_c_ag2[i])
        f_data_set.write('\n')  
        
    for i in range (0, len(soft_c_ag3)):
        f_data_set.write(soft_c_ag3[i])
        f_data_set.write('\n')  
    
    ##Wrapping up 
    f_data_set.write('\n') 
    f_data_set.write('End \n')    
    f_data_set.close        
 
    return 

##This function calls GLPK to solve the problem 
def call_GLPK ():
    
    import subprocess
    import os 
    current_directory = os.path.dirname(__file__) + '\\' 
    
    ##Directories 
    main_call = current_directory + 'glpk-4.61\w64\glpsol --lp'
    file_location = current_directory + 'working_folder\script.lp'
    result_location = current_directory + 'working_folder\out.txt'
    
    command = main_call + ' ' + file_location + ' -o ' + result_location
    
    print(command)
    
    o = subprocess.check_call(command, shell= True)
    ## Checking for the output of the solver 
    if os.path.isfile(result_location) == False:
        convergence = 0
        return o, convergence
    
    else:
        if os.path.getsize(result_location) == 0:
            convergence = 0
            return o, convergence
    
    with open(result_location, 'r') as fo:
        solver_msg = fo.read()
    
    if 'OPTIMAL' in solver_msg:
        convergence = 1
    
    else:
        convergence = 0
    
    return o, convergence

##This function extracts the results from the text file 
def extract_GLPK_results ():
     
    import os 
    current_directory = os.path.dirname(__file__) + '\\' 
    import pandas as pd 
    
    ##Result file location 
    result_file = current_directory + 'working_folder\\out.txt'
    
    ##Extracting the objective function 
    with open(result_file) as fo:
        for rec in fo:
            if 'Objective:  ' in rec:
                obj = rec.split(' ')
                break
    obj_value = float(obj[4])

    ##Establishing the list of results to extract 
    staff = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    list_names = []
    
    for i in range (0, 7):          ##Days in a week 
        for j in range (0, len(staff)):
            for k in range (0, 3):
                list_names.append(staff[j] + '_' + str(i) + '_m' + str(k))
            for k in range (0, 2):
                list_names.append(staff[j] + '_' + str(i) + '_a' + str(k))                
                
            
    #Extracting the rest of the values 
        ##Parameters to search the file by 
        starting_line = 0
        variable_count = 0        
        last_line = 0    
 
        ##Initiating a dataframe to hold the return values 
        results_final = pd.DataFrame(columns = ['Names', 'Values'])
    
    with open(result_file) as fo:
        for rec in fo:
            if last_line == 1:
                break            
            else:
                check_split = rec.split()
                if check_split:
                    if starting_line < 2:
                        if len(check_split) != 0:
                            if str.isdigit(check_split[0]) == True:
                                if int(check_split[0]) == 1:
                                    starting_line = starting_line + 1            
            
                    ##This is where the records should start
                    if starting_line == 2:
                        if variable_count < len(list_names):
                            if (str.isdigit(check_split[1]) == False) and (len(check_split[1]) > 12): 
                                if check_split[1] in list_names:
                                    temp_name = check_split[1]
                                    check_split2 = next(fo).split()
                                    temp_data_to_save = [temp_name, int(check_split2[1])]
                                    temp_data_to_save_df = pd.DataFrame(data = [temp_data_to_save], columns = ['Names', 'Values'])
                                    results_final = results_final.append(temp_data_to_save_df, ignore_index = True)
                                
                            elif (str.isdigit(check_split[1]) == False):
                                if check_split[1] == 'feasibility':
                                    last_line = 1
                                    break
                                elif check_split[1] in list_names:
                                    temp_name = check_split[1]
                                    temp_data_to_save = [temp_name, int(check_split[3])]
                                    temp_data_to_save_df = pd.DataFrame(data = [temp_data_to_save], columns = ['Names', 'Values'])
                                    results_final = results_final.append(temp_data_to_save_df, ignore_index = True)
                                    variable_count = variable_count + 1    
            
    return obj_value, results_final


