# README

## 项目架构

```text
EE208项目架构

│  .gitignore
│  config.py
│  content.bat
│  content.txt
│  manage.py
│  password.py
│  README.md
│  requirements.txt
│  
│       
├─app
│  │  models.py
│  │  password.py
│  │  __init__.py
│  │  
│  ├─img_search
│  │  │  config.py
│  │  │  evaluation.py
│  │  │  img_infos.npy
│  │  │  img_loader.py
│  │  │  LSH.py
│  │  │  utils.py
│  │  │  __init__.py
│  │  │  
│  │  └─test
│  │         1000245077_1.jpg
│  │         1000380456_0.jpg
│  │         1000380456_1.jpg
│  │         test1.jpg
│  │         test2.jpg
│  │          
│  ├─logo_search
│  │  │  logo_matching.py
│  │  │  __init__.py
│  │  │  
│  │  └──logo
│  │     │  test.jpg
│  │     │  
│  │     └─train
│  │             361_1.jpg
│  │             adidas_1.jpg
│  │             adidas_2.jpg
│  │             anta_1.jpg
│  │             asics_1.jpg
│  │             converse_1.jpg
│  │             LiNing_1.jpg
│  │             NewBalance_1.jpg
│  │             nike_1.jpg
│  │             nike_2.jpg
│  │             puma_1.jpg
│  │          
│  ├─main
│  │  │  EE208_ES_FP_class.py
│  │  │  errors.py
│  │  │  forms.py
│  │  │  test.py
│  │  │  views.py
│  │  │  WordCloud.py
│  │  └─ __init__.py
│  │
│  │          
│  ├─static
│  │  │  bootstrap.css
│  │  │  champion.png
│  │  │  cover.jpg
│  │  │  custom.js
│  │  │  djy.jpg
│  │  │  djy_qr.jpg
│  │  │  gadgets.png
│  │  │  icon.png
│  │  │  item.css
│  │  │  JOMA.jpg
│  │  │  jsy.jpg
│  │  │  jsy_qr.png
│  │  │  parallax-bg.jpg
│  │  │  puma.png
│  │  │  search.png
│  │  │  share.png
│  │  │  ywl.jpg
│  │  │  ywl_qr.jpg
│  │  │  zrh.jpg
│  │  │  zrh_qr.jpg
│  │  │  安踏.png
│  │  │  李宁.png
│  │  │  耐克.png
│  │  └─ 阿迪达斯.png
│  │          
│  ├─templates
│  │      404.html
│  │      500.html
│  │      base.html
│  │      base2.html
│  │      index.html
│  │      item.html
│  │      result.html
│  │      upload.html
│  │      upload_logo.html
│  │      
│  └──upload
│         1000245077_1.jpg
│         1000380456_1.jpg
│         1001040677_2.jpg
│         1001197777_0.jpg
│         panda.jpg
│         test.jpg
│         test1.jpg
│         头像.jpg
│          
├─DangDang
│  │  main.py
│  │  password.py
│  │  README.txt
│  │  scrapy.cfg
│  │  
│  └──DangDang
│     │  items.py
│     │  middlewares.py
│     │  pipelines.py
│     │  res.py
│     │  settings.py
│     │  __init__.py
│     │  
│     └──spiders
│        │  Dang.py
│        └─ __init__.py
│          
├─flaskechart
│  │  app.py
│  │  cut_comment_segment.py
│  │  
│  ├─.vscode
│  │      settings.json
│  │      
│  └──templates
│         index.html
│          
└──Migration
       concat.py
        
```

## 项目依赖

本次项目的依赖包括以下`python` 库:

```requirements
Flask==0.12.2
Flask-Bootstrap==3.3.7.1
Flask-Cors==3.0.2
Flask-SQLAlchemy==2.4.4
Flask-WTF==0.14.3
jieba==0.42.1
Jinja2==2.11.2
numpy==1.19.5
pyecharts==1.9.0
PyMySQL==1.0.1
bitarray==0.8.1
lxml==3.7.3
progressbar==2.5
PyTorch==1.6.0
torchvision==0.7.0
```

## 项目分工

|     分工      |           负责人            |
| :-----------: | :-------------------------: |
|     爬虫      |           丁健宇            |
|   前端搭建    |        江书洋 丁健宇        |
|   后端实现    |        张若涵 易文龙        |
|   文档撰写    | 张若涵 丁健宇 江书洋 易文龙 |
|   报告撰写    | 张若涵 丁健宇 江书洋 易文龙 |
| PPT制作及答辩 |           易文龙            |
| Demo展示录制  |           丁健宇            |

## 项目准备

首先需要在命令行安装以上依赖项, 可以在命令行中输入以下命令:

```shell
pip install -r requirements.txt
```

其次, 需要确保数据库开启, 具体的密码通过项目展示页的`index.html`上的二维码向项目成员进行获取.
另外, 需要保证本地的ElasticSearch在打开状态. 具体的做法如下:

- 首先进入[下载](https://www.elastic.co/cn/downloads/past-releases/elasticsearch-7-5-2)页面, 找到相对应的环境版本：``
- 下载`*.zip`文件到本地, 解压缩后进入`elasticsearch-7.5.2/bin`文件夹中, 首先运行`bin/elastic_search`或者是`bin/elastic_search.bat`（取决于操作系统）. 
- 其次运行以下命令`curl http://localhost:9200/`或者在`Windows`的`Powershell`上运行`Invoke-RestMethod http://localhost:9200`
- 保持第二步的命令行窗口不关闭的情况下, 运行本项目中的其他代码.

在终端, 进入到本项目的目录下, 运行下列代码:

```bash
python manage.py
```

## 项目功能

本次项目采集了当当网、网易严选（以当当网为主）两大电商网站中的运动服饰和电子数码两类商品, 构建了一个功能完整丰富、体验效果良好、视觉感官享受的搜索引擎.
本搜索引擎能够实现以下核心及亮点功能：

1. 能够根据商品名称、商品属性、关键词进行检索
2. 能够上传图片, 根据图片进行检索
3. 能够按照相关度、价格等属性对搜索结果进行排序展示
4. 能够按照类别、品牌、特性等属性对商品进行过滤
5. 能够用词云等可视化方式展示评论信息要点
6. 能够根据商品评论内容进行情感分析估计商品质量, 按照打分进行商品排序
7. 能够根据品牌名称进行搜索
8. 能够上传实物logo图像, 准确识别并进行搜索
