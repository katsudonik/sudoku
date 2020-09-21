#!/usr/bin/env python
# coding: utf-8

# # import library & define functions

# In[1]:


import pandas as pd
import numpy as np
import sudoku
import importlib
importlib.reload(sudoku)


# # import data

# In[2]:


result = np.loadtxt('input_data/test_2.csv', delimiter=',', dtype='int64')
sudoku = sudoku.Sudoku(result)


# # calc

# In[3]:


sudoku.calc()


# # display result

# In[4]:


# sudoku.display_result()


# # display remaining candidate 

# In[5]:


# sudoku.display_remaining_candidate()


# In[ ]:


sudoku.exploratory_calc()


# In[ ]:


if sudoku.result_zero_size() == 0:
    sudoku.check_result()
    print('complete!')
else:
    print('unresolved size:', sudoku.result_zero_size())
    sudoku.display_result()


# In[ ]:


# np.sort(sudoku.result, axis=1)


# In[ ]:


# np.sort(sudoku.result, axis=0)

