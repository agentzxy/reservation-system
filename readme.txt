home_page.html是首页，有团体预约和个人预约
group_contact和single_contact分别是填写团体信息和个人信息的页面，表单提交给g_recordings或者s_recordings
g_recordings或者s_recordings是显示表单提交的内容，通知已成功预约
group_forms和single_forms是表单的主要内容

目前已经将single的表单内容传入数据库
还需要做的事是将剩余表单的数据传入数据库，并且从数据库中获取当前时间段预约人数，如果超出规定人数，则不能预约该时间段
并且还要能从mysql中获取数据，将数据显示在页面中，以便工作人员观察


2019.11.18 00:30
已经将表单数据传入数据库了，但是具体时间段无法传入，并且取消预约时，输入的cell返回值为none

2019.11.18 13:37
已经成功将个人预约的表单所有数据传入数据库，并且也可以取消预约了，接下来要将group的表单传入，并且取消预约要分为single和group

2019.11.18 20:27
团体预约和个人预约都已经ok，剩余的任务就是限制预约人数，传入的date在数据库中搜索，如果超过一定数量，就弹出flash，写该时间段已人满，
并且重新返回填表页面

2019.11.19 11:37
增加用户登录注册功能，利用邮箱注册，发送邮件一个验证码，用户名和密码，将用户信息传入用户数据库。个人预约，团体预约都将在用户里面，
增加一个用户查看预约记录，与个人预约，团体预约为同一层次界面

2019.11.20 21:28
增加了用户登录功能，注册功能还未完善，学习redius数据库，注册完毕后跳转注册成功页面，上面写返回首页登陆，然后就可以与前面接上了，
希望之后加的功能还有记录cookies

2019.11.21 16:50
用户登录功能已经ok，注册有点问题，登陆完后，将取消预约改为查看您的预约记录，跳转到个人预约记录页面，页面通过访问数据库，数据库将nickname为
该用户的都选出来，呈现在页面上，每条记录旁边有个取消按钮，如果点击则删除数据库的该条记录，由nickname和手机号选出

2019.11.22 17:08
用户登录后分为团体预约和个人预约，预约记录直接显示，主要问题是如何把用户名进行传递

2019.11.24 15:40
用户已经可以成功登录，并且用户名参数可以传递，剩余工作是在home_page里面加入取消的按键，然后登录添加一个管理员登录，最后完善注册功能