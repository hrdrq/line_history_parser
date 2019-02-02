# encoding: utf-8
import sys
import os
import re

result = []
mate_name = None

def read_file (file_path):
    f = open(os.path.expanduser(file_path))
    # 最初の３行の処理
    # 例：
    # #1 [LINE] あやことのトーク履歴
    # #2 保存日時：2019/02/02 15:12
    # #3
    line = f.readline()
    global mate_name
    match = re.search(r'\[LINE\] (.*)とのトーク履歴' , line)
    mate_name = match.group(1)
    for _ in range(2):
        next(f)
    while line:
        parse_line(line, f)
        line = f.readline()
    f.close

def parse_line (line, f):
    if line == "\n":
        return
    elif re.search(r'^\d{4}\/\d{2}\/\d{2}\([日月火水木金土]\)$' , line):
        result.append({
            "type": "date",
            "content": line.replace('\n', '')
        })
    else :
        match = re.search(r'^(\d{2}:\d{2})\t(.+)\t(.+)$' , line)
        if match:
            if match.group(2) == mate_name:
                who = "mate"
            else:
                who = "me"
            text = match.group(3)
            # 複数行の場合
            if re.search(r'^"' , text):
                # 最初の「"」を消す
                content = text[1:]
                while 1:
                    text = f.readline()
                    content += text
                    if re.search(r'"$' , text):
                        # 最後の「"」と改行を消す
                        content = content[:-2]
                        break
            else:
                content = text.replace('\n', '')
            result.append({
                "type": "text",
                "who": who,
                "content": content,
                "time": match.group(1)
            })

def output_html ():
    body = ""
    for r in result:
        if r["type"] == "date":
            body += '<div class="date">{content}</div>'.format(content=r["content"])
        else:
            body += '<div class="text {who}">{content}</div><div class="time {who}">{time}</div>'.format(who=r["who"], time=r["time"], content=r["content"])
    res_html = "<html><head><title>{title}</title><link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"></head><body>{body}</body></html>" \
    .format(title=mate_name, body=body)
    f = open("{}.html".format(mate_name), "w")
    f.write(res_html)
    f.close

# 例：python main.py "~/Downloads/[LINE] あやことのトーク.txt"
if __name__ == '__main__':
    argvs = sys.argv
    file_path = argvs[1]
    read_file (file_path)
    output_html()