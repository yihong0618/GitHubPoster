# GitHubPoster

Make everything a GitHub svg poster and [skyline](https://skyline.github.com/)!

##  `svg` in `README` examples

![](https://github.com/yihong0618/GitHubPoster/blob/main/examples/twitter.svg)

## Circular

![](https://github.com/yihong0618/GitHubPoster/blob/main/examples/strava_circular.svg)

## Skyline

![image](https://user-images.githubusercontent.com/15976103/120966953-80d07180-c799-11eb-8769-92554905ab3f.png)

## Support

- **[Strava](#strava)**
- **[Nintendo Switch](#ns)**
- **[GPX](#GPX)**
- **[Duolingo](#duolingo)**
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
- **[Notion](#Notion)**
- **[Garmin](#Garmin)**
- **[Forest](#Forest)**
- **[Json](#Json)**
- **[Multiple](#Multiple)**
- **[Jike](#Jike)**
- **[Summary](#Summary)**
- **[Todoist](#Todoist)**
- **[OpenLanguage](#OpenLanguage)**
- **[Apple Health](#AppleHealth)**
- **[ChatGPT](#ChatGPT)**

## Download
```
git clone https://github.com/yihong0618/GitHubPoster.git
```
## pip install

```
pip3 install -U 'github_poster[all]'
```

## Install(Python3.6+)
```
pip3 install -r requirements.txt
```

## Use

The generated svg is in `OUT_FOLDER`, named with type (for now)

Different types are used as specified below:

- `--year 2021`: You can specify a year (default) or a year range `--year 2012-2021`
- `--special-number1 10 -- special_number2 20`: By default, the number of different colors is automatically generated (special colors), you can also specify the color
- `--special-color1 pink --special-color2 '#33C6A4'`: You can also specify the color
- `--with-animation`: You can add animation (add GOGOGO animation)
- `--animation-time 14`: you can control the animation time (default is 10s), use with `--with-animation`
- `--with-skyline`: You can save skyline `stl` file (default skyline year is to_year),
- `--skyline-with-name`: set to print user name on model, use with `--with-skyline`
- `--is-circular`: With this command, the svg will be circular and with animation
- `--without-type-name`: Support for hiding the name of the build type in the title
- `---stand-with-ukraine`

Other parameters can be found with `python3 -m github_poster <type> --help`


### GPX

<details>
<summary>Make your <code>GPX</code> GitHub poster</summary>
<br>

mv gpx files to `GPX_FOLDER` then run the code
```
python3 -m github_poster gpx --gpx_dir ~/blog/GPX_OUT/ --year 2013-2021
or pip
github_poster github_poster gpx --gpx_dir ~/blog/GPX_OUT/ --year 2013-2021
```
</details>

### Strava

<details>
<summary>Make your <code>Strava</code> GitHub poster</summary>

1. Sign in/Sign up [Strava](https://www.strava.com/) account
2. Open after successful Signin [Strava Developers](http://developers.strava.com) -> [Create & Manage Your App](https://strava.com/settings/api)

3. Create `My API Application`: Enter the following information

<br>

![My API Application](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/strava_settings_api.png)
Created successfully：

<br>

![](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/created_successfully_1.png)

4. Use the link below to request all permissions: Replace `${your_id}` in the link with `My API Application` `Client ID`
```
https://www.strava.com/oauth/authorize?client_id=${your_id}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all,profile:write,activity:write
```
![get_all_permissions](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_all_permissions.png)

5. Get the `code` value in the link

<br>

example：
```
http://localhost/exchange_token?state=&code=1dab37edd9970971fb502c9efdd087f4f3471e6e&scope=read,activity:write,activity:read_all,profile:write,profile:read_all,read_all
```
`code` value：
```
1dab37edd9970971fb502c9efdd087f4f3471e6
```
![get_code](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_code.png)

6. Use `Client_id`、`Client_secret`、`Code` get `refresch_token`: Execute in `Terminal/iTerm`
```
curl -X POST https://www.strava.com/oauth/token \
-F client_id=${Your Client ID} \
-F client_secret=${Your Client Secret} \
-F code=${Your Code} \
-F grant_type=authorization_code
```
example：
```
curl -X POST https://www.strava.com/oauth/token \
-F client_id=12345 \
-F client_secret=b21******d0bfb377998ed1ac3b0 \
-F code=d09******b58abface48003 \
-F grant_type=authorization_code
```
![get_refresch_token](https://raw.githubusercontent.com/shaonianche/gallery/master/running_page/get_refresch_token.png)

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

From APP`(Nintendo Switch Parent Controls)` using `mitmproxy` to get the `session_token` and `devide _id`

```
python3 -m github_poster ns --ns_session_token ${session_token} --ns_device_id ${device_id} --year 2020-2021
or pip
github_poster ns --ns_session_token ${session_token} --ns_device_id ${device_id} --year 2020-2021
```
</details>


### Duolingo

<details>
<summary>Make your <code>Duolingo</code> GitHub poster</summary>
<br>

Find your `duolingo id`, F12 from `XHR`
![image](https://user-images.githubusercontent.com/15976103/116336188-baad7000-a80a-11eb-80d7-033d4bf0f260.png)


```
python3 -m github_poster duolingo --duolingo_user_name ${user_id} --year 2015-2021
or
github_poster duolingo --duolingo_user_name ${user_id} --year 2015-2021
```
</details>

### Issue

<details>
<summary>Make your <code>Issue</code> GitHub poster</summary>
<br>

Like my [issue](https://github.com/yihong0618/2021/issues/5)

```
	python3 -m github_poster issue --issue_number ${issue_number} --repo_name ${repo_name} --token ${github_token}
or
github_poster issue --issue_number ${issue_number} --repo_name ${repo_name} --token ${github_token}
```
</details>

### LeetCode

<details>
<summary>Make your <code>LeetCode</code> GitHub poster</summary>
<br>

Find your `LeetCode Cookie`

```
python3 -m github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021
or
github_poster leetcode --leetcode_cookie ${leetcode_cookie} --year 2019-2021
```

</details>

### Twitter

<details>
<summary>Make your <code>Twitter</code> GitHub poster</summary>
<br>

Find your `Twitter user_id` (in the url)

```
python3 -m github_poster twitter --twitter_user_name ${user_name} --year 2018-2021 --track-color '#1C9CEA'
or
github_poster twitter --twitter_user_name ${twitter_user_name} --year 2018-2021 --track-color '#1C9CEA'
```

The method above uses [twint](https://github.com/twintproject/twint) to scrape tweets directly from Twitter.

Alternatively, [download your Twitter Archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive) and use `contrib/convert_twitter_archive_to_json_data_source.py` to convert it to JSON data source and feed it to [Json](#Json) loader. This method is useful if one or more of the following applies to you:

- You have lots of tweets.
- You have been using Twitter for many years.
- Your connection to Twitter is not reliable enough.
- You have a protected Twitter account.
</details>

### Youtube

<details>
<summary>Make your <code>YouTube</code> GitHub poster</summary>
<br>

Use Google [History Takeout](https://takeout.google.com/settings/takeout) to download `YouTube` history data，choose `json` format，mv `watch-history.json` to `IN-FOLDER` then run the code

```
python3 -m github_poster youtube --year 2015-2021
or
github_poster youtube --year 2015-2021
```
</details>

### Bilibili

<details>
<summary>Make your <code>Bilibili</code> GitHub poster</summary>
<br>

Find your `Bilibili (XHR) cookie`

```
python3 -m github_poster bilibili --cookie "${bilibili-cookie}"
or
github_poster bilibili --cookie "${bilibili-cookie}"
```
</details>

### GitHub

<details>
<summary>Make your <code>GitHub</code> GitHub poster</summary>
<br>

Get your `GitHub Name` (in the url)

```
python3 -m github_poster github --github_user_name "${github_user_name}" --with-skyline
or
github_poster github --github_user_name "${github_user_name}" --with-skyline
```
</details>

### GitLab

<details>
<summary>Make your <code>GitLab</code> GitLab poster</summary>
<br>

Get your `GitLab Name` (in the url)

```
python3 -m github_poster gitlab --gitlab_user_name "${gitlab_user_name}"
or
github_poster gitlab --gialab_user_name "${gitlab_user_name}"
```

For self-managed `GitLab`, specify the base url of your instance. You should use `_gitlab_session` from Cookies if sign in required.
s
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

Find your [Amazon](https://www.amazon.com/) Cookie

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

Find your own `WakaTime API Key` at: [WakaTime API Key](https://wakatime.com/settings/api-key)

```
python -m github_poster wakatime --wakatime_key="your_wakatime_api_key" --year 2019-2021
or
github_poster wakatime --wakatime_key="your_wakatime_api_key" --year 2019-2021
```

</details>

### Dota2

<details>
<summary>Make your <code>Dota2</code> poster</summary>
<br>

Find your `dota2_id`, eg：Dendi's ID `70388657`
Check your dota2_id(steamid32): https://steamid.xyz/.
Check your game data: https://api.opendota.com/api/players/{dota2_id}/matches.
more info: https://docs.opendota.com/#section/Introduction


```
python -m github_poster dota2 --dota2_id="your dota2 id" --year 2017-2018
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

### Notion

<details>
<summary>Make your <code> Notion </code> poster</summary>

Get Notion `Internal Integration Token`(notion_token), see [here](https://developers.notion.com/docs/authorization#authorizing-internal-integrations) for more details.

1. Sign in [Notion](https://www.notion.so/my-integrations) developers site
2. Click 'New integration' to create a new token
3. You can see `Internal Integration Token` below `Secrets` after submit

Get Notion Database ID(database_id), see [here](https://developers.notion.com/docs/working-with-databases#adding-pages-to-a-database) for more details.

1. Open the database as a full page in Notion
2. Use the `Share` menu to `Copy link`, and you'll get a URL looks like `https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`
3. The part that corresponds to `{database_id}` is the ID of your Notion Database

Note：The database need a property which type is `Date`, the value of it will be used to generate the poster.
The name of the date property should be set as option `prop_name`'s value，default value is `Datetime`

```
python3 -m github_poster notion --notion_token="your notion_token" --database_id="your database_id" --prop_name="your prop_name"
or
github_poster notion --notion_token="your notion_token" --database_id="your database_id" --prop_name="your prop_name"
```

</details>

### Garmin
<details>

<summary>Make your <code> Garmin </code> poster</summary>

需要填写 Garmin 的账号和密码

```
python3 -m github_poster garmin --garmin_user_name ${user_name} --garmin_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618 --cn
or
github_poster garmin --garmin_user_name ${user_name} --garmin_password ${pass_word} --year 2016-2021 --special-color1 blue --special-color2 pink --me yihong0618 --cn
```
</details>

### Forest

<details>
<summary>Make your <code> Forest </code> GitHub poster</summary>
<br>

Need to add your Forest email and password

```
python3 -m github_poster forest --forest_email ${user_name} --forest_password ${pass_word} --year 2016-2021 --special-color1 blue --me yihong0618
or
github_poster forest --forest_email ${user_name} --forest_password ${pass_word} --year 2016-2021 --special-color1 blue --me yihong0618
```
</details>

### Json

<details>
<summary>Make your <code>Json(source data) types</code> poster</summary>
<br>

make sure your json file format is like `data.json` in examples

```
python3 -m github_poster json --json_file "your json data file" --year 2019-2021 --me PythonHunter
or
github_poster json --json_file "your json data file" --year 2019-2021 --me PythonHunter
```

</details>

### Multiple

<details>
<summary>Make your <code>Multiple types</code> poster</summary>
<br>

support multiple types

```
python3 -m github_poster multiple  --types "github, twitter, strava" --twitter_user_name "twitter user name" --github_user_name "github user name" --strava_client_id  "your strava client id"  --strava_client_secret "your strava client secret"  --strava_refresh_token "your strava refresh token"  --year 2020-2021
or
github_poster multiple  --types "github, twitter, strava" --twitter_user_name "twitter user name" --github_user_name "github user name" --strava_client_id  "your strava client id"  --strava_client_secret "your strava client secret"  --strava_refresh_token "your strava refresh token"  --year 2020-2021
```

</details>

### Summary

<details>
<summary>Make your <code>Summary types</code> poster</summary>
<br>

support summary types

```
python3 -m github_poster summary  --types "github, twitter, strava" --twitter_user_name "twitter user name" --github_user_name "github user name" --strava_client_id  "your strava client id"  --strava_client_secret "your strava client secret"  --strava_refresh_token "your strava refresh token"  --year 2021
or
github_poster summary  --types "github, twitter, strava" --twitter_user_name "twitter user name" --github_user_name "github user name" --strava_client_id  "your strava client id"  --strava_client_secret "your strava client secret"  --strava_refresh_token "your strava refresh token"  --year 2021
```
</details>

### Jike

<details>
<summary>Make your <code>Jike(source data) types</code> poster</summary>
<br>

need to find your Jike cookie from `Jike (XHR)` and `jike_user_id`, `jike_user_id` can be found in your personal page link
eg. in the link `https://web.okjike.com/u/82D23B32-CF36-4C59-AD6F-D05E3552CBF3`, `82D23B32-CF36-4C59-AD6F-D05E3552CBF3` is the user_id

ps. only get the data for the last year

```
python3 -m github_poster jike --jike_cookie "your jike cookie" --jike_user_id 'your jike user id' --year 2021 --me "your name" --with-animation --animation-time 14 --count_type 'like'
or
github_poster jike --jike_cookie "your jike cookie" --jike_user_id "your jike user id" --year 2021 --me "your name" --with-animation --animation-time 14 --count_type 'like'
```

Option argument `count_type`, you can specify statistics type:
- `record`: post num (default)
- `like`: post be liked num
- `share`: post be share num
- `comment`: post be comment num
- `repost`: post be repost num

</details>

### Todoist

<details>
<summary>Make <code> Todoist Task Completion </code> GitHub poster</summary>

Because of Todoist policies, only users with Pro Plan(or above) can retrieve full historical activity from APIs.

Get your token please find on [Todoist Developer Docs](https://developer.todoist.com/guides/#developing-with-todoist)

<br>

```
python3 -m github_poster todoist --year 2021-2022 --todoist_token "your todoist dev token" --me "your name"
or
github_poster todoist --year 2021-2022 --todoist_token "your todoist dev token" --me "your name"
```
</details>

### OpenLanguage

<details>
<summary>Make <code> OpenLanguage </code> GitHub poster</summary>

For some reason, make sure your password only has letters and numbers, otherwise you will get an error.
<br>

```
python3 -m github_poster openlanguage --year 2021-2022 --openlanguage_user_name "you account" --openlanguage_password "you password" --me "your name"
or
github_poster openlanguage --year 2021-2022 --openlanguage_user_name "you account" --openlanguage_password "you password" --me "your name"
```
</details>

### AppleHealth
<details>
<summary>Make <code> Apple Health </code> GitHub poster</summary>

Apple Health has plenty of data that can be visualized. 
At this moment this loader only supports Move, Exercise, and Stand data from Apple Watch Activity but any record Apple Health has can be supported in the same way.

Loader has two modes: 

increment mode (default）is good for daily update. iOS Shortcut can be used to trigger a workflow running loader on this mode.
Read [this repo](https://github.com/yihong0618/iBeats) for more details.
<br>
```
python3 -m github_poster apple_health --date <date-str> --value <value> --apple_health_record_type <move, exercise, stand> --me "your name"
or
github_poster apple_health --appple_health_date <date-str> --apple_health_value <value> --apple_health_record_type <move, exercise, stand> --me "your name"
```

backfill mode is good for dumping all data at once.
Open the Health App, click on the avatar on the top right corner, select "Export All Health Data" on the bottom, copy the zip file to `IN-FOLDER` and unzip. You will get a `apple_health_export` folder. Then run:
<br>
```
python3 -m github_poster apple_health --apple_health_mode backfill --year 2015-2021 --apple_health_record_type <move, exercise, stand> --me "your name"
or
github_poster apple_health --apple_health_mode backfill --year 2015-2021 --apple_health_record_type <move, exercise, stand> --me "your name"
```

### ChatGPT

<details>
<summary>Make your <code> ChatGPT </code> GitHub poster</summary>
<br>

Copy the conversations.json from ChatGPT's official export history to `IN-FOLDER`, then run (renamed to chatgpt-history.json)

```
python3 -m github_poster chatgpt 
or
github_poster chatgpt --me yihong0618
```
</details>

# Contribution

- Any Issues PR welcome.
- Any new loader welcome
- how to write new loader by `ruter`(Chinese) [如何为 GithubPoster 添加 loader](https://umm.js.org/p/c88bf4c7/)

Before submitting PR:
- Format Python code with `black` (`black .`)
- Format Python code with `isort` (`isort --profile black  **/**/*.py`)

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
- [x] pypi
- [x] test
- [x] English README
- [x] Loader doc
- [ ] Refactor some code

# GitHub Actions

1. fork or clone this repo
2. Change the secrets
3. Change the `type` in `yml` file

![image](https://user-images.githubusercontent.com/15976103/116517569-be6fee00-a901-11eb-9178-55df0c3301e3.png)
![image](https://user-images.githubusercontent.com/15976103/116517636-d21b5480-a901-11eb-90e7-8314404f5f59.png)

# Special thanks

- @[flopp](https://github.com/flopp) great repo [GpxTrackPoster](https://github.com/flopp/GpxTrackPoster)
- @[JasonkayZK](https://github.com/JasonkayZK) Wakatime loader
- @[shaonianche](https://github.com/shaonianche) Dota2 loader
- @[umm233](https://github.com/umm233) Jike loader
- @[ruter](https://github.com/ruter) Notion loader
- @[frostming](https://github.com/frostming) `CI` refator and some Actions code
- @[j178](https://github.com/j178) refator the import logic
- @[iamshaynez](https://github.com/iamshaynez) todolist loader
- @[guaguaguaxia](https://github.com/guaguaguaxia) OpenLanguage loader
- @[rip-tyang](https://github.com/rip-tyang) AppleHealth loader

# Support

Thanks is enough.
