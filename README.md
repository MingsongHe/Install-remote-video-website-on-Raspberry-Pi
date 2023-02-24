# Install-remote-video-website-on-Raspberry-Pi
选择网站sap的主题sbalab，主题复制到树莓派的/var/www/html/wp-content/themes目录下后，
将主题名字改为templates，解压缩，并将自动生成的主题目录名也改为templates
在themes目录下放置文件
camera_pi.py</BR>
iot_v50_p_c.py
start-video.py
stop-video.py
在templates目录下，放置文件：
alter_passw.html
alter_passw.php
index_v50_cn.html
index_v50_us.html
login_cn.html
login_us.html
使用终端启动 Python 3 脚本（需要键盘输入，外部IO的程序？）
在目录 /home/pi/.config/lxsession/LXDE-pi/
下的autostart文件
nano /home/pi/.config/lxsession/LXDE-pi/autostart
代码如下：
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@lxterminal -e python3 /var/www/html/wp-content/themes/start-video.py

网站英文/中文主页面程序尾加代码：
主页面效果如附图1。

建立新页面： 远程视频和控制
页面程序（用html)：
<div class="aspect-ratio">
  <iframe src="http://192.168.1.172:8001/cn" frameborder="0"></iframe>
</div>
加custom CSS
/* 这个规则规定了iframe父元素容器的尺寸，我们要去它的宽高比应该是 25:14 */
.aspect-ratio {
  position: relative;
  width: 100%;
  height: 0%;
  padding-bottom: 64%; /* 高度应该是宽度的64% （960x610) */
}

/* 设定iframe的宽度和高度，让iframe占满整个父元素容器 */
.aspect-ratio iframe {
  position: absolute;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
}

效果见附图2
完善菜单。菜单点击，用户名：Admin,  密码 30189，输入验证码
进入 远程视频和控制页面。
