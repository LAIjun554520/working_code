## studio performance test

from version: studio2.1.0

当前内容：

1. workflow性能测试
python3 studio_performance.py -c per_exec_basic_change_4 -t online  -a n -k workflow  
ps；-c用例，用例名称就是yml文件名
2. tdt性能测试
3. catalog性能测试


使用方式：

1. python studio_performance.py -h 获取命令参数
2. 执行时需要配置conf文件，写入环境及用户密码信息