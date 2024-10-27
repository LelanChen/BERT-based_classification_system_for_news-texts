#!/usr/bin/python
# -*- encoding:utf-8 -*-

'''
通过正则工具去除html标签，同时去除英文和表情符号，只保留中文、数字和有用的字符
之后通过replace（）去除多余空格
最后将繁体全部转换成中文简体
'''
import re
from opencc import OpenCC

def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<![CDATA[[^>]*//]]>',re.I) #匹配CDATA
    re_script=re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>',re.I)#Script
    re_style=re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>',re.I)#style
    re_br=re.compile('<brs*?/?>')#处理换行
    re_h=re.compile('</?w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line=re.compile('n+')
    s=blank_line.sub('n',s)
    s=replaceCharEntity(s)#替换实体
    return s
##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
                'lt':'<','60':'<',
                'gt':'>','62':'>',
                'amp':'&','38':'&',
                'quot':'"','34':'"',}

    re_charEntity=re.compile(r'&#?(?P<name>w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如>
        key=sz.group('name')#去除&;后entity,如>为gt
        try:
            htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz=re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr=re_charEntity.sub('',htmlstr,1)
            sz=re_charEntity.search(htmlstr)
    return htmlstr
def repalce(s,re_exp,repl_string):
    return re_exp.sub(repl_string,s)


def clean_character(sentence):
    pattern = re.compile("[^\u4e00-\u9fa5^0-9^,^。^！^？^（^）^《^》^：]")  #只保留中文、数字和有用的字符，去掉其他东西
    line=re.sub(pattern,'',sentence)  #把文本中匹配到的字符替换成空字符
    # 去掉前面是垃圾的话
    pattern_del_start = r'^（原文链接）|（作者）|更多相关资讯请关注：|原标题|出品|作者|编辑'
    line = re.sub(pattern_del_start, '', line)
    new_sentence=''.join(line.split())    #去除空白
    return new_sentence


def Simplified(sentence):
    new_sentence = OpenCC('t2s').convert(sentence)   # 繁体转为简体
    return new_sentence

def data_cleaning(content):
    #str1=filter_tags(content) #去除HTML标签
    str2=clean_character(content)
    str3=Simplified(str2)
    return str3


