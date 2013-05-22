#!/usr/bin/env python
# Filename: ixia_pkt_compare.py
# Function: Compare standard mac/ip list and collect pkts' mac/ip addresses list print miss entries 
# coding:utf-8
# Author: Will
# Example command: python ixia_pkt_compare -f ixia_capture_file(txt mode) -p srcmac -b standard_begin_mac -l  standard_list_num
import re,argparse

def mac_range_list(mac_start,mac_increase,mac_mode='upper'):
    mac_start_hex=mac_start.replace(':','')
#    hex_originate=''.join(mac_originate.split(':'))
    mac_start_dec=int(mac_start_hex,16)
    mac_range=[]
    for i in range(mac_start_dec,mac_start_dec+mac_increase):
        if i <= 65535:
            mac_entry= '0000:0000:%04x' % i
        elif i <= 4294967295:
            mac_delta= '%08x' % i
            mac_entry= '0000:%s:%s' % (''.join(mac_delta[:4 ]),''.join(mac_delta[4:]))
        elif i <= 281474976710655:
            mac_delta= '%012x' % i
            mac_entry= '%s:%s:%s' % (''.join(mac_delta[:4 ]),''.join(mac_delta[4:8]),''.join(mac_delta[ 8:]))
        else:
            print 'Not match the Mac address format'
        if mac_mode == 'upper':
            mac_range.append(mac_entry.upper())
        elif mac_mode == 'lower':
            mac_range.append(mac_entry.lower())
        else:
            print 'mac_mode input error, please type in lower or uppper'
    return mac_range

def ip_range_list(ip_start,ip_increase):
    ip_start_hex=''.join(['%02x' % int(i) for i in ip_start.split('.')])
    ip_start_dec=int(ip_start_hex,16)
    ip_range=[]
    for i in range(ip_start_dec,ip_start_dec+ip_increase):
        if i <= 4294967295:
            ip_delta= '%08x' % i
            ip_entry= '%s.%s.%s.%s' % (int(ip_delta[0:2],16),int(ip_delta[2:4],16),int(ip_delta[4:6],16),int(ip_delta[6:],16))
            ip_range.append(ip_entry)
        else:
            print 'IP_start add increase number is bigger the ip address format'
    return ip_range

def read_ixia_file(File_Path,Pkt_Parameter= 'srcmac'):
    file_open=open(File_Path)
    file_data=file_open.readlines()
#    print file_data
    file_open.close()
    file_mac_list=[]
    func_warn=0
    if Pkt_Parameter == 'srcmac' or Pkt_Parameter == 'dstmac':
        for i_file_line in file_data:
            file_mac_entries=re.findall(r'(\w{2}\s\w{2}\s\w{2}\s\w{2}\s\w{2}\s\w{2})\t' ,i_file_line)
#            print file_mac_entries
            mac_format_list=[]
###Format the mac from '00 00 00 00 00 00' to '0000:0000:0000'
            for i_mac_entry in file_mac_entries:
                mac_format_separate_list=list(i_mac_entry.replace( ' ','' ))
                mac_format_entry= '%s:%s:%s' % ('' .join(mac_format_separate_list[: 4]), '' .join(mac_format_separate_list[ 4: 8]), ''.join(mac_format_separate_list[ 8:]))
#                print 'mac_format_entry is %s' % mac_format_entry
                mac_format_list.append(mac_format_entry)
#            print 'mac_format_list is %s' % mac_format_list
            file_mac_list+=mac_format_list[:2]    
#        print file_mac_list
        Total_entry=len(file_mac_list)
        file_src_mac_list=[]
        file_dst_mac_list=[]
        for j in range(Total_entry):
            if j% 2 == 0:
                file_dst_mac_list.append(file_mac_list[j])
            elif j% 2 == 1:
                file_src_mac_list.append(file_mac_list[j])

    if Pkt_Parameter == 'srcip_gre' or Pkt_Parameter == 'dstip_gre' or Pkt_Parameter == 'srcmac_gre' or Pkt_Parameter == 'dstmac_gre':
        file_ip_src_gre_list=[]
        file_ip_dst_gre_list=[]
        file_mac_src_gre_list=[]
        file_mac_dst_gre_list=[]
        for i_file_line in file_data:
            file_pkt_entries=re.findall(r'\w{2} \w{2} \w{2} \w{2} \w{2} \w{2}',i_file_line)
###Jude the pkts' protocol whether GRE or not
            try:
                pkt_protocol = file_pkt_entries[3].replace(' ','')[6:8]
            except IndexError:
                func_warn+=1
                continue
            else:
                if pkt_protocol != '2F':
                    continue
###Get the offset your want and set them to a string without blank
            if Pkt_Parameter == 'srcip_gre' or Pkt_Parameter == 'dstip_gre':
                file_ip_info=''.join(file_pkt_entries[4:6]).replace(' ','')
###The first two lines are not the data raw,so may cause info='',cause int('',16) raise ValueError
                try:
                    file_ip_src_gre='%d.%d.%d.%d' % (int(file_ip_info[0:2],16),int(file_ip_info[2:4],16),int(file_ip_info[4:6],16),int(file_ip_info[6:8],16))
                except ValueError:
                    func_warn+=1
                else:
                    file_ip_src_gre_list.append(file_ip_src_gre)
                try:
                    file_ip_dst_gre='%d.%d.%d.%d' % (int(file_ip_info[8:10],16),int(file_ip_info[10:12],16),int(file_ip_info[12:14],16),int(file_ip_info[14:16],16))
                except ValueError:
                    func_warn+=1
                else:
                    file_ip_dst_gre_list.append(file_ip_dst_gre)
            if Pkt_Parameter == 'srcmac_gre' or Pkt_Parameter == 'dstmac_gre':
                file_mac_info=''.join(file_pkt_entries[7:10]).replace(' ','')
###The first two lines are not the data raw,so may cause info='',cause int('',16) raise ValueError
                try:
                    file_mac_src_gre='%s:%s:%s' % (file_mac_info[16:20],file_mac_info[20:24],file_mac_info[24:28])
                except ValueError:
                    func_warn+=1
                else:
                    file_mac_src_gre_list.append(file_mac_src_gre)
                try:
                    file_mac_dst_gre='%s:%s:%s' % (file_mac_info[4:8],file_mac_info[8:12],file_mac_info[12:16])
                except ValueError:
                    func_warn+=1
                else:
                    file_mac_dst_gre_list.append(file_mac_dst_gre)
    if Pkt_Parameter == 'srcmac':
        return file_src_mac_list
    elif Pkt_Parameter == 'dstmac':
        return file_dst_mac_list        
    elif Pkt_Parameter == 'srcip_gre':
        return file_ip_src_gre_list
    elif Pkt_Parameter == 'dstip_gre':
        return file_ip_dst_gre_list
    elif Pkt_Parameter == 'srcmac_gre':
        return file_mac_src_gre_list
    elif Pkt_Parameter == 'dstmac_gre':
        return file_mac_dst_gre_list

def list_compare(list_standard,list_compare):
    dict_standard={}
    for i_key in list_standard:
        dict_standard[i_key]=0
    dict_compare={}
    for j_key in list_compare:
#if list_standard not has the key,may raise the KeyError
        try:
            j_appear = dict_standard[j_key]
        except KeyError:
            j_appear = -1
        else:
            j_appear += 1
            dict_standard[j_key]=j_appear
        dict_compare[j_key] = j_appear
#Merger the two dicts  
    Tuple_Merger=dict_standard.items()+dict_compare.items()
    dict_Merger={}
    for i_tuple_key,i_tuple_value in Tuple_Merger:
        dict_Merger[i_tuple_key]=i_tuple_value
    return dict_Merger

parser = argparse.ArgumentParser(description='Compare two list and get the different')

parser.add_argument('-f', '--file', required=True, default=None, dest='file_path',
                    help='IXIA capture pkts file')

parser.add_argument('-p', '--parameters', required=True, default='srcmac', choices=['srcmac','dstmac','srcip_gre','dstip_gre','srcmac_gre','dstmac_gre'],dest='parameter',
                    help='IXIA capture pkts parameters, such as srcmac/dstmac/srcip_gre/dstip_gre/srcmac_gre/dstmac_gre')

parser.add_argument('-bm', '--beginmac', required=False, default='0000:0000:0001', dest='begin_mac',
                    help='The loop begin mac')

parser.add_argument('-bi', '--beginip', required=False, default='0.0.0.0', dest='begin_ip',
                    help='The loop begin ip')
                    
parser.add_argument('-l', '--loopnum', required=True, default=1, type=int, dest='loop',
                    help='Loop number')                                     

###Define a func of get the parameters not appear/exist and appear times in list_compare
def dic_info(dict_compare_result,info_mode):
    list_not_appear=[]
    list_not_exist=[]
    dict_appear_times={}
    for i_key,i_value in dict_compare_result.items():
        if i_value == 0:
            list_not_appear.append(i_key)
#            print 'Miss the mac entry %s' % i_key
        elif i_value == -1:
            list_not_exist.append(i_key)
#            print 'Not exist the mac entry %s' % i_key
        else:
            dict_appear_times[i_key]=i_value
    if info_mode == 'remove':
        return list_not_exist
    elif info_mode == 'add':
        return list_not_appear
    elif info_mode == 'times':
        return dict_appear_times.items()
    else:
        print '''Not except info mode, please type in "remove/add/times" '''
args = parser.parse_args()
file_path = args.file_path
parameter = args.parameter
begin_mac = args.begin_mac
begin_ip = args.begin_ip
loop = args.loop

###Get the Mac list from IXIA capture pkts files
list_collect=read_ixia_file(file_path,parameter)
#print 'list_collect is %s' % list_collect

if parameter == 'srcmac' or parameter == 'dstmac' or parameter == 'srcmac_gre' or parameter == 'dstmac_gre':
###Generate standard Mac list
    list_standard=mac_range_list(begin_mac,loop)
#print 'list_standard is %s' % list_standard

if parameter == 'srcip_gre' or parameter == 'dstip_gre':
    list_standard=ip_range_list(begin_ip,loop) 

###Compare both lists and get the different, assign the value to a dict
dict_result=list_compare(list_standard,list_collect)
#print 'dict_result is %s' % dict_result
###Get the info of the dict result
list_dic_info=dic_info(dict_result,'add')
#print 'list_dic_info is %s' % list_dic_info
###Print info of the result
if len(list_dic_info)==0:
    print 'All standard entries are in your collect IXIA files'
else:
    for lost_entry in list_dic_info:
        print 'Your collect IXIA files lost the entry %s' % lost_entry 
