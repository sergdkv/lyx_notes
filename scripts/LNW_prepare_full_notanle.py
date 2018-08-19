#!/usr/bin/python
# -*- coding: cp1251 -*-
# merge_clean_and_labeled_sfiles.py
import sys
import  re
import pprint

def lines_not_match( a, b ):
    a2 = re.sub( 'NWHEADSTART.*?NWHEADEND', '', a );
    a3 = re.sub( '[ \t]*', '', a2 );
    b2 = re.sub( 'NWHEADSTART.*?NWHEADEND', '', b );
    b3 = re.sub( '[ \t]*', '', b2 );
    return a3 != b3

clean_file=file(sys.argv[1]).readlines()
L_file=file(sys.argv[2]).readlines()


def find_and_repair( clean_file, L_file, start_line ):
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
