# my-first-pop

本python3脚本仅适用于闽南师范大学学生疫情信息采集系统的自动化提交
需要手动网页填写过一次信息，之后脚本自动提交
网址：http://dxg.mnnu.edu.cn/SPCP/Web/
依赖：urllib bs4 http.cookiejar apscheduler

修改脚本中的学号和密码即可
#txtUid： 学号   txtPwd： 密码
linux 系统后台执行命令
nohup python -u mnnu_post.py > out.log 2>&1 &
python2版本未测试！
