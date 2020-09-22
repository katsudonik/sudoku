#!/usr/bin/env python
# coding: utf-8

# # import library & define functions

# In[3]:


import pandas as pd
import numpy as np
from copy import deepcopy


# In[1]:


class Sudoku:
    def __init__(self, initial_data):
        self.result = initial_data
        self.tmp =  np.repeat(np.ones((9, 9))[:, :, np.newaxis], 9, axis=2)
        self.block_all()
        print('imported data:', 'null size:', self.result_zero_size())
        self.display_result()
        self.recursion_cnt = 0
        self.exploring_num = 0
        
    def result_zero_size(self):
        return np.count_nonzero(self.result.flatten() == 0)
    
    def block_all(self):
        # exist place
        non_zero_index = pd.DataFrame(np.where(self.result != 0))
        for i in list(non_zero_index.transpose().index):
            self.tmp[:, non_zero_index[i][0], non_zero_index[i][1]] = 0    
        
        for i in list(np.arange(9)):
            # row
            for v in self.result[i][self.result[i] != 0]:
                self.tmp[v-1,i,:] = 0
            # column
            for v in self.result[:,i][self.result[:,i] != 0]:
                self.tmp[v-1,:,i] = 0
        # box
        for a in list(np.arange(0, 7, 3)):
            for b in list(np.arange(0, 7, 3)):
                ## this box
                t_box_arr = self.result[a:a+3, b:b+3].flatten()
                for v in t_box_arr[t_box_arr != 0]:
                    self.tmp[v-1,a:a+3, b:b+3] = 0
                ## other box
                self.block_other_box(a, b)

    def block_other_box(self, a, b):
        r_cands_v = [[],[],[]]
        c_cands_v = [[],[],[]]
        k = np.arange(0, 7, 3)
        n_arr = np.arange(9)
        for n in list(n_arr):
            num_tmp = self.tmp[n]
            t_box = num_tmp[a:a+3, b:b+3]
            # block other box's row
            r_candidates = np.where(np.sum(t_box, axis=1) != 0)[0]
            if r_candidates.size == 1:
                block_r = a + r_candidates[0]
                for t_b in k[k != b]:
                    self.tmp[n, block_r, t_b:t_b+3] = 0
                r_cands_v[r_candidates[0]].append(n)
            # block other box's column
            c_candidates = np.where(np.sum(t_box, axis=0) != 0)[0]
            if c_candidates.size == 1:
                block_c = b + c_candidates[0]
                for t_a in k[k != a]:
                    self.tmp[n, t_a:t_a+3, block_c] = 0
                c_cands_v[c_candidates[0]].append(n)

        # block this box
        for i in list(range(3)):
            ## block this box's row
            res_box_r = self.result[a+i, b:b+3]
            if res_box_r[res_box_r == 0].size == len(r_cands_v[i]):
                for n in n_arr[~np.isin(n_arr, r_cands_v[i])]:
                    self.tmp[n, a+i, b:b+3] = 0
            ## block this box's column
            res_box_c = self.result[a:a+3, b+i]
            if res_box_c[res_box_c == 0].size == len(c_cands_v[i]):
                for n in n_arr[~np.isin(n_arr, c_cands_v[i])]:
                    self.tmp[n, a:a+3, b+i] = 0

    def put(self, r, c, v):
        self.result[r, c] = v
        # block
        ## exist place
        self.tmp[:, r, c] = 0
        ## row
        self.tmp[v-1,r,:] = 0
        ## column
        self.tmp[v-1,:,c] = 0
        ## box
        a = list(np.arange(0, 7, 3))[int(r/3)]
        b = list(np.arange(0, 7, 3))[int(c/3)]
        self.tmp[v-1,a:a+3, b:b+3] = 0
        ## other box
        self.block_other_box(a, b)

    def put_in_fixed_places(self):
        for n in list(np.arange(9)):
            num_tmp = self.tmp[n]
            for i in list(np.arange(9)):
                # row
                if num_tmp[i].sum() == 1:
                    self.put(i, np.where(num_tmp[i] == 1)[0][0], n+1)
                # column
                if num_tmp[:,i].sum() == 1:
                    self.put(np.where(num_tmp[:,i] == 1)[0][0], i, n+1)
            # box
            for a in list(np.arange(0, 7, 3)):
                for b in list(np.arange(0, 7, 3)):
                    t_box = num_tmp[a:a+3, b:b+3]
                    if t_box.flatten().sum() == 1:
                        self.put(a + np.where(t_box == 1)[0][0], b + np.where(t_box == 1)[1][0], n+1)
                        
        # candidate size: 1 (tecknick 2)
        candidate_size_map = np.sum(self.tmp, axis=0)
        candidate_one_indexes = pd.DataFrame(np.where(candidate_size_map == 1))
        if len(candidate_one_indexes.transpose().index) >= 1:
            i = candidate_one_indexes.transpose().index[0]
            this_cell_layers = self.tmp[:, candidate_one_indexes[i][0], candidate_one_indexes[i][1]]
            self.put(candidate_one_indexes[i][0], candidate_one_indexes[i][1], np.where(this_cell_layers == 1)[0][0] + 1)

    def repeat_put_in_fixed_places(self):
        while self.result_zero_size() != 0:
            before_size = self.result_zero_size()
            self.put_in_fixed_places()
            if self.result_zero_size() == before_size:
                break

    def exploratory_calc(self):
        candidate_size_map = np.sum(self.tmp, axis=0)
        min_size = candidate_size_map[candidate_size_map != 0].min()
        min_size_indexes = pd.DataFrame(np.where(candidate_size_map == min_size))
        for i in list(min_size_indexes.transpose().index):
            candidate_values = list(np.where(self.tmp[:, min_size_indexes[i][0], min_size_indexes[i][1]] == 1)[0] + 1)
            for v in candidate_values:
                self.put(min_size_indexes[i][0], min_size_indexes[i][1], v)
                self.repeat_put_in_fixed_places()
                if self.result_zero_size() == 0:
                    return True
                if np.count_nonzero(self.tmp.flatten() != 0) != 0:
                    # NOTE: append savepoint
                    self.recursion_cnt += 1
                    print('recursion_cnt: ', self.recursion_cnt)
                    self.result_bk.append(deepcopy(self.result))
                    self.tmp_bk.append(deepcopy(self.tmp))
                    # NOTE: recurrent run
                    if self.exploratory_calc() == True:
                        return True
                # NOTE: rollback
                self.result = deepcopy(self.result_bk[self.recursion_cnt])
                self.tmp = deepcopy(self.tmp_bk[self.recursion_cnt])
        self.recursion_cnt -= 1
        self.result_bk = self.result_bk[:-1]
        self.tmp_bk = self.tmp_bk[:-1]
        return False  
        
    def calc(self):
        self.repeat_put_in_fixed_places()
        if self.result_zero_size() == 0:
            self.check_result()
            print('complete!')
        else:
