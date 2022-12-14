# HNU-Auto-Clockin

HNU疫情防控和健康监测系统每日自动打卡

## 更新日志

2022.12.14 打卡系统下线，该脚本也下班了，再也不见！

2022.10.16 自动打卡归来，看中特形式主义土崩瓦解，民主自由精神照耀全体人民之日已经到来

2022.3.20 居然提示“请使用微信登录打卡”，可恶。但道高一尺魔高一丈，待研究。

2022.2.24 感谢 [@Mufanc](https://github.com/Mufanc) 同学关于直接在本地识别验证码的commit😂

2021.6.4 使用百度云公开验证码识别OCRapi，不再需要百度账号，此处感谢[GGP](https://github.com/2X-ercha)的提醒。

## 如何使用

把大象塞进冰箱需要几步？

0. **给本项目点Star**

1. **创建一个GitHub账号，将本项目fork到你自己的账号下**
   ![QQ20210316-0.png](https://i.loli.net/2021/03/16/1krc8KwVATBUWCl.png)

2. **配置学号与个人中心密码**

    进入你fork过去的，自己名下的项目，点击Settings -> Secrets页面，再点击New repository Secret，在Name栏输入**USERNAME**，Value栏输入你的学号。然后再添加一个Secret，Name栏为**PASSWORD**，Value栏填写你登录个人中心的密码。
    ![QQ20210316-2.png](https://i.loli.net/2021/03/16/4vqF6bsBPfSUDZc.png)

3. **填写打卡地址**

    你还需要分别以**PROVINCE**, **CITY**, **COUNTY**为NAME添加相应的Secret，Value中请注意须在地名后面添加“省“、”市“、”县/区“，如”湖南省“、”长沙市“、”岳麓区“。另外，详细地址默认为一个句号，你可以在源代码（clock_in.py）中修改。

4. **开始自动化运行**

    进入到**Actions**界面，点击该工作流，然后Run workflow，即可开启自动化运行，你可以在设置里绑定邮箱以接收运行失败的通知。
    ![Snipaste_2021-03-15_21-56-15.png](https://i.loli.net/2021/03/16/oxSp8VYlfskWq53.png)
    ![Snipaste_2021-03-15_21-56-34.png](https://i.loli.net/2021/03/16/xETNukAF8hVS1nw.png)
    ![Snipaste_2021-03-15_21-57-11.png](https://i.loli.net/2021/03/16/XtR6lphCxLQg3an.png)

    你可以在如下界面中检查自动化运行情况：
    ![Snipaste_2021-03-15_21-57-49.png](https://i.loli.net/2021/03/16/8RwnFvq1ZBTuMxe.png)
    ![Snipaste_2021-03-15_21-58-06.png](https://i.loli.net/2021/03/16/MSok2D9VYJOBRK7.png)
    ![image.png](https://i.loli.net/2021/03/16/vnaiPEmyx5ugNlW.png)

    我设定为每天凌晨0:15自动运行，但GitHub的“特性”是运行不准时，通常会延迟到1点左右才启动。你可以在/.github/workflows/python-app.yml文件里修改运行时间，请注意cron语法下的时间为零时区时间，需要将北京时间减8个小时，且分钟在前小时在后。详情参见[POSIX cron 语法](https://crontab.guru/)和[官方文档](https://docs.github.com/cn/actions/reference/events-that-trigger-workflows#)。

**寒暑假离校返校状态切换：进入clockin.py中的main函数改这个IsInCampus的数值就行了**
![Snipaste_2022-01-15_21-32-04.png](https://s2.loli.net/2022/01/15/GHs2EvakgqNlBOn.png)
