#每个接口一个文档
#前后端分离时



### 获取用户信息

### 请求

    GET/user/user/

##### params

   id int 用户id

#### 响应
成功响应：

    {
  "code": 200,
  "data": {
    "avatar": "upload\\TIM\u622a\u56fe20180410155236.png",
    "id": 5,
    "name": "321",
    "phone": "18000581752"
  }
}


失败响应：

    {
	'code': 0,
	'msg': '数据库错误，请稍后重试'
}