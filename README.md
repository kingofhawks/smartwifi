smartwifi

开发环境:
从以下链接下载python2.7 distribution
http://continuum.io/downloads
$cd smartwifi
$python manage.py runserver
127.0.0.1:8000/accounts/login
default admin user:admin/11111

TODO:
1. use adminLTE template from http://www.almsaeedstudio.com/

=============
总体
服务器web系统可以参考
RippleOS云端管理界面http://my.rippletek.com/users/sign_in
协成广告界面 http://www.wifiadv.com/index.php/index/index/log.html
服务器后端采用django+mysql，前端采用bootstrap框架

代码一定要写得优雅！

在开发过程中，会在bitbucket上建立一个仓库，每天或者每两天同步代码

系统登录用户分为3中角色：系统管理员、代理商、商户。系统管理员可以管理代理商和商户，代理商可以管理下属的商户，商户可以管理自己下面的网关
登录时，登录页面会选择是登录为那种类型，不同类型展示的内容有区别，如系统管理员能看到代理商管理，而普通用户就不能看到
服务器内部数据库
	系统管理员表 sysadmin
登录的用户分为超级管理员（可以添加管理员和设置管理员密码），普通管理员admin，管理员可以添加代理商和普通商户
管理员属性：管理员用户名username，管理员密码password（MD5存放），是否超级管理员superadmin，联系电话phone，QQ号码qq，邮箱mail，是否覆盖所有login广告override_ad1，ad1广告模版ad1，是否覆盖所有等待验证码广告override_ad2，ad2广告模版ad2，是否覆盖所有跳转广告override_ad3，ad3广告模版ad3，是否覆盖SSID，SSID，短信模板smstemp，备注comment
系统管理员配置的广告设置如果配置为覆盖，则下级代理商和商户对应广告设置不生效
	代理商表agent
代理商可以添加商户
代理商属性：代理商用户名username，代理商全称fullname，密码password(MD5存放)，联系电话phone，联系QQ号码qq，邮箱mail，是否覆盖所有login广告override_ad1，ad1广告模版ad1，是否覆盖所有等待验证码广告override_ad2，ad2广告模版ad2，是否覆盖所有跳转广告override_ad3，ad3广告模版ad3，是否覆盖SSID，SSID，短信模板smstemp，备注comment
代理商可以管理属下的商户和网关
代理商配置的广告设置如果配置为覆盖，则下级商户对应广告设置不生效
	商户表customer
商户属性：商户用户名username,全名fullname，所属代理商名agent，密码（MD5存放），联系电话phone，联系QQ号qq，邮箱mail，短信模板smstemp，备注comment
商户可以管理属下的网关配置
	网关表gateway
网关属性：网关ID，网关所属商户customer，mac地址
	用户表
表示曾经或者正在登录到网关进行上网的用户
用户属性：用户名username（可选），手机号phone，mac地址，上网时的IP地址ipaddr，微信号weixin，微博号weibo，备注comment，上次登录时间lastlogin，自上次登录以来的累计发送流量cur_send_bytes，自上次登录以来的累计接收流量cur_recv_bytes，该用户总的发送流量total_send_bytes，该用户总的接收流量total_recv_bytes，该用户当前token（用于用户登录认证），
	广告表ad
决定了每个网关要展示的广告
属性：广告adid，广告图片adimg，广告文字adtext
	广告统计表adstat
记录每个广告被展示的时间
属性：adid，showtime
	公告表notice
每个用户登录到系统时，会从web界面上看到的对自己的公告和消息
属性：公告id，公告内容content，公告对象target，公告是否被处理
系统管理员可以向所有代理商和商户，代理商可以向下属商户下发公告

短信模板
用户网关做的登录短信验证时，对客户发送短信的模版，格式如
你的验证码是[XXXXXX]，有一点科技，[]里面为验证码
短信模板如果网关有设置，则使用网关的，或者商户有设置，则使用商户的，依次类推。

系统对外接口
系统对外部网关接入提供4个接口
/api/login，该接口用于网关上的客户登录时展示登录界面，可以参考

/api/auth，该接口用于网关向服务器认证，可以参考


/api/ping网关定时向服务器发送该消息，服务器应当会送Pong，可以参考

/api/portal用户认证成功后被定向到的页面，可以参考


系统要提供的功能
系统管理员管理（系统管理员可见）
代理商管理（系统管理员可见）
商户管理（系统管理员和代理商可见）
网关管理（系统管理员，代理商，商户可见，但是范围不同）
广告配置
广告统计和曲线
网关流量和曲线
用户查询和导出
公告管理
多浏览器支持

