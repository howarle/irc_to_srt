# lrc_to_srt
porting lrc file to srt file

将lrc歌词字幕转为srt字幕，

由于lrc歌词字幕只指定了文本的出现时间，而srt字幕需要指定文本的出现、消失时间，
因此转化时，默认将当前文本消失时间定为下一条文本的出现时间。

## 使用
`lrc2srt.py -i INPUT_FILE_OR_FLODER`

## 参数
|  参数   | 说明 |
|  ----  | ----  |
| -i INPUT, --input INPUT  | 输入的lrc文件或文件夹，默认递归遍历文件夹 |
| -apt APPTIME, --apptime APPTIME  | 文本最小出现时间 ，默认1s|
| -spt SPETIME, --spetime SPETIME  | 相邻文本间隔时间，默认0.05s |

