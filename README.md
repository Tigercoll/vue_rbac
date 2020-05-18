# 1.RBAC后台 API 接口文档

## 1.1. API V1 接口说明

- 接口基准地址：`http://127.0.0.1:3000/api/private/v1/`
- 服务端已开启 CORS 跨域支持
- API V1 认证统一使用 Token 认证
- 需要授权的 API ，必须在请求头中使用 `Authorization` 字段提供 `token` 令牌
- 使用 HTTP Status Code 标识状态
- 数据返回格式统一使用 JSON

### 1.1.1. 支持的请求方法

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
- DELETE（DELETE）：从服务器删除资源。
- HEAD：获取资源的元数据。
- OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。

### 1.1.2. 通用返回状态说明

| *状态码* | *含义*                | *说明*                                              |
| -------- | --------------------- | --------------------------------------------------- |
| 200      | OK                    | 请求成功                                            |
| 201      | CREATED               | 创建成功                                            |
| 204      | DELETED               | 删除成功                                            |
| 400      | BAD REQUEST           | 请求的地址不存在或者包含不支持的参数                |
| 401      | UNAUTHORIZED          | 未授权                                              |
| 403      | FORBIDDEN             | 被禁止访问                                          |
| 404      | NOT FOUND             | 请求的资源不存在                                    |
| 422      | Unprocesable entity   | [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误 |
| 500      | INTERNAL SERVER ERROR | 内部错误                                            |
|          |                       |                                                     |



## 1.2. 登录

### 1.2.1. 登录验证接口

- 请求路径：login
- 请求方法：post
- 请求参数

| 参数名   | 参数说明 | 备注     |
| -------- | -------- | -------- |
| username | 用户名   | 不能为空 |
| password | 密码     | 不能为空 |

- 响应参数

| 参数名   | 参数说明    | 备注            |
| -------- | ----------- | --------------- |
| id       | 用户 ID     |                 |
| rid      | 用户角色 ID |                 |
| username | 用户名      |                 |
| mobile   | 手机号      |                 |
| email    | 邮箱        |                 |
| token    | 令牌        | 基于 jwt 的令牌 |



响应数据

```json
{
    "data": {
        "id": 1,
        "rid": 0,
        "username": "测试01",
        "mobile": "123",
        "email": "123@qq.com",
        "token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE1MTI1NDQyOTksImV4cCI6MTUxMjYzMDY5OX0.eGrsrvwHm-tPsO9r_pxHIQ5i5L1kX9RX444uwnRGaIM"
    },
    "meta": {
        "msg": "登录成功",
        "status": 200
    }
}
```

## 1.3. 注册

##### 1.3.1 注册接口

- 请求路径:register
- 请求方法:post
- 请求参数

| 参数名     | 参数说明 | 备注     |
| ---------- | -------- | -------- |
| username   | 用户名   | 不能为空 |
| password   | 密码     | 不能为空 |
| password_2 | 确认密码 | 不能为空 |
| mobile     | 手机号   | 不能为空 |
| email      | 邮箱号   | 不能为空 |

- 响应参数

| 参数名   | 参数说明    | 备注 |
| -------- | ----------- | ---- |
| id       | 用户 ID     |      |
| username | 用户名      |      |
| mobile   | 手机号      |      |
| email    | 邮箱        |      |
| role     | 用户角色 ID |      |

```json
{
    'data':{
        'id': 10,
        'username': '测试0001',
        'mobile': '13812345678',
        'email': '123@qq.com',
        'role': None
    },
      "meta": {
        "msg": "注册成功",
        "status": 201
    }
}
```



## 1.4 用户管理

### 1.4.1. 用户数据列表

- 请求路径：users
- 请求方法：get
- 请求参数

- 

| 参数名   | 参数说明     | 备注     |
| -------- | ------------ | -------- |
| query    | 查询参数     | 可以为空 |
| pagenum  | 当前页码     | 不能为空 |
| pagesize | 每页显示条数 | 不能为空 |

- 响应参数

| 参数名    | 参数说明     | 备注 |
| --------- | ------------ | ---- |
| totalpage | 总记录数     |      |
| pagenum   | 当前页码     |      |
| users     | 用户数据集合 |      |

- 响应数据

```json
{
    "data": {
        "totalpage": 5,
        "pagenum": 4,
        "users": [
            {
                "id": 25,
                "username": "tige117",
                "mobile": "18616358651",
                "email": "tige112@163.com",
                "role_name": "炒鸡管理员"
            }
        ]
    },
    "meta": {
        "msg": "获取成功",
        "status": 200
    }
}
```

### 1.4.2. 添加用户

- 请求路径：users
- 请求方法：post
- 请求参数

| 参数名   | 参数说明 | 备注     |
| -------- | -------- | -------- |
| username | 用户名称 | 不能为空 |
| password | 用户密码 | 不能为空 |
| email    | 邮箱     | 可以为空 |
| mobile   | 手机号   | 可以为空 |

- 响应参数

| 参数名   | 参数说明    | 备注 |
| -------- | ----------- | ---- |
| id       | 用户 ID     |      |
| role     | 用户角色 ID |      |
| username | 用户名      |      |
| mobile   | 手机号      |      |
| email    | 邮箱        |      |

- 响应数据

```json
{
    'meta': {
        'msg': '用户创建成功', 
        'status': 201
    },
    'data': {
        'id': 11,
        'username': '测试0002', 
        'mobile': '13812345678',
        'email': '123@qq.com', 
        'role': None}
}

```

### 1.4.3. 根据 ID 查询用户信息

- 请求路径：users/:id
- 请求方法：get
- 请求参数

| 参数名 | 参数说明 | 备注                  |
| ------ | -------- | --------------------- |
| id     | 用户 ID  | 不能为空`携带在url中` |

- 响应参数

| 参数名  | 参数说明 | 备注 |
| ------- | -------- | ---- |
| id      | 用户 ID  |      |
| role_id | 角色 ID  |      |
| mobile  | 手机号   |      |
| email   | 邮箱     |      |

- 响应数据

```json
{
    'data': {
        'id': 3,
        'username': '测试03', 
        'role_id': 2, 
        'mobile': '13812345678',
        'email': '123@qq.com'
    }, 
    'meta':{
        'msg': '查询成功', 
        'status': 200
    }
}
```

### 1.4.4. 编辑用户

- 请求路径：users/:id
- 请求方法：put
- 请求参数

| 参数名 | 参数说明 | 备注                        |
| ------ | -------- | --------------------------- |
| id     | 用户 id  | 不能为空 `参数是url参数:id` |
| email  | 邮箱     | 可以为空                    |
| mobile | 手机号   | 可以为空                    |

- 响应参数

| 参数名   | 参数说明 | 备注 |
| -------- | -------- | ---- |
| id       | 用户 ID  |      |
| username | 用户名   |      |
| role_id  | 角色 ID  |      |
| mobile   | 手机号   |      |
| email    | 邮箱     |      |

- 响应数据

```json
/* 200表示成功，500表示失败 */
{
    'data': {
        'id': 3,
        'username': '测试03', 
        'role_id': '普通员工', 
        'mobile': '13812345677',
        'email': '123@qq.com'
    },
    'meta': {
        'msg': '更新成功', 'status': 200
    }
}
```

### 1.4.5. 删除单个用户

- 请求路径：users/:id
- 请求方法：delete
- 请求参数

| 参数名 | 参数说明 | 备注                       |
| ------ | -------- | -------------------------- |
| id     | 用户 id  | 不能为空`参数是url参数:id` |

- 响应参数
- 响应数据

```json
{
    "data": null,
    "meta": {
        "msg": "删除成功",
        "status": 200
    }
}
```

### 1.4.6. 分配用户角色

- 请求路径：users/:id/role
- 请求方法：put
- 请求参数

| 参数名 | 参数说明 | 备注                       |
| ------ | -------- | -------------------------- |
| id     | 用户 ID  | 不能为空`参数是url参数:id` |
| rid    | 角色 id  | 不能为空`参数body参数`     |

- 响应参数

| 参数名   | 参数说明 | 备注 |
| -------- | -------- | ---- |
| id       | 用户 ID  |      |
| rid      | 角色 ID  |      |
| username | 用户名   |      |
| mobile   | 手机号   |      |
| email    | 邮箱     |      |

- 响应数据

```json
{
    'data': {
        'id': 3,
        'rid': '4',
        'username': '测试03', 
        'mobile': '13812345677',
        'email': '123@qq.com'
    },
    'meta': {
        'msg': '设置角色成功', 
        'status': 200
    }
}
```

## 1.5. 角色管理

### 1.5.1. 角色列表

- 请求路径：roles

- 请求方法：get

- 响应数据说明

  + 第一层为角色信息

  - 第二层开始为权限说明，权限一共有 3 层权限
  - 最后一层权限，不包含 `children` 属性

- 响应数据

```json
{
    'data': [{
        'id': 1,
        'roleName': '管理员',
        'roleDesc': '管理员', 
        'children': [{
            'id': 1, 
            'authName': '用户管理', 
            'path': 'users', 
            'children': [{
                'id': 2, 
                'authName': '用户列表',
                'path': 'users',
                'pid': 1,
                'children': [{
                    'id': 3,
                    'authName': '添加用户', 
                    'path': 'users',
                    'pid': [1, 2]
                }]}]}]}]}]     
            'meta': {
                'msg': '获取成功', 
                'status': 200
            }
}

```

### 1.5.2. 添加角色

- 请求路径：roles
- 请求方法：post
- 请求参数

| 参数名    | 参数说明 | 备注     |
| --------- | -------- | -------- |
| rolesName | 角色名称 | 不能为空 |
| rolesDesc | 角色描述 | 可以为空 |

- 响应参数

| 参数名   | 参数说明 | 备注 |
| -------- | -------- | ---- |
| roleId   | 角色 ID  |      |
| roleName | 角色名称 |      |
| roleDesc | 角色描述 |      |

- 响应数据

```json
{
    "data": {
        "roleId": 40,
        "roleName": "admin2",
        "roleDesc": "admin2Desc"
    },
    "meta": {
        "msg": "创建成功",
        "status": 201
    }
}
```

### 1.5.3. 根据 ID 查询角色

- 请求路径：roles/:id
- 请求方法：get
- 请求参数

| 参数名 | 参数说明 | 备注                  |
| ------ | -------- | --------------------- |
| :id    | 角色 ID  | 不能为空`携带在url中` |

- 响应参数

| 参数名   | 参数说明 | 备注 |
| -------- | -------- | ---- |
| roleId   | 角色 ID  |      |
| roleName | 角色名称 |      |
| roleDesc | 角色描述 |      |

- 响应数据

```json
{
    "data": {
        "roleId": 31,
        "roleName": "测试角色",
        "roleDesc": "测试负责人"
    },
    "meta": {
        "msg": "获取成功",
        "status": 200
    }
}
```

### 1.5.4. 编辑提交角色

- 请求路径：roles/:id
- 请求方法：put
- 请求参数

| 参数名    | 参数说明 | 备注                  |
| --------- | -------- | --------------------- |
| :id       | 角色 ID  | 不能为空`携带在url中` |
| rolesName | 角色名称 | 不能为空              |
| rolesDesc | 角色描述 | 可以为空              |

- 响应参数

| 参数名   | 参数说明 | 备注 |
| -------- | -------- | ---- |
| roleId   | 角色 ID  |      |
| roleName | 角色名称 |      |
| roleDesc | 角色描述 |      |

- 响应数据

```json
{
    "data": {
        "roleId": 31,
        "roleName": "测试角色",
        "roleDesc": "测试角色描述"
    },
    "meta": {
        "msg": "获取成功",
        "status": 200
    }
}
```

### 1.5.5. 删除角色

- 请求路径：roles/:id
- 请求方法：delete
- 请求参数

| 参数名 | 参数说明 | 备注                  |
| ------ | -------- | --------------------- |
| :id    | 角色 ID  | 不能为空`携带在url中` |

- 响应数据

```json
{
    "data": null,
    "meta": {
        "msg": "删除成功",
        "status": 200
    }
}
```

### 1.5.6. 角色授权

- 请求路径：roles/:roleId/rights
- 请求方法：post
- 请求参数：通过 `请求体` 发送给后端

| 参数名  | 参数说明               | 备注                                                         |
| ------- | ---------------------- | ------------------------------------------------------------ |
| :roleId | 角色 ID                | 不能为空`携带在url中`                                        |
| rids    | 权限 ID 列表（字符串） | 以 `,` 分割的权限 ID 列表（获取所有被选中、叶子节点的key和半选中节点的key, 包括 1，2，3级节点） |

- 响应数据

```json
{
    "data": null,
    "meta": {
        "msg": "更新成功",
        "status": 200
    }
}
```

### 1.5.7. 删除角色指定权限

- 请求路径：roles/:roleId/rights/:rightId

- 请求方法：delete

- 请求参数

  | 参数名   | 参数说明 | 备注                  |
  | -------- | -------- | --------------------- |
  | :roleId  | 角色 ID  | 不能为空`携带在url中` |
  | :rightId | 权限 ID  | 不能为空`携带在url中` |

- 响应数据说明 

  - 返回的data, 是当前角色下最新的权限数据

- 响应数据

  ```json
  {
      "data": [
          {
              "id": 101,
              "authName": "商品管理",
              "path": null,
              "children": [
                  {
                      "id": 104,
                      "authName": "商品列表",
                      "path": null,
                      "children": [
                          {
                              "id": 105,
                              "authName": "添加商品",
                              "path": null
                          },
                          {
                              "id": 116,
                              "authName": "修改",
                              "path": null
                          }
                      ]
                  }
              ]
          }
      ],
      "meta": {
          "msg": "取消权限成功",
          "status": 200
      }
  }
  ```

## 1.6. 权限管理

### 1.6.1. 所有权限列表

- 请求路径：rights/:type
- 请求方法：get
- 请求参数

| 参数名 | 参数说明 | 备注                                                         |
| ------ | -------- | ------------------------------------------------------------ |
| type   | 类型     | 值 list 或 tree , list 列表显示权限, tree 树状显示权限,`参数是url参数:type` |

- 响应参数

| 参数名   | 参数说明     | 备注 |
| -------- | ------------ | ---- |
| id       | 权限 ID      |      |
| authName | 权限说明     |      |
| level    | 权限层级     |      |
| pid      | 权限父 ID    |      |
| path     | 对应访问路径 |      |

- 响应数据 type=list

```json
  {
    "data": [
        {
            "id": 101,
            "authName": "商品管理",
            "level": "0",
            "pid": 0,
            "path": null
        },
        {
            "id": 102,
            "authName": "订单管理",
            "level": "0",
            "pid": 0,
            "path": null
        }
    ],
    "meta": {
        "msg": "获取权限列表成功",
        "status": 200
    }
}
```

type=tree

```json
  {
    data: [
      {
        id: 101,
        authName: '商品管理',
        path: null,
        pid: 0,
        children: [
          {
            id: 104,
            authName: '商品列表',
            path: null,
            pid: 101,
            children: [
              {
                id: 105,
                authName: '添加商品',
                path: null,
                pid: '104,101'
              }
            ]
          }
        ]
      }
    ],
    meta: {
      msg: '获取权限列表成功',
      status: 200
    }
  }
```

### 1.6.2. 左侧菜单权限

- 请求路径：menus
- 请求方法：get
- 响应数据

```json
# 菜单栏其实为1,2级权限.
{
    "data":
        {
            "id": 101,
            "authName": "商品管理",
            "path": null,
            "children": [
                {
                    "id": 104,
                    "authName": "商品列表",
                    "path": null,
                    "children": []
                }
            ]
        }
    "meta": {
        "msg": "获取菜单列表成功",
        "status": 200
    }
}
```



# 2.前端展示文档说明

## 2.1.前端开发语言

主要采用:vue+vue-cli+element-ui完成整体页面布局.

采用axios 发送请求.

## 2.2. 主要组件

register组件:用来完成用户的注册

login组件:用户完成用户的登录

home 组件:主目录组件,也就是首页

users组件:用户管理页面,包括用户的增删改查,以及用户的角色授权操作

roles组件:角色管理组件,角色信息的增删改查,已经角色下的删除权限已经添加权限操作

rights组件:用户展示权限列表,采用tree 形式展示,权限的增删改查还是需要后台接口的配合,所以未做增删改查操作.





