#!/usr/bin/env python
# coding: utf-8

# # import library & define functions

# In[1]:


import pandas as pd
import numpy as np
from copy import deepcopy


# In[2]:


class Sudoku:
    def __init__(self, initial_data):
        self.result = initial_data
        self.tmp =  np.repeat(np.ones((9, 9))[:, :, np.newaxis], 9, axis=2)
        self.block_exist_place()
        print('imported data:', 'null size:', self.result_zero_size())
        self.display_result()
        
    def result_zero_size(self):
        return np.count_nonzero(self.result.flatten() == 0)
    
    def block_exist_place(self):
        non_zero_index = pd.DataFrame(np.where(self.result != 0))
        for i in list(non_zero_index.transpose().index):
            self.tmp[:, non_zero_index[i][0], non_zero_index[i][1]] = 0    

    def block_all(self):
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
                t_box_arr = self.result[a:a+3, b:b+3].flatten()
                for v in t_box_arr[t_box_arr != 0]:
                    self.tmp[v-1,a:a+3, b:b+3] = 0

    def put_all(self):
        for n in list(np.arange(9)):
            num_tmp = self.tmp[n]

            for i in list(np.arange(9)):
                # row
                if num_tmp[i][num_tmp[i] == 1].size == 1:
                    self.result[i, np.where(num_tmp[i] == 1)[0][0]] = n+1
                # column
                if num_tmp[:,i][num_tmp[:,i] == 1].size == 1:
                    self.result[np.where(num_tmp[:,i] == 1)[0][0], i] = n+1
            # box
            for a in list(np.arange(0, 7, 3)):
                for b in list(np.arange(0, 7, 3)):
                    t_box = num_tmp[a:a+3, b:b+3]
                    t = t_box.flatten()
                    if t[t == 1].size == 1:
                        self.result[a + np.where(t_box == 1)[0][0], b + np.where(t_box == 1)[1][0]] = n+1

    def block_and_put(self):
        while self.result_zero_size() != 0:
            before_size = self.result_zero_size()
            print('.')
            self.block_all()
            self.put_all()
            self.block_exist_place()
            if self.result_zero_size() == before_size:
                break

    def exploratory_calc(self):
        for i in np.arange(9):
            if self.result_zero_size() == 0:
                break
            if np.count_nonzero(self.tmp[i].flatten() != 0) == 0:
                continue

        #     print('define i:', i)
            tmp_candidates = pd.DataFrame(np.where(self.tmp[i] != 0))
            for c_i in list(tmp_candidates.transpose().index):
                self.result[ tmp_candidates[c_i][0], tmp_candidates[c_i][1]] = i+1
                self.block_exist_place()
                self.block_and_put()
        #         display(pd.DataFrame(result))
                if self.result_zero_size() == 0:
                    break
                print('unresolved size:', self.result_zero_size())
                self.result = deepcopy(self.result_bk)
                self.tmp = deepcopy(self.tmp_bk)

    def calc(self):
        self.block_and_put()
        if self.result_zero_size() != 0:
#             print('unresolved size:', self.result_zero_size())
            self.result_bk = deepcopy(self.result)
            self.tmp_bk = deepcopy(self.tmp)
        else:
            print('complete!')
        self.display_result()
        if self.result_zero_size() != 0:
            self.exploratory_calc()
            if self.result_zero_size() != 0:
                print('unresolved size:', self.result_zero_size())
                self.display_result()
            else:
                self.check_result()
                print('complete!')
    
    def display_result(self):
        display(pd.DataFrame(self.result))
    
    def display_remaining_candidate(self):
        for i in np.arange(9):
            candidate_size = np.count_nonzero(self.tmp[i].flatten() != 0)
            if candidate_size != 0:
                print('num:', i+1)
                display(pd.DataFrame(self.tmp[i].astype(int)))

    def raise_err(self):
        self.display_result()
        raise Exception('anything is wrong!')

    def check_result(self):
        for i in list(np.arange(9)):
            if np.unique(self.result[i]).size != 9:
                self.raise_err()
            if np.unique(self.result[:,i]).size != 9:
                self.raise_err()
        for a in list(np.arange(0, 7, 3)):
            for b in list(np.arange(0, 7, 3)):
                if np.unique(self.result[a:a+3, b:b+3].flatten()).size != 9:
                    self.raise_err()


# # import data

# In[3]:


result = np.loadtxt('input_data/test_1.csv', delimiter=',', dtype='int64')
sudoku = Sudoku(result)


# # calc

# In[4]:


sudoku.calc()


# # display result

# In[5]:


sudoku.display_result()


# # display remaining candidate 

# In[6]:


sudoku.display_remaining_candidate()

