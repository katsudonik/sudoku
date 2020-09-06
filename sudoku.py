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
        # row
        for r in list(np.arange(9)):
            for v in self.result[r]:
                if v != 0:
                    self.tmp[v-1,r,:] = 0
        # column
        for c in list(np.arange(9)):
            for v in self.result[:,c]:
                if v != 0:
                    self.tmp[v-1,:,c] = 0
        # box
        for a in list(np.arange(0, 7, 3)):
            for b in list(np.arange(0, 7, 3)):
                for v in self.result[a:a+3, b:b+3].flatten():
                    if v != 0:
                        self.tmp[v-1,a:a+3, b:b+3] = 0

    def put_all(self):
        for n in list(np.arange(9)):
            num_tmp = self.tmp[n]

            # row
            for r in list(np.arange(9)):
                if num_tmp[r][num_tmp[r] == 1].size == 1:
                    self.result[r, np.where(num_tmp[r] == 1)[0][0]] = n+1
            # column
            for c in list(np.arange(9)):
                if num_tmp[:,c][num_tmp[:,c] == 1].size == 1:
                    self.result[np.where(num_tmp[:,c] == 1)[0][0], c] = n+1
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
#         self.display_result()
        if self.result_zero_size() != 0:
            self.exploratory_calc()
            if self.result_zero_size() != 0:
                print('unresolved size:', self.result_zero_size())
                self.display_result()
            else:
                print('complete!')
    
    def display_result(self):
        display(pd.DataFrame(self.result))
    
    def display_remaining_candidate(self):
        for i in np.arange(9):
            candidate_size = np.count_nonzero(self.tmp[i].flatten() != 0)
            if candidate_size != 0:
                print('num:', i+1)
                display(pd.DataFrame(self.tmp[i].astype(int)))


# # import data

# In[3]:


result = np.array([
    [0,0,0,7,0,0,6,2,0],
    [0,0,6,0,8,0,0,0,1],
    [0,5,0,0,3,0,0,0,7],
    [7,0,0,0,0,0,0,0,0],
    [0,8,3,0,0,0,9,5,0],
    [0,0,0,0,0,0,0,0,3],
    [2,0,0,0,6,0,0,7,0],
    [4,0,0,0,9,0,5,0,0],
    [0,3,7,0,0,1,0,0,0],
])

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

