import os,re,argparse
from file_oper import get_extension_file

def floattime2strtime(in_time):
    hour =int(in_time/3600)
    min =int((in_time-hour*3600)/60)
    sec =in_time-hour*3600-min*60
    res = '%02d:%02d:%02.3f'%(hour, min, sec)
    return re.sub('\.', ',', res)

def str_lrc_to_srt(in_str, min_app_time= 1.0, spe_time = 0.05):
    time_str = re.findall(r"\[([\d]+):([\d.]+)\]", in_str, flags=re.M)
    timeline = []
    for t in time_str:
        timeline.append([float(t[0])*60+float(t[1]), r'\['+t[0]+':'+t[1]+r'\]'])
    timeline.sort()

    res = ''
    cnt = 1
    timeline_size = len(timeline)
    timeline.append([(timeline[timeline_size-1][0])+10 ,''])
    for i in range(0, timeline_size):
        nw = timeline[i]
        text = re.search(nw[1]+r'(.*)', in_str, flags=re.M)
        str_time = nw[0]
        end_time = max(timeline[i+1][0]-spe_time, str_time + min_app_time)
        res = res + str(cnt) + '\n' + floattime2strtime(str_time) + ' --> ' + floattime2strtime(end_time) + '\n'
        res = res + text.group(1) + '\n\n'
        cnt = cnt + 1

    return res

def file_lrc_to_srt(in_file, min_app_time= 1.0, spe_time = 0.05):
    out_file = os.path.splitext(in_file)[0] + '.srt'
    if (not os.path.isfile(in_file)) or (os.path.splitext(in_file)[-1]).lower() != '.lrc':
        raise Exception("file not exists or not .lrc file")
    if os.path.exists(out_file):
        print('\'%s\' already exists'%out_file)
        return False

    ifile = open(in_file, "r+", encoding='UTF-8')
    in_str = ifile.read()
    ifile.close()
    ret = str_lrc_to_srt(in_str, min_app_time, spe_time)
    ofile = open(out_file, "w+", encoding='UTF-8')
    ofile.write(ret)
    ofile.close()
    print('success : \''+out_file+'\'')
    return True

input_help = '''input file or folder (recursion)'''
apptime_help = '''text minumum appear time, default 1s'''
spetime_help = '''sperate time between adjacent text, default .05s'''

def main():
    parser = argparse.ArgumentParser(description="Command line for lrc_to_srt")
    parser.add_argument('-i','--input', type=str, default='./', required=True, help=input_help)
    parser.add_argument('-apt','--apptime', type=float, default=1.0, required=False, help=apptime_help)
    parser.add_argument('-spt','--spetime', type=float, default=0.05, required=False, help=spetime_help)
    args = parser.parse_args()
    input = args.input
    apptime = args.apptime
    spetime = args.spetime

    file_d = []
    if (os.path.isdir(input)):
        file_d = get_extension_file(input, ['lrc'])
    else:
        file_d.append(input)
    
    fail_list = []
    file_d_size = len(file_d)
    succ = 0
    for file in file_d:
        try:
            succ = succ + file_lrc_to_srt(file, apptime, spetime)
        except BaseException:
            print('fail : \''+file+'\'')
            fail_list.append(file)
    
    if(len(fail_list)==0):
        print('All %d/%d success, %d/%d srt file already exists.'%(succ,file_d_size,file_d_size-succ,file_d_size))
    else:
        print('All done, %d/%d failed.'%(len(fail_list),file_d_size))
        print('failed list:')
        for file in fail_list:
            print (file)

if __name__ == '__main__':
    main()