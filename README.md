# GitHubPoster
Make everything a GitHub svg poster

## 支持
- **[Strava](#strava)**
- **[开心词场](#cichang)**
- **[扇贝](#shanbay)**
- **[Nintendo Switch](#ns)**
- **[GPX](#GPX)**
- **[多邻国](#duolingo)**


## 下载
```
git clone https://github.com/yihong0618/GitHubPoster.git
```
## 安装(Python3.6+)
```
pip3 install -r requirements.txt
```
### GPX

<details>
<summary>Make your <code>GPX</code> GitHub poster</summary>
<br>

把其它软件生成的(like running_page) gpx files 拷贝到 `GPX_FOLDER` 之后运行，或指定文件夹如我的文件夹是 `~/blog/GPX_OUT/`
```python
python3 cli.py --type gpx --gpx-dir ~/blog/GPX_OUT/ --year 2013-2021
```
</details>

### Strava

<details>
<summary>Make your strava GitHub poster</summary>

1. 注册/登陆 [Strava](https://www.strava.com/) 账号
2. 登陆成功后打开 [Strava Developers](http://developers.strava.com) -> [Create & Manage Your App](https://strava.com/settings/api)

3. 创建 `My API Application`   
输入下列信息：
![My API Application](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/strava_settings_api.png)
创建成功：
![](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/created_successfully_1.png)
4. 使用以下链接请求所有权限   
将 ${your_id} 替换为 My API Application 中的 Client ID 后访问完整链接
```
https://www.strava.com/oauth/authorize?client_id=${your_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all,profile:write,activity:write
```
![get_all_permissions](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_all_permissions.png)
5. 提取授权后返回链接中的 code 值   
例如：
```
http://localhost/exchange_token?state=&code=1dab37edd9970971fb502c9efdd087f4f3471e6e&scope=read,activity:write,activity:read_all,profile:write,profile:read_all,read_all
```
`code` 数值为：
```
1dab37edd9970971fb502c9efdd087f4f3471e6
```
![get_code](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_code.png)
6. 使用 Client_id、Client_secret、Code 请求 refresch_token   
在 `终端/iTerm` 中执行：
```
curl -X POST https://www.strava.com/oauth/token \
-F client_id=${Your Client ID} \
-F client_secret=${Your Client Secret} \
-F code=${Your Code} \
-F grant_type=authorization_code
```
示例：
```
curl -X POST https://www.strava.com/oauth/token \
-F client_id=12345 \
-F client_secret=b21******d0bfb377998ed1ac3b0 \
-F code=d09******b58abface48003 \
-F grant_type=authorization_code
```
![get_refresch_token](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_refresch_token.png)

7. 同步数据至 Strava   
在项目根目录执行：
```python
python3 cli.py --type strava --strava_client_id  ${client_id} --strava_client_secret ${client_secret} --strava_refresh_token ${client_secret} --year 2012-2021}
```
