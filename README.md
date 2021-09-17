# GitHubPoster
Make everything a GitHub svg poster and [skyline](https://skyline.github.com/)!

简体中文 | [English](https://github.com/yihong0618/GitHubPoster/blob/main/README-EN.md)

## 直接引入 `svg` 在 `README` 中的例子

![](https://github.com/yihong0618/GitHubPoster/blob/main/examples/issue.svg)

## Skyline
![image](https://user-images.githubusercontent.com/15976103/120966953-80d07180-c799-11eb-8769-92554905ab3f.png)

## Circular
![](https://github.com/yihong0618/GitHubPoster/blob/main/examples/strava_circular.svg)



## 支持
- **[Strava](#strava)**
- **[开心词场](#cichang)**
- **[扇贝](#shanbay)**
- **[Nintendo Switch](#ns)**
- **[GPX](#GPX)**
- **[多邻国](#duolingo)**
- **[Issue](#Issue)**
- **[Twitter](#Twitter)**
- **[YouTube](#Youtube)**
- **[Bilibili](#Bilibili)**
- **[GitHub](#GitHub)**
- **[GitLab](#GitLab)**
- **[Kindle](#Kindle)**
- **[WakaTime](#WakaTime)**
- **[Dota2](#Dota2)**
- **[Nike](#Nike)**
- **[Garmin](#Garmin)**
- **[Multiple](#Multiple)**


## 下载
```
git clone https://github.com/yihong0618/GitHubPoster.git
```
## pip 安装

```
pip3 install -U github_poster
```

## 安装(Python3.6+)
```
pip3 install -r requirements.txt
```

## 使用

- 不同类型按下方指定的使用方式
- 可以指定年份如 --year 2021, (default) 或年份区间 2012-2021
- 生成的 svg 在 `OUT_FOLDER` 内, 用 type 命名（暂时）
- 默认自动生成不同颜色需要的 number（特殊颜色）, 也可以指定如： --special-number1 10 -- special_number2 20
- 也可以指定颜色： --special-color1 pink --special-color2 '#33C6A4'
- 其它参数可以见 `python3 -m github_poster <type> --help`
- 可以增加动画 --with-animation (加入 GOGOGO 动画), 可以控制动画时间 --animation-time 14（默认是 10s）
- 可以增加 Skyline --with-skyline (默认生成的为 to_year), 可以使用 --skyline-with-name 将用户名打印在 skyline 上
- 支持 circular svg 配合动画 --is-circular

### GPX

<details>
<summary>Make your <code>GPX</code> GitHub poster</summary>
<br>

把其它软件生成的(like running_page) gpx files 拷贝到 `GPX_FOLDER` 之后运行，或指定文件夹如我的文件夹是 `~/blog/GPX_OUT/`
```
python3 -m github_poster gpx --gpx_dir ~/blog/GPX_OUT/ --year 2013-2021
or pip
github_poster github_poster gpx --gpx_dir ~/blog/GPX_OUT/ --year 2013-2021
```
</details>

### Strava

<details>
<summary>Make your <code>Strava</code> GitHub poster</summary>

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
6. 使用 `Client_id`、`Client_secret`、`Code` 请求 `refresch_token`
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

7. 同步数据至 `Strava`
在项目根目录执行：
```
python3 -m github_poster --strava_client_id  ${client_id} --strava_client_secret ${client_secret} --strava_refresh_token ${refresh_token} --year 2012-2021
or pip
github_poster --strava_client_id  ${client_id} --strava_client_secret ${client_secret} --strava_refresh_token ${refresh_token} --year 2012-2021
```
</details>

### NS

<details>
<summary>Make your <code>Nintendo Switch</code> GitHub poster</summary>
<br>

需要下载 `家长控制那个 APP(Nintendo Switch Parent Controls)` 进行抓包（可以使用 mitmproxy 等抓包软件）

```
python3 -m github_poster ns --ns_session_token ${session_token} --ns_device_id ${device_id} --year 2020-2021
or pip
github_poster ns --ns_session_token ${session_token} --ns_device_id ${device_id} --year 2020-2021
```
</details>

### 开心词场

<details>
<summary>Make your <code>开心词场</code> GitHub poster</summary>
<br>

需要填写开心词场的账号和密码

```
python3 -m github_poster cichang --cichang_user_name ${user_name} --cichang_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618
or
github_poster cichang --cichang_user_name ${user_name} --cichang_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618
```
</details>

### 多邻国

<details>
<summary>Make your <code>多邻国（duolingo）</code> GitHub poster</summary>
<br>

需要找到你的多邻国 id, 从网页抓 xhr 就可以获得如下图
![image](https://user-images.githubusercontent.com/15976103/116336188-baad7000-a80a-11eb-80d7-033d4bf0f260.png)


```
python3 -m github_poster duolingo --duolingo_user_name ${user_id} --year 2015-2021
or
github_poster duolingo --duolingo_user_name ${user_id} --year 2015-2021
```
</details>

### 扇贝

<details>
<summary>Make your <code>扇贝（shanbay）</code> GitHub poster</summary>
<br>

需要找到你的扇贝 user_id, 从网页抓 xhr 就可以获得如下图
![image](https://user-images.githubusercontent.com/15976103/116340351-a02ac500-a811-11eb-938f-72ff141e4942.png)


```
python3 -m github_poster shanbay --shanbay_user_name ${user_name} --year 2012-2021 --special-color1 '#33C6A4' --special-color2 '#33C6A4'
or
github_poster shanbay --shanbay_user_name ${user_name} --year 2012-2021 --special-color1 '#33C6A4' --special-color2 '#33C6A4'
```
</details>

### Issue

<details>
<summary>Make your <code>Issue</code> GitHub poster</summary>
<br>

可以参考我的 [issue](https://github.com/yihong0618/2021/issues/5)

```
python3 -m github_poster issue --issue_number ${issue_number} --repo_name ${repo_name} --github_token ${github_token}
or
github_poster issue --issue_number ${issue_number} --repo_name ${repo_name} --github_token ${github_token}
```
</details>

### LeetCode

<details>
<summary>Make your <code>LeetCode </code> GitHub poster</summary>
<br>

需要找到你 `LeetCode` 的 `cookie`

```
python3 -m github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021
or
github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021
```
如果使用的是 leetcode-cn（leetcode 中国需要加上参数）--cn

```
python3 -m github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021 --cn
or
github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021 --cn
```
</details>

### Twitter

<details>
<summary>Make your <code>Twitter </code> GitHub poster</summary>
<br>

需要找到你的 `Twitter user_id`, 网址里那个就是

```
python3 -m github_poster twitter --twitter_user_name ${user_name} --year 2018-2021 --track-color '#1C9CEA'
or
github_poster twitter --user_name ${twitter_user_name} --year 2018-2021 --track-color '#1C9CEA'
```
</details>

### Youtube

<details>
<summary>Make your <code>YouTube </code> GitHub poster</summary>
<br>

利用 Google 的[历史下载](https://takeout.google.com/settings/takeout)下载 `YouTube` 的历史数据，选择 `json` 格式，将 `watch-history.json` 拷贝到 `IN-FOLDER` 然后运行

```
python3 -m github_poster youtube --year 2015-2021
or
github_poster youtube --year 2015-2021
```
</details>

### Bilibili

<details>
<summary>Make your <code>Bilibili </code> GitHub poster</summary>
<br>

需要找到你 `Bilibili (XHR)` 的 `cookie`

```
python3 -m github_poster bilibili --bilibili_cookie "${bilibili-cookie}"
or
github_poster bilibili --bilibili_cookie "${bilibili-cookie}"
```
</details>

### GitHub

<details>
<summary>Make your <code>GitHub </code> GitHub poster</summary>
<br>

需要找到你 `GitHub Name` (url 后面那个)

```
python3 -m github_poster github --github_user_name "${github_user_name}" --with-skyline
or
github_poster github --github_user_name "${github_user_name}" --with-skyline
```
</details>

### GitLab

<details>
<summary>Make your <code>GitLab </code> GitLab poster</summary>
<br>

需要找到你 `GitLab Name` (url 后面那个)

```
python3 -m github_poster gitlab --gitlab_user_name "${gitlab_user_name}"
or
github_poster gitlab --gitlab_user_name "${gitlab_user_name}"
```

如果是自己搭建的 `GitLab`，可以指定 `GitLab` 的 URL，以及登录 `GitLab` 后得到的 `_gitlab_session` 这个 `cookie`(如果需要登录的话)

```
python3 -m github_poster gitlab --gitlab_user_name "${gitlab_user_name}" --base_url "https://your-gitlab.com" --session "${gitlab_session}"
or
github_poster gitlab --gitlab_user_name "${gitlab_user_name}" --base_url "https://your-gitlab.com" --session "${gitlab_session}"
```

</details>

### Kindle

<details>
<summary>Make your <code>Kindle</code> GitHub poster</summary>
<br>

在亚马逊网站上需要找到你 [Amazon-CN](https://www.amazon.cn/) (XHR) Cookie

```
python3 -m github_poster kindle --kindle_cookie ${kindle_cookie} --cn --year 2018-2021
or
github_poster kindle --kindle_cookie ${kindle_cookie} --cn --year 2018-2021
```

</details>

### WakaTime

<details>
<summary>Make your <code>WakaTime</code> poster</summary>
<br>

在 WakaTime 官网获取你的 WakaTime API Key：[WakaTime API Key](https://wakatime.com/settings/api-key)

```
python3 -m github_poster wakatime --wakatime_key="your_wakatime_api_key" --year 2019-2021
or
github_poster wakatime --wakatime_key="your_wakatime_api_key" --year 2019-2021
```

</details>

### Dota2

<details>
<summary>Make your <code>Dota2</code> poster</summary>
<br>

找到 `Dota2` 的游戏 ID，例如：`Dendi` 的 ID `70388657`
通过 `steam url/username` 查询到你的 `dota2_id` : https://steamid.xyz/
使用 `dota2_id` 取得你的游戏数据：https://api.opendota.com/api/players/{dota2_id}/matches.
更多接口信息：https://docs.opendota.com/#section/Introduction"


```
python3 -m github_poster dota2 --dota2_id="your dota2 id" --year 2017-2018
or
github_poster dota2 --dota2_id="your dota2 id" --year 2017-2018
```

</details>

### Nike

<details>
<summary>Make your <code> Nike </code> poster</summary>>

获取 Nike 的 refresh_token

1. 登录 [Nike](https://www.nike.com) 官网
2. In Developer -> Application-> Storage -> https:unite.nike.com 中找到 refresh_token


```
python3 -m github_poster nike --nike_refresh_token="your nike_refresh_token" --year 2012-2021
or
github_poster nike --nike_refresh_token="your nike_refresh_token" --year 2012-2021
```

</details>

### Garmin
<details>
<summary>Make your <code> Garmin </code> poster</summary>>

需要填写 Garmin 的账号和密码

```
python3 -m github_poster garmin --garmin_user_name ${user_name} --garmin_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618 --cn
or
github_poster garmin --garmin_user_name ${user_name} --garmin_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618 --cn
```
</details>

### Mutiple

<details>
<summary>Make your <code>Mutiple types</code> poster</summary>
<br>

多个 types 最多支持三个，参数参考上面文档

```
python3 -m github_poster multiple  --types "github, twitter, strava" --twitter_user_name "twitter user name" --github_user_name "github user name" --strava_client_id  "your strava client id"  --strava_client_secret "your strava client secret"  --strava_refresh_token "your strava refresh token"  --year 2020-2021
```

</details>

# 参与项目

- 任何 Issues PR 均欢迎。
- 可以提交新的 loader

提交PR前:
- 使用 black 对 Python 代码进行格式化。(`black .`)
- 使用 isort 对 Python import 进行格式化。(`isort --profile black  **/**/*.py` )

# TODO

- [x] twitter
- [x] GitLab
- [x] GitHub
- [x] LeetCode
- [x] GitHub from issues
- [x] YouTube
- [x] Bilibili
- [x] GitHub Actions
- [x] Change all default color
- [x] Skyline
- [x] Dota2
- [ ] 如何写 loader 的 doc
- [x] pypi
- [x] test
- [x] English README

# GitHub Actions

1. fork or clone this repo
2. 更改需要的 secrets
3. 更改需要的 type, 多个 type 用逗号分隔

![image](https://user-images.githubusercontent.com/15976103/116517569-be6fee00-a901-11eb-9178-55df0c3301e3.png)
![image](https://user-images.githubusercontent.com/15976103/116517636-d21b5480-a901-11eb-90e7-8314404f5f59.png)

# 特别感谢
- @[flopp](https://github.com/flopp) 特别棒的项目 [GpxTrackPoster](https://github.com/flopp/GpxTrackPoster)
- @[JasonkayZK](https://github.com/JasonkayZK) Wakatime loader
- @[shaonianche](https://github.com/shaonianche) Dota2 loader
- @[frostming](https://github.com/frostming) `CI` refator and some Actions code

# 赞赏
谢谢就够了
