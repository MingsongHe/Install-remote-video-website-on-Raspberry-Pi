<!doctype html> 
<html> 
<head> 
<meta charset="UTF-8"> 
<title>正在修改密码</title> 
</head> 
<body> 
 <?php
 session_start (); //开启会话
 $username = $_REQUEST ["username"]; 
 $oldpassword = $_REQUEST ["oldpassword"]; 
 $newpassword = $_REQUEST ["newpassword"]; 
 $dbusername = null; 
 $dbpassword = null;

 $link = mysqli_connect('localhost','root','30189');
   if (!$link) {
       exit('数据库链接失败！');
   }
   mysqli_set_charset($link , 'utf8');
   mysqli_select_db($link,'iot_v50');
    $sql = "select * from user where name = '$username'";
    $res = mysqli_query($link , $sql);
    $row = mysqli_fetch_array($res);  //用mysqli_fetch_array($res);，下面用$row ["name"];或者$row [1];都可以，但是用mysqli_fetch_row($res);，下面只能用$row ["name"];
    $dbusername = $row ["name"]; 
    $dbpassword = $row ["password"]; 

 if ( $dbusername == "" ) { 
    mysqli_close ( $link );
 ?> 
 <script type="text/javascript"> 
 alert("用户名错误!"); 
 window.location.href="alter_passw.html"; 
 </script> 
 <?php
 } 
 if ($oldpassword != $dbpassword) { 
    mysqli_close ( $link );
 ?> 
 <script type="text/javascript"> 
 alert("密码错误!"); 
 window.location.href="alter_passw.html"; 
 </script> 
 <?php
 } 
 
 //如果上述用户名密码判定不错，则update进数据库中 
 $sql = "update user set password='$newpassword' where name='$username'";
 $res = mysqli_query($link , $sql);
 
 mysqli_close ( $link ); 
 ?> 
<script type="text/javascript"> 
 alert("密码修改成功"); 
 window.location.href="http://192.168.1.172/";
 window.location.href="http://192.168.1.172/"; 
 </script> 
</body> 
</html> 
