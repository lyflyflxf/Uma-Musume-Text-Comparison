# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
# from pdb import set_trace as st


old_dir = r'E:\py\tools\umamonitor\original'
new_dir = r'E:\py\tools\umamonitor\230131'
print_error = 2

os.chdir(new_dir)
count = 0
new_len =0
old_len=0
# new_dict = {}
# old_dict = {}
separators = [r'\\n', '\r\n','\n','\r']
output = ''
message = ''
title_name = "Title"
text_list_name = "TextBlockList"


def publish_error(s: str, option_override = 0):
    global output
    if option_override ==-1:
        return
    if print_error == 1 or option_override ==1:
        print(s)
    elif print_error == 2 or option_override ==2:
        output += s + '\n'


def compare_line(new: str, old: str,option_override =0):
    if new is None or old is None:
        if not (new is None and old is None):
            message = f"新老文本不同时为空。路径：{new_partial_path}"
            publish_error(message)
            return 1
        return 0
    if new != old:
        for separator in separators:
            if isinstance(new,str):
                new = new.replace(separator, '')
            else:
                new = str(new)
            if isinstance(old,str):
                old = old.replace(separator, '')
            else:
                old = str(old)
        if new != old:
            alert = f'文本有变化的文件路径：{new_partial_path}:\n当前文本:{new}' \
                    f'\n既往文本:{old}'
            # for k in range(len(new)):
            #     if new[k]!=old[k]:
            #         st()
            publish_error(alert,option_override)
            return 1
        else:
            return 0
    return 0


for root, dirs, files in os.walk(r"."):
    for file in files:
        new_partial_path = os.path.join(root, file)
        old_path = os.path.join(old_dir, new_partial_path)
        if count == 1:
            break

        # 检查是否有新文件
        if not os.path.isfile(old_path):
            # new_path = os.path.join(new_dir, new_partial_path)
            message = f'新文件:{new_partial_path}'
            # publish_error(message)
            continue
        # 判断相同文件名的文本是否完全相同。如果不同，则去掉换行符，再次比较。如果仍不同，则显示文件名和新旧内容
        old_json = json.load(open(old_path, 'r', encoding='utf-8'))
        new_json = json.load(open(new_partial_path, 'r', encoding='utf-8'))
        # print(new_partial_path)
        # print(new_json)
        if isinstance(new_json, list):
            new_len = len(new_json)
            old_len = len(old_json)
            if new_len != old_len:
                message = f"文本有变化的文件路径：{new_partial_path}\n新老文件的行数差为{new_len - old_len}。"
                publish_error(message)

            for i in range(min(new_len, old_len)):
                new_line = new_json[i]
                old_line = old_json[i]
                compare_line(new_line, old_line)
        elif isinstance(new_json, dict):
            new_name = new_json[title_name]
            old_name = old_json[title_name]
            if new_name != old_name:
                message = f'文本名称有变动。新名称：{new_name}  老名称：{old_name}'
                publish_error(message)
            new_len = len(new_json[text_list_name])
            old_len = len(old_json[text_list_name])
            if new_len != old_len:
                message = f"文本有变化的文件路径：{new_partial_path}\n新老对话的行数差为{new_len - old_len}。"
                publish_error(message)
            for i in range(min(new_len, old_len)):
                new_dict = new_json[text_list_name][i]
                old_dict = old_json[text_list_name][i]
                if new_dict is None or old_dict is None:
                    if not (new_dict is None and old_dict is None):
                        message =f"新老文本不同时为空。路径：{new_partial_path}"
                        publish_error(message)
                    continue
                for key in new_dict.keys():
                    if compare_line(new_dict[key], old_dict[key]) !=0:
                        message = f"文本块变更。路径：{new_partial_path}\n新块：{str(new_dict)}\n老块：{str(old_dict)}"
                        publish_error(message)
                        break

with open(r"E:\py\tools\umamonitor\output.txt",'w',encoding='utf-8') as f:
    f.write(output)