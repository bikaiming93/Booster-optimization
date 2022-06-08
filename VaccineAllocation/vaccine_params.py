import numpy as np
import datetime as dt
import pandas as pd
from VaccineAllocation import config
import iteround

class Vaccine:
    '''
        Vaccine class to define epidemiological characteristics, supply and fixed allocation schedule of vaccine.
        Parameters:
            vaccine_data: (dict) dict of vaccine characteristics.
            vaccine_allocation_data: (dict) contains vaccine schedule, supply and allocation data.
            booster_allocation_data: (dict) contains booster schedule, supply and allocation data.
            instance: data instance      
                
    '''    
    def __init__(self, vaccine_data, vaccine_allocation_data, booster_allocation_data, instance):
        self.effect_time = vaccine_data['effect_time']
        self.waning_time = vaccine_data['waning_time']
        self.second_dose_time = vaccine_data['second_dose_time']
        self.beta_reduct = vaccine_data['beta_reduct'] 
        self.tau_reduct = vaccine_data['tau_reduct'] 
        self.beta_reduct_delta = vaccine_data['beta_reduct_delta'] 
        self.tau_reduct_delta = vaccine_data['tau_reduct_delta'] 
        self.tau_reduct_omicron = vaccine_data['tau_reduct_omicron'] 
        self.instance = instance
        self.vaccine_supply = self.define_supply(instance, vaccine_allocation_data, booster_allocation_data)
          
        
    def define_groups(self, problem_type):  
        '''
             Define different vaccine groups. 
             {
                 group 0: unvaccinated group,
                 group 1: partially vaccinated, 
                 group 2: fully vaccinated,    
                 group 3: waning efficacy group.   
             }
             
             Assuming:
                 - one type of vaccine with two-doses
                 - after first dose move to group 1 compartment.
                 - after second dose move to group 2 compartment.
                 - after efficacy wanes, move to group 3 compartment.
                 - If boster shot is administred move from group 3 compartment to group 2 compartment.
                           
        '''  
        # Including vaccine groups
        self._vaccine_groups = []
        self._vaccine_groups.append(Vaccine_group('v_0', 0, 0, 0, 0, 0, self.instance, problem_type)) #unvax
        self._vaccine_groups.append(Vaccine_group('v_1', self.beta_reduct[1], self.tau_reduct[1], self.beta_reduct_delta[1], self.tau_reduct_delta[1], self.tau_reduct_omicron[1], self.instance, problem_type)) # partially vaccinated
        self._vaccine_groups.append(Vaccine_group('v_2', self.beta_reduct[2], self.tau_reduct[2], self.beta_reduct_delta[2], self.tau_reduct_delta[2], self.tau_reduct_omicron[2], self.instance, problem_type)) # fully vaccinated
        self._vaccine_groups.append(Vaccine_group('v_3', self.beta_reduct[0], self.tau_reduct[0], self.beta_reduct_delta[0], self.tau_reduct_delta[0], self.tau_reduct_omicron[0], self.instance, problem_type)) # waning efficacy
        return self._vaccine_groups      
    

    def define_supply(self, instance, vaccine_allocation_data, booster_allocation_data):
        '''
        Load vaccine supply and allocation data, and process them.
        Shift vaccine schedule for waiting vaccine to be effective, second dose and vaccine waning effect and also for booster dose.
        '''
        N = instance.N
        self.actual_vaccine_time = [time for time in vaccine_allocation_data['vaccine_time']] 
        self.first_dose_time = [time + dt.timedelta(days = self.effect_time) for time in vaccine_allocation_data['vaccine_time']]
        self.second_dose_time = [time + dt.timedelta(days = self.second_dose_time + self.effect_time) for time in self.first_dose_time if time + dt.timedelta(days = self.second_dose_time + self.effect_time) <= instance.end_date]

        
        self.waning_time = [time + dt.timedelta(days = self.waning_time)  for time in vaccine_allocation_data['vaccine_time'] if time + dt.timedelta(days = self.waning_time) <= instance.end_date] 
        self.vaccine_proportion = [amount for amount in vaccine_allocation_data['vaccine_amount']]  
     
        self.vaccine_start_time = np.where(np.array(instance.cal.calendar) == self.actual_vaccine_time[0])[0]
        
       
        v_first_allocation = []
        v_second_allocation = []
        v_booster_allocation = []
        v_wane_allocation = []
        
        # Fixed vaccine allocation:
        for i in range(len(vaccine_allocation_data['A1-R1'])):
            vac_assignment = np.zeros((5, 2))
            vac_assignment[0, 0] = vaccine_allocation_data['A1-R1'][i]
            vac_assignment[0, 1] = vaccine_allocation_data['A1-R2'][i]
            vac_assignment[1, 0] = vaccine_allocation_data['A2-R1'][i]
            vac_assignment[1, 1] = vaccine_allocation_data['A2-R2'][i]
            vac_assignment[2, 0] = vaccine_allocation_data['A3-R1'][i]
            vac_assignment[2, 1] = vaccine_allocation_data['A3-R2'][i]
            vac_assignment[3, 0] = vaccine_allocation_data['A4-R1'][i]
            vac_assignment[3, 1] = vaccine_allocation_data['A4-R2'][i]
            vac_assignment[4, 0] = vaccine_allocation_data['A5-R1'][i]
            vac_assignment[4, 1] = vaccine_allocation_data['A5-R2'][i]
                     
            if np.sum(vac_assignment) > 0:
                pro_round = vac_assignment/np.sum(vac_assignment)
            else:
                pro_round = np.zeros((5, 2))
            within_proportion = vac_assignment/N   
            
            # First dose vaccine allocation:    
            supply_first_dose =  {'time': self.first_dose_time[i], 'amount': self.vaccine_proportion[i], 'type': "first_dose"}
            allocation_item = {'assignment': vac_assignment, 'proportion': pro_round, 'within_proportion': within_proportion,  'supply': supply_first_dose, 'type': 'first_dose', 'from': 'v_0', 'to': 'v_1'}    
            v_first_allocation.append(allocation_item)
            
            # Second dose vaccine allocation:  
            if i < len(self.second_dose_time):
                supply_second_dose =  {'time': self.second_dose_time[i], 'amount': self.vaccine_proportion[i], 'type': "second_dose"}
                allocation_item = {'assignment': vac_assignment, 'proportion': pro_round,'within_proportion': within_proportion,  'supply': supply_second_dose, 'type': 'second_dose', 'from': 'v_1', 'to': 'v_2'}    
                v_second_allocation.append(allocation_item)
            
           
            # Waning vaccine efficacy:
            if i < len(self.waning_time):
                supply_waning =  {'time': self.waning_time[i], 'amount': self.vaccine_proportion[i], 'type': "waning"}
                allocation_item = {'assignment': vac_assignment, 'proportion': pro_round, 'within_proportion': within_proportion, 'supply': supply_waning, 'type': 'waning', 'from': 'v_2', 'to': 'v_3'}    
                v_wane_allocation.append(allocation_item)
            
            
        # Fixed booster vaccine allocation:
        if booster_allocation_data is not None:
            self.booster_time = [time  for time in booster_allocation_data['vaccine_time']]
            self.booster_proportion = [amount for amount in booster_allocation_data['vaccine_amount']]  
            for i in range(len(booster_allocation_data['A1-R1'])):
                vac_assignment = np.zeros((5, 2))
                vac_assignment[0, 0] = booster_allocation_data['A1-R1'][i]
                vac_assignment[0, 1] = booster_allocation_data['A1-R2'][i]
                vac_assignment[1, 0] = booster_allocation_data['A2-R1'][i]
                vac_assignment[1, 1] = booster_allocation_data['A2-R2'][i]
                vac_assignment[2, 0] = booster_allocation_data['A3-R1'][i]
                vac_assignment[2, 1] = booster_allocation_data['A3-R2'][i]
                vac_assignment[3, 0] = booster_allocation_data['A4-R1'][i]
                vac_assignment[3, 1] = booster_allocation_data['A4-R2'][i]
                vac_assignment[4, 0] = booster_allocation_data['A5-R1'][i]
                vac_assignment[4, 1] = booster_allocation_data['A5-R2'][i]
                     
                if np.sum(vac_assignment) > 0:
                    pro_round = vac_assignment/np.sum(vac_assignment)
                else:
                    pro_round = np.zeros((5, 2))
                within_proportion = vac_assignment/N   
            
                # Booster dose vaccine allocation:    
                supply_booster_dose =  {'time': self.booster_time[i], 'amount': self.booster_proportion[i], 'type': "booster_dose"}
                allocation_item = {'assignment': vac_assignment, 'proportion': pro_round, 'within_proportion': within_proportion,  'supply': supply_booster_dose, 'type': 'booster_dose', 'from': 'v_3', 'to': 'v_2'}    
                v_booster_allocation.append(allocation_item)
 
            
        
        self.vaccine_allocation = {'v_first': v_first_allocation, 'v_second': v_second_allocation, 'v_booster': v_booster_allocation, 'v_wane': v_wane_allocation}
        #breakpoint()      
    
