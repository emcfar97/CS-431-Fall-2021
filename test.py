import os, shutil
from os.path import splitext, join, exists
import mysql.connector as sql

# DATAB = sql.connect(
#     user='root', password='SchooL1@', database='userData', 
#     host='192.168.1.43' if __file__.startswith(('e:\\', 'e:/')) else '127.0.0.1'
#     )
# CURSOR = DATAB.cursor(buffered=True)

path = r'C:\Users\Emc11\Downloads\Katawa Shoujo'
dest = r'C:\Users\Emc11\Dropbox\Videos\ん\エラティカ 三'
sprites = {}

# for i in range(3):

    #     for file in os.listdir(path):

    #         if not file.endswith('jpg'): continue
    #         file = splitext(file)[0]
    #         try: 
    #             char, pose, expr = file.split('_')[1:]
    #             if not char.startswith(("shiz", "mish", "lill", "hanak", "emi", "rin")): continue
    #         except ValueError: continue
            
    #         if i == 0: 
    #             if char == 'emiwheel': continue
    #             if char == 'shizuyu': continue
    #             if char == 'rinpan': continue
                
    #             sprites[char] = {}
            
    #         elif i == 1: 
    #             if char == 'shizuyu':
    #                 pose = char
    #                 char = 'shizu'
    #             if char == 'emiwheel':
    #                 pose = char
    #                 char = 'emi'
    #             if char == 'rinpan': 
    #                 pose = char
    #                 char = 'rin'
                
    #             sprites[char][pose] = []

    #         elif i == 2: 
    #             if char == 'shizuyu':
    #                 pose = char
    #                 char = 'shizu'
    #             if char == 'emiwheel':
    #                 pose = char
    #                 char = 'emi'
    #             if char == 'rinpan': 
    #                 pose = char
    #                 char = 'rin'
                
    #             sprites[char][pose].append(expr)

