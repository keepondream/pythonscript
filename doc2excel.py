#!/usr/bin/env python
# Filename: doc2excel.py
# Function: Transfer doc to excel list
# -*- coding: UTF-8 -*-
# Author: Well

import os, re, sys, xlrd, xlwt, argparse

def debug(mesage, is_debug=True):
    if mesage and is_debug:
        print 'DEBUG',
        print mesage


def doc2txt(doc_file):
    doc_file = doc_file
    ###add "" for special filename
    os.system("catdoc '%s' > test.txt" % doc_file)
    print 'Transfer doc or docx to txt successfully'
    return 'test.txt'


### cut the file begin with begin regex, end with end regex
def cut_file(file_line_list,begin_reg,end_reg,is_debug=False):
    begin_count=0
    end_count=0
    ###cannot use list.index to confirm the index, due to the line may be dup
    line_index=0
    cut_result_list=[]
    for line in file_line_list:
        is_begin=re.search(begin_reg, line)
        is_end=re.search(end_reg, line)
        if is_begin:
            begin_count+=1
            begin_index=line_index
            debug('''Match the begin flag "%s"''' % line, is_debug)
        elif is_end:
            end_count+=1
            end_index=line_index
            debug('''Match the end flag "%s"''' % line, is_debug)
        else:
            pass
        ###only both count >0, get the begin index to end index's content
        if begin_count >= 1 and end_count >=1:
            debug('The begin index is %s, end index is %s' % (begin_index,end_index),is_debug)
            cut_result_list.append(file_line_list[begin_index:end_index])
            ###set the count to 0
            begin_count=0
            end_count=0
        line_index+=1
    return cut_result_list


def write_excel(row_num,col_num,value,sheet_object):
    ###transfer to u mode
    sheet_object.write(row_num,col_num,value)

 
parse = argparse.ArgumentParser(description='Telnet host to execute CLI')
parse.add_argument('-df', '--docfile', required=False,  action='append', default=[], dest='doc_file_list',
                    help='doc file path')

parse.add_argument('-tf', '--txtfile', required=False,  action='append', default=[], dest='txt_file_list',
                    help='txt file path')

parse.add_argument('-ef', '--excelfile', required=False, default=None, dest='excel_file',
                    help='excel file path')

parse.add_argument('-sn', '--sheetname', required=False, action='append', default=[], dest='sheet_name_list',
                    help='Sheet name')

parse.add_argument('-b', '--begin', required=False, default='^Case ID', dest='begin_reg',
                    help='begin regex')

parse.add_argument('-e', '--end', required=False, default='^Test Result', dest='end_reg',
                    help='end regex')

parse.add_argument('-debug', '--debug', required=False, default=False,action='store_true', dest='is_debug',
                    help='enable debug mode')
 
 

def main():
    args = parse.parse_args() 
    doc_file_list=args.doc_file_list
    txt_file_list=args.txt_file_list
    excel_file=args.excel_file
    is_debug=args.is_debug
    begin_reg=args.begin_reg
    end_reg=args.end_reg
    sheet_name_list=args.sheet_name_list
    excel_object = xlwt.Workbook(encoding='utf-8')
    is_doc=False
    is_txt=False
    ### if set sheet name list , need check if match the num of doc_list
    if len(sheet_name_list) > 0 and len(doc_file_list)!=len(sheet_name_list):
        print 'doc files num and sheets num is not the same, please check'
        return None
    if doc_file_list:
        is_doc=True
        text_file_list=doc_file_list
    elif txt_file_list:
        is_txt=True
        text_file_list=txt_file_list
    ###used for sheet name list index if the two list' length is the same
    text_index = 0
    for text_file in text_file_list:
        if is_doc:
            debug('Transfer text to txt',is_debug)
            text_file=doc2txt(text_file)
            debug('Transfer successfully, open the txt',is_debug)
        with open(text_file, mode='rb') as text_open:
            text_list=text_open.readlines()
        cut_list=cut_file(text_list,begin_reg,end_reg,is_debug)
        debug('cut list is as below')
        debug(cut_list,is_debug)
        info_list=[]
        ### get info(case_id auto_flag priority description) from file
        for unit_list in cut_list:
            case_id=''
            priority=''
            auto_flag=''
            description=''
            for line in unit_list:
                case_id_reg=re.search('Case ID\s+([.\w-]+)',line)
                if case_id_reg:
                    case_id=case_id_reg.group(1)
                priority_reg=re.search('Priority\s+(\w+)',line)
                if priority_reg:
                    priority=priority_reg.group(1)
                auto_flag_reg=re.search('Automation Flag\s+(\w+)',line)
                if auto_flag_reg:
                    auto_flag=auto_flag_reg.group(1)
                description_reg=re.search('Description\s+(.*)',line)
                if description_reg:
                    description=description_reg.group(1)
                    description=re.sub(r'\xe2\x80\x99','',description)
            ###
#            if case_id and auto_flag and priority and description:
            if case_id and priority and description:   
                info_list.append((case_id,priority,auto_flag,description))
        debug('info list is as below')
        debug(info_list,is_debug)
        ###open a excel
        if len(sheet_name_list) == 0:
            debug('Not set sheet name, use default instead')
            sheet_name='sheet%s' % text_index
        else:
            debug('Sheet name has been set and the num is same with text')
            sheet_name=sheet_name_list[text_index]
        debug('sheet name is %s' % sheet_name, is_debug)
        sheet_object=excel_object.add_sheet(sheet_name)
        row_index=0
        for case_id,priority,auto_flag,description in info_list:
            write_excel(row_index,0,case_id,sheet_object)
            write_excel(row_index,1,priority,sheet_object)
            write_excel(row_index,2,auto_flag,sheet_object)
            write_excel(row_index,3,description,sheet_object)
            row_index += 1
        text_index += 1
        debug('Write sheet %s successfully' % sheet_name,is_debug)
    debug('Write all sheets successfully',is_debug)
    ###if not set execl file name, may use text's first one insteal
    if excel_file:
        excel_file_name=excel_file
    else:
        if is_doc:
            excel_file_name=re.sub('doc$|docx$','xls',text_file_list[0])
        elif is_txt:
            excel_file_name=re.sub('txt','xls',text_file_list[0])
    debug('excel name is %s' % excel_file_name)
    excel_object.save(excel_file_name)
    debug('Save file %s successfully' % excel_file_name,is_debug)

if __name__=='__main__':
    try:
        doc2excel_result=main()
    except Exception, e:
        print str(e)