class Vaccine_group:
    def __init__(self, v_name, v_beta_reduct, v_tau_reduct, v_beta_reduct_delta, v_tau_reduct_delta, v_tau_reduct_omicron, instance, problem_type):
        '''
        Define each vaccine status as a group. Define each set of compartments for vaccine group.
        
        Parameters
        ----------
        v_name : string
            vaccine status type.
        v_beta_reduct : float [0,1]
            reduction in transmission.
        v_tau_reduct : float [0,1]
            reduction in symptomatic infection.   
        instance : 
            problem instance.

        '''
        self.v_beta_reduct = v_beta_reduct
        self.v_tau_reduct = v_tau_reduct
        self.v_beta_reduct_delta = v_beta_reduct_delta
        self.v_tau_reduct_delta = v_tau_reduct_delta
        self.v_tau_reduct_omicron = v_tau_reduct_omicron
        self.v_name = v_name
    
        T, A, L = instance.T, instance.A, instance.L
        step_size = config['step_size']
   
        
        types = 'int' if problem_type == 'stochastic' else 'float'
        #breakpoint()
            
        self.S = np.zeros((T, A, L), dtype=types)
        self.E = np.zeros((T, A, L), dtype=types)
        self.IA = np.zeros((T, A, L), dtype=types)
        self.IY = np.zeros((T, A, L), dtype=types)
        self.PA = np.zeros((T, A, L), dtype=types)
        self.PY = np.zeros((T, A, L), dtype=types)
        self.IH = np.zeros((T, A, L), dtype=types)
        self.ICU = np.zeros((T, A, L), dtype=types)
        self.R = np.zeros((T, A, L), dtype=types)
        self.D = np.zeros((T, A, L), dtype=types)
        self.IYIH = np.zeros((T - 1, A, L))
        self.IYICU = np.zeros((T - 1, A, L))
        self.IHICU = np.zeros((T - 1, A, L))
        self.ToICU = np.zeros((T - 1, A, L))
        self.ToIHT = np.zeros((T - 1, A, L))
        self.ToICUD = np.zeros((T - 1, A, L))
        self.ToIYD = np.zeros((T - 1, A, L))
        self.ToIA = np.zeros((T - 1, A, L))
        self.ToIY = np.zeros((T - 1, A, L))
        
        self._S = np.zeros((step_size + 1, A, L), dtype=types)
        self._E = np.zeros((step_size + 1, A, L), dtype=types)
        self._IA = np.zeros((step_size + 1, A, L), dtype=types)
        self._IY = np.zeros((step_size + 1, A, L), dtype=types)
        self._PA = np.zeros((step_size + 1, A, L), dtype=types)
        self._PY = np.zeros((step_size + 1, A, L), dtype=types)
        self._IH = np.zeros((step_size + 1, A, L), dtype=types)
        self._ICU = np.zeros((step_size + 1, A, L), dtype=types)
        self._R = np.zeros((step_size + 1, A, L), dtype=types)
        self._D = np.zeros((step_size + 1, A, L), dtype=types)
        self._IYIH = np.zeros((step_size, A, L))
        self._IYICU = np.zeros((step_size, A, L))
        self._IHICU = np.zeros((step_size, A, L))
        self._ToICU = np.zeros((step_size, A, L))
        self._ToIHT = np.zeros((step_size, A, L))
        self._ToICUD = np.zeros((step_size, A, L))
        self._ToIYD = np.zeros((step_size, A, L))
        self._ToIA = np.zeros((T - 1, A, L))
        self._ToIY = np.zeros((T - 1, A, L))
        
        
        if self.v_name == 'v_0':
            N, I0 = instance.N, instance.I0
            # Initial Conditions (assumed)
            self.PY[0] = I0
            self.R[0] = 0
            self.S[0] = N - self.PY[0] - self.IY[0]
            
        self._S[0] = self.S[0].copy()
        self._E[0] = self.E[0].copy()
        self._IA[0] = self.IA[0].copy()
        self._IY[0] = self.IY[0].copy()
        self._PA[0] = self.PA[0].copy()
        self._PY[0] = self.PY[0].copy()
        self._IH[0] = self.IH[0].copy()
        self._ICU[0] = self.ICU[0].copy()
        self._R[0] = self.R[0].copy()
        self._D[0] = self.D[0].copy()
    
    
    def reset_history(self, instance, seed):
        '''
            reset history for a new simulation.
        '''
        T, A, L = instance.T, instance.A, instance.L
        step_size = config['step_size']
       
        types = 'int' if seed >= 0 else 'float'
        #breakpoint()
        
        self.S = np.zeros((T, A, L), dtype=types)
        self.E = np.zeros((T, A, L), dtype=types)
        self.IA = np.zeros((T, A, L), dtype=types)
        self.IY = np.zeros((T, A, L), dtype=types)
        self.PA = np.zeros((T, A, L), dtype=types)
        self.PY = np.zeros((T, A, L), dtype=types)
        self.IH = np.zeros((T, A, L), dtype=types)
        self.ICU = np.zeros((T, A, L), dtype=types)
        self.R = np.zeros((T, A, L), dtype=types)
        self.D = np.zeros((T, A, L), dtype=types)
        self.IYIH = np.zeros((T - 1, A, L))
        self.IYICU = np.zeros((T - 1, A, L))
        self.IHICU = np.zeros((T - 1, A, L))
        self.ToICU = np.zeros((T - 1, A, L))
        self.ToIHT = np.zeros((T - 1, A, L))
        self.ToICUD = np.zeros((T - 1, A, L))
        self.ToIYD = np.zeros((T - 1, A, L))
        self.ToIA = np.zeros((T - 1, A, L))   
        self.ToIY = np.zeros((T - 1, A, L))
        
        self._S = np.zeros((step_size + 1, A, L), dtype=types)
        self._E = np.zeros((step_size + 1, A, L), dtype=types)
        self._IA = np.zeros((step_size + 1, A, L), dtype=types)
        self._IY = np.zeros((step_size + 1, A, L), dtype=types)
        self._PA = np.zeros((step_size + 1, A, L), dtype=types)
        self._PY = np.zeros((step_size + 1, A, L), dtype=types)
        self._IH = np.zeros((step_size + 1, A, L), dtype=types)
        self._ICU = np.zeros((step_size + 1, A, L), dtype=types)
        self._R = np.zeros((step_size + 1, A, L), dtype=types)
        self._D = np.zeros((step_size + 1, A, L), dtype=types)
        self._IYIH = np.zeros((step_size, A, L))
        self._IYICU = np.zeros((step_size, A, L))
        self._IHICU = np.zeros((step_size, A, L))
        self._ToICU = np.zeros((step_size, A, L))
        self._ToIHT = np.zeros((step_size, A, L))
        self._ToICUD = np.zeros((step_size, A, L))
        self._ToIYD = np.zeros((step_size, A, L))          
        self._ToIA = np.zeros((T - 1, A, L))   
        self._ToIY = np.zeros((T - 1, A, L))
        
        if self.v_name == 'v_0':
            N, I0 = instance.N, instance.I0
            # Initial Conditions (assumed)
            self.PY[0] = I0
            self.R[0] = 0
            self.S[0] = N - self.PY[0] - self.IY[0]
                
        self._S[0] = self.S[0].copy()
        self._E[0] = self.E[0].copy()
        self._IA[0] = self.IA[0].copy()
        self._IY[0] = self.IY[0].copy()
        self._PA[0] = self.PA[0].copy()
        self._PY[0] = self.PY[0].copy()
        self._IH[0] = self.IH[0].copy()
        self._ICU[0] = self.ICU[0].copy()
        self._R[0] = self.R[0].copy()
        self._D[0] = self.D[0].copy()
        
    def vaccine_flow(self, instance, allocation):
        '''
            Define the flow of individuals between susceptible compartments of different vaccine groups.
            Assume the flow is mechanistics (alternative could be to have exponential flow). 
        '''
        T, A, L = instance.T, instance.A, instance.L
        total_risk_gr = A*L
        N = instance.N
        
        self.v_out = []
        self.v_in = []
        N_out = np.zeros((total_risk_gr, T))
        N_in = np.zeros((total_risk_gr, T))
        N_eligible = []

        if self.v_name == 'v_0':
            allocation_in = []
            allocation_out = allocation['v_first']
            
        elif self.v_name == 'v_1':
            allocation_in = allocation['v_first']
            allocation_out = allocation['v_second']
         
        elif self.v_name == 'v_2':
            allocation_in = allocation['v_second']
            allocation_in.extend(allocation['v_booster'])
            allocation_out = allocation['v_wane']
        else:
            allocation_in = allocation['v_wane']
            allocation_out = allocation['v_booster']
        
        
        #breakpoint()
        for allocation_item in allocation_in:
            a = {'daily_assignment': allocation_item['assignment_daily'], 'from': allocation_item['from'], 'time': allocation_item['supply']['time']}
            N_in += allocation_item['assignment_daily']  
            self.v_in.append(a)
            
        for allocation_item in allocation_out:
            a = {'daily_assignment': allocation_item['assignment_daily'], 'to': allocation_item['to'], 'time': allocation_item['supply']['time']}
            N_out += allocation_item['assignment_daily']  
            self.v_out.append(a)
        
        if self.v_name == 'v_0':
            for age_risk_gr in range(total_risk_gr):
                    N_eligible.append([N.reshape(total_risk_gr)[age_risk_gr] - np.sum(N_out[age_risk_gr, 0:t]) for t in range(T)])
        else:
            for age_risk_gr in range(total_risk_gr):
                N_eligible.append([np.sum(N_in[age_risk_gr, 0:t]) - np.sum(N_out[age_risk_gr, 0:t]) for t in range(T)])
                
        self.N_eligible = N_eligible
      
        
    def delta_update(self, prev):
        '''
            Update efficacy according to delta variant (VoC) prevelance.
        '''
        
        self.v_beta_reduct = self.v_beta_reduct * (1 - prev) + self.v_beta_reduct_delta * prev #decreased efficacy against infection.
        self.v_tau_reduct = self.v_tau_reduct * (1 - prev) + self.v_tau_reduct_delta * prev #decreased efficacy against symptomatic infection.    
     
    def omicron_update(self, prev):
        '''
            Update efficacy according to omicron variant (VoC) prevelance.
        '''
        self.v_tau_reduct = self.v_tau_reduct * (1 - prev) + self.v_tau_reduct_omicron * prev
        #breakpoint() 
        