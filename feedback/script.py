import sys
import json
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", type=str, required=True)
    args = parser.parse_args()
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    output_path = args.output_path
    assert output_path.endswith('.jsonl'), "output path should be a jsonl file!"
    dirname, filename = os.path.split(output_path)
    if dirname != '' and not os.path.exists(os.path.split()[0]):
        os.makedirs(dirname)
    f = open(output_path, 'a')
    data = []
    while True:
        d = {}
        print(OKBLUE + "自动生成代码（整文件）" + OKCYAN + "（换行后Windows输入ctrl+Z或Linux输入ctrl+D以结束输入）" + ENDC)
        _input = ''.join(sys.stdin.readlines())
        d['generated_code'] = _input
        num = int(input(OKBLUE + "生成质量打分（0-5）" + ENDC))
        assert num in range(6), "打分应在0-5范围内！"
        d['rating'] = num
        print(OKBLUE + "编译或运行错误信息" + OKCYAN + "（换行后Windows输入ctrl+Z或Linux输入ctrl+D以结束输入）" + ENDC)
        _input = ''.join(sys.stdin.readlines())
        d['error'] = _input
        num = int(input(OKBLUE + "修正所需时间（分钟）：" + ENDC))
        d['correct_min'] = num
        print(OKBLUE + "修正后代码（整文件）" + OKCYAN + "（换行后Windows输入ctrl+Z或Linux输入ctrl+D以结束输入）" + ENDC)
        _input = ''.join(sys.stdin.readlines())
        d['right_code'] = _input
        valid = True
        for k in d:
            if isinstance(d[k], str):
                d[k] = d[k].replace('\x1a', '').replace('\x04', '').replace('\t', "    ").rstrip()
                if d[k].strip() == '':
                    print(WARNING + f"{k}项为空，请检查输入" + ENDC)
                    valid = False
                    break
        if not valid:
            continue
        data.append(d)
        f.write(json.dumps(d) + '\n')
        f.flush()
        print(OKGREEN + f"你完成了{len(data)}条数据。" + ENDC)