#             print('unresolved size:', self.result_zero_size())
            self.result_bk = [deepcopy(self.result)]
            self.tmp_bk = [deepcopy(self.tmp)]
#             self.total_candidate_size = pd.DataFrame(np.where(self.tmp != 0)).transpose().index.size
#             print('total candidate size: ', self.total_candidate_size)
            self.exploratory_calc()
            if self.result_zero_size() == 0:
                self.check_result()
                print('complete!')
            else:
                print('unresolved size:', self.result_zero_size())
                self.display_result()

                
    # debug functions:
    
    def display_result(self):
        display( pd.DataFrame( np.where(self.result == 0, None, self.result) ).style.highlight_null(null_color='red') )
    
    def display_remaining_candidate(self):
        for i in np.arange(9):
            candidate_size = np.count_nonzero(self.tmp[i].flatten() != 0)
            if candidate_size != 0:
                print('num:', i+1)
                display(pd.DataFrame(self.tmp[i].astype(int)))

    def raise_err(self):
        raise Exception('anything is wrong!')

    def check_result(self):
        for i in list(np.arange(9)):
            if np.unique(self.result[i]).size != 9:
                display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=pd.IndexSlice[i:i]) )
                self.raise_err()
            if np.unique(self.result[:,i]).size != 9:
                display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=[i]) )
                self.raise_err()
        for a in list(np.arange(0, 7, 3)):
            for b in list(np.arange(0, 7, 3)):
                if np.unique(self.result[a:a+3, b:b+3].flatten()).size != 9:
                    display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=pd.IndexSlice[a:a+2, b:b+2]) )
                    self.raise_err()

    def check_result_duplicate(self):
        for i in list(np.arange(9)):
            if np.unique(self.result[i][self.result[i] != 0]).size != self.result[i][self.result[i] != 0].size:
                display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=pd.IndexSlice[i:i]) )
                self.raise_err()
            if np.unique(self.result[:,i][self.result[:,i] != 0]).size != self.result[:,i][self.result[:,i] != 0].size:
                display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=[i]) )
                self.raise_err()
        for a in list(np.arange(0, 7, 3)):
            for b in list(np.arange(0, 7, 3)):
                t = self.result[a:a+3, b:b+3].flatten()
                if (np.unique(t[t != 0]).size) != (t[t != 0].size):
                    display( pd.DataFrame(self.result).style.background_gradient(cmap='winter', subset=pd.IndexSlice[a:a+2, b:b+2]) )
                    self.raise_err()

    def display_by_color(self, df, subset):
        display( df.style.background_gradient(cmap='winter', subset=subset) )

