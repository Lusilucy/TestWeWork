# 企业微信项目
- 概要：本项目为企业微信项目测试实战(以通讯录管理的子功能成员管理为例)
```shell
# 测试前请先配置python环境
pip install -r requirements.txt
```
## 1）功能测试案例
- xmind完整版：[企业微信测试案例](testcases/功能测试案例/企业微信测试案例.xmind)
- 转换csv导入jira版：
  - [案例导入-api](testcases/功能测试案例/企业微信测试案例导入-api.csv)
  - [案例导入-web](testcases/功能测试案例/企业微信测试案例导入-web.csv)
  - [案例导入-app1](testcases/功能测试案例/企业微信测试案例导入-app1.csv)
  - [案例导入-app2](testcases/功能测试案例/企业微信测试案例导入-app2.csv)

## 2）Jira测试管理平台
### 1、案例管理

- 案例配置
  - 案例导入格式转换代码：[xmind转csv代码](testcases/功能测试案例/xmind_csv.py)
  - jira案例导入配置文件：[jira导入配置](testcases/功能测试案例/jira导入案例配置文件.txt)
  
- 平台：
  - 模块及案例数：
  ![img_23.png](images/img_23.png)
  - 案例详情
  ![img_20.png](images/img_20.png)
  - 测试案例工作流
  ![img_21.png](images/img_21.png)
  - 测试案例创建界面
  ![img_22.png](images/img_22.png)
    
### 2、Bug管理
- 平台：
  - Bug详情
  ![img_24.png](images/img_24.png)
  - Bug工作流
  ![img_25.png](images/img_25.png)
  - Bug创建界面
  ![img_26.png](images/img_26.png)

## 3）项目代码
- github:[TestWeWork](https://github.com/Lusilucy/TestWeWork)

[comment]: <> (- gitee:[TestWeWork]&#40;&#41;)

### *项目导览*
- **1、数据：**[datas](datas)
  - 系统配置数据：[conf_data](datas/conf_data)
  - 测试数据：[test_data](datas/test_data)
  
- **2、日志：**[logs](logs)
  - api:[apitest](logs/apitest.log)
  - app:[apptest](logs/apptest.log)
  - web:[webtest](logs/webtest.log)

- **3、页面：**
  - 公共方法：[base](pages/base.py)
    
  - 异常封装：[myerror](pages/myerror.py)
    
  - API：[API](pages/API)
    - api公共方法：[api](/pages/API/api.py)
    - wework公共方法：[wework](/pages/API/wework_api.py) *获取access_token*
    - 成员接口：[user](pages/API/user_api.py)
    - 部门接口：[department](pages/API/department_api.py)
    
  - App：[App](pages/API)
    - app公共方法：[app](pages/App/app.py)
    - 主页：[main_page](pages/App/main_page.py)
    - 消息：[message_page](pages/App/message_page)
    - 通讯录：[contact_page](pages/App/contact_page)
    - 工作台：[workbench_page](pages/App/workbench_page)
    - 我：[me_page](pages/App/me_page)
    
  - Web：[Web](pages/Web)
    - web公共方法：[web](pages/Web/web.py)
    - 登录页：[login_page](pages/Web/login_page.py)
    - 复用浏览器启动shell：[launch_chrome](pages/Web/launch_chrome.sh)
    - 首页：[index_page](pages/Web/index_page)
    - 通讯录：[contact_page](pages/Web/contact_page)
    - 应用管理：[apps_page](pages/Web/apps_page)
    - 客户联系：[custormer_page](pages/Web/customer_page)
    - 管理工具：[manageTools](pages/Web/manageTools_page)
    - 我的企业：[profile_page](pages/Web/profile_page)
    - 页面资源：[page_source](pages/Web/page_source)
  
- **4、测试案例：**
  - API：[api](testcases/api)
    - 测试【成员】功能案例[user](testcases/api/test_user_api.py)
    - 测试【部门】功能案例[department](testcases/api/test_department_api.py)
    
  - App：[app](testcases/app)
    - 测试【成员】功能案例[member](testcases/app/test_member_app.py)
    
  - Web：[web](testcases/web)
    - 测试【成员】功能案例[member](testcases/web/test_member_web.py)
  
  - 压测：[stress](testcases/stress)
    - jmeter压测脚本：[jmeter](testcases/stress/TestWeWork.jmx)
    - 自动化测试bash脚本：[bash](testcases/stress/auto_stress_test.sh)
  
  - 功能测试案例（文本）：
    - xmind：[企业微信测试案例](testcases/功能测试案例/企业微信测试案例.xmind)
    - xmind转csv工具：[xmind_csv](testcases/功能测试案例/xmind_csv.py)

- **5、工具：**[utils](utils/utils.py)
  - *封装解析yaml,json；fake数据等工具类方法*

- **6、其他：**
  - 导览：[Readme](readme.md)
  - 配置python库：[requirements](requirements.txt)



## 3）Jenkins持续集成
  ![img_12.png](images/img_12.png)
### 1、API
- 平台
  ![img_7.png](images/img_7.png)
  ![img_18.png](images/img_18.png)
- 预警提示
  ![img.png](images/img.png)
- 测试报告
  ![img.png](images/img_2.png)
  ![img_19.png](images/img_19.png)
  
### 2、App
- 平台
  - **打包构建app**
  ![img_1.png](images/img_1.png)
  ![img_13.png](images/img_13.png)
  - **测试app**
  ![img_5.png](images/img_5.png)

- 预警提示
  ![img_4.png](images/img_4.png)
  ![img_6.png](images/img_6.png)

- 测试报告
  ![img_3.png](images/img_3.png)
  
### 3、Web
- 平台
  ![img_8.png](images/img_8.png)
  
  - **可进行无界面运行**
  ![img_11.png](images/img_11.png)
  
- 预警提示
  ![img_10.png](images/img_10.png)

- 测试报告
  ![img_17.png](images/img_17.png)
  ![img_9.png](images/img_9.png)

### 4、压测
- 平台
  ![img_14.png](images/img_14.png)
- 预警提示
  ![img_15.png](images/img_15.png)
- 测试报告
  ![img_16.png](images/img_16.png)




