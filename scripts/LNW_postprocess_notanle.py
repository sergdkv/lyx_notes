#!/usr/bin/python
# -*- coding: cp1251 -*-
# merge_clean_and_labeled_sfiles.py
import sys
import  re
import pprint

def delete_NWHEAD_tags( s ):
    start='NWHEADSTART'
    end='NWHEADEND'
    i1 = 0
    while True:
       i1 = s.find( start, i1 )
       if i1 == -1: 
           return s
       i2 = s.find( end, i1 + len(start) )
       if i2 == -1: 
           return s
       start_pos=i1
       end_pos=i2+len(end)
       s = s[:start_pos] + s[end_pos:]


def lines_not_match( a, b ):
    return delete_NWHEAD_tags(a) != delete_NWHEAD_tags(b)

clean_file=file(sys.argv[1]).readlines()
tagged_file=file(sys.argv[2]).readlines()


def find_and_repair( clean_text, tagged_text, start_line ):
  # сравниваем файлы clean_file и L_file
  # ищем место несоответствия строк файлов и пытаемся починить их
  # возвращаем новый текст L_file или False если починить файл невозможно

  
  l1 = len(clean_file)
  l2 = len(L_file)
  for N_line in range( start_line, min( l1, l2 )):
     if lines_not_match( clean_file[N_line], L_file[N_line] ):
       k = 0
       for i2 in range( -1, 50 ):
         i = N_line - i2
         if i >= len(L_file): continue
         if i < 1 : break
         if re.match( '^NWHEADSTART', L_file[i] ) :
            ### пытаемся исправить ошибку объединив строки i и i-1
            old_im1 = L_file[i-1]
            old_i = L_file[i]
            L_file[i-1] = old_im1.rstrip( '\r\n' ) + old_i
            del ( L_file[i] )
            new_start_line = min( i, N_line )
            ### рекурсивный вызов
            ### проверяем, исправлена ли ошибка и нужно ли исправить другие ошибки
            res = find_and_repair( clean_file, L_file, new_start_line )
            if res != False : return res
            ### попытка исправить ошибку не удалась. откат
            L_file[i-1] = old_im1
            L_file.insert( i, old_i )
            k += 1
         if k > 3: break
       return False
  return L_file

res = find_and_repair( clean_file, L_file, 0 )

l1 = len(res)
l2 = len(clean_file)
for N_line in range(max( l1, l2 )):
    if lines_not_match( clean_file[N_line], res[N_line] ):
       print >>sys.stderr, "Error in line ", N_Line
       sys.exit(1)

sys.stdout.writelines( res )
