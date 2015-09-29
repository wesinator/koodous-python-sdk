# Python SDK
This is the Python SDK developed by our team to use Koodous easily.

#In development!!!

Koodous works with many different hashes algortihms, but we prefer sha256 to manage all samples in the better way.
#How to install?
Easy!!
From Github:
```
$ git clone https://github.com/Koodous/python-sdk.git
$ cd python-sdk
$ pip install -r requirements.txt
$ sudo python setup.py install
```

Or easier, from PyPi:
```
$ pip install koodous-py
```

#How to use?

The only thing that you need is your API token that you can obtain after register in [koodous.com](https://koodous.com) for free!
Go to your profile and there it is.
```
import koodous
koodous_obj = koodous.Koodous(token)
koodous_obj.upload(filepath)
```
##Search APKs
```
apks = obj.search('whatsapp and package_name:"com.whatsapp" and size:2MB+ and rating:2+')
```
This apks variable contains a python list with the details of the found APKs.
```
[   
    ...,
    {
        "size": 16674795,
        "rating": 2,
        "sha1": "8b0b907fb72d6284d22ccacb40df1b497a361ad1",
        "corrupted": false,
        "package_name": "com.whatsapp",
        "tags": [
            "googleplay"
        ],
        "image": "https://koodous.com/media/apk_images/tmpRdiC7v",
        "detected": false,
        "repo": "googleplay",
        "created_on": 1426302935,
        "stored": true,
        "displayed_version": "2.12.5",
        "analyzed": true,
        "sha256": "f149b135f86ce2dbaa6a0efb332fb0309d39dd692100172b4aff3f95ce5c43b4",
        "company": "WhatsApp Inc.",
        "app": "WhatsApp",
        "trusted": false,
        "md5": "3b7991ee09db22db6de8e1d5d58e2885"
    },
    ...
]
```
##Download an analysis
```
analysis = koodous_obj.get_analysis(sha256)
```
If analysis has "None" value this means that the analysis is not ready. You can require an analysis, wait 2 minutes approximately and request it again.
```
koodous_obj.analyze(apk) #Wait 2 minutes and retry get_analysis(sha256)
```
And then you can access to analysis information (JSON format):
```
print analysis
{
    "androguard": {
        "app_name": "图表",
        "package_name": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh",
        "providers": [],
        "new_permissions": [],
        "filters": [
            "android.app.action.DEVICE_ADMIN_ENABLED",
            "android.intent.action.MAIN",
            "android.provider.Telephony.SMS_RECEIVED"
        ],
        "max_sdk_version": null,
        "certificate": {
            "sha1": "7750A347F871CF2C9753A6958E87ABE2358AA9B0",
            "IssuerDN": "C=US, O=Android, CN=Android Debug",
            "subjectDN": "C=US, O=Android, CN=Android Debug"
        },
        "min_sdk_version": "8",
        "version_code": "2",
        "libraries": [],
        "target_sdk_version": "20",
        "cordova": null,
        "activities": [
            "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.MainActivity"
        ],
        "main_activity": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.MainActivity",
        "receivers": [
            "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.DevicesReceiver2",
            "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.laixinxis"
        ],
        "signature_name": "META-INF/CERT.RSA",
        "dexes": {
            "classes": {
                "ssdeep": "384:lrmS/xLyL7zIQ9CIBLlCRWAodycJ2NWhWYORsynlvGO61EP4T:lSwxLInI3IBLntnhPOR2O6Y4T",
                "sha256": "17e213420ee4d5c78fb9fcd0e0af668922aaf7ff0c98d0ace3c21e58f19be8dd"
            }
        },
        "displayed_version": "2.0",
        "services": [
            "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.MyServers1"
        ],
        "permissions": [
            "android.permission.SEND_SMS",
            "android.permission.KILL_BACKGROUND_PROCESSES",
            "android.permission.WRITE_SMS",
            ...
        ],
        "functionalities": {
            "dynamicbroadcastreceiver": [
                {
                    "code": "invoke-virtual v7, v1, v0, v2, v6, Ldfkldsfdgjhdfg/fdgjndfkgirg/fghsdiuogh/MyServers1;->registerReceiver(Landroid/content/BroadcastReceiver; Landroid/content/IntentFilter; Ljava/lang/String; Landroid/os/Handler;)Landroid/content/Intent;",
                    "class": "Ldfkldsfdgjhdfg/fdgjndfkgirg/fghsdiuogh/MyServers1;",
                    "method": "onCreate"
                },
                {
                    "code": "invoke-virtual v3, v1, Ldfkldsfdgjhdfg/fdgjndfkgirg/fghsdiuogh/MyServers1;->unregisterReceiver(Landroid/content/BroadcastReceiver;)V",
                    "class": "Ldfkldsfdgjhdfg/fdgjndfkgirg/fghsdiuogh/MyServers1;",
                    "method": "onDestroy"
                }
            ]
        },
        "urls": [
            "http://60.8.229.158:8002/sj.asp"
        ]
    },
    "cuckoo": {
        "network": {
            "http": [],
            "smtp": [],
            "hosts": [],
            "dns": [],
            "domains": [],
            "irc": []
        },
        "target": {
            "category": "file",
            "file": {
                "size": 54477,
                "sha1": "4bac63842c26957190ae1722647c1f0fc6828f1d",
                "crc32": "4339AE28",
                "ssdeep": "768:XyDIt03WP8fPyKC4rCHkHu7rnQJ1KRPJEOdLt74Hz9DncM5WYxwiGM4ywEHfXl+5:ENzPKkO7rIKRPJFdxcBp5X8rEvMjy0r",
                "sha256": "88ddda0977d8af07d5b04979736e713a950767f7270658ead6781e6464631f8a",
                "sha512": "f6761c060b4bd80a9dd456f498a48d0dbd20056e33936fbb05e789cbea6f250c3debeafe2e1923df884b90aa793a5842814c7c30ea79f48666c4618f536a7db5",
                "md5": "4be0093ac136b39ec33021f7b55452a9"
            }
        }
    },
    "droidbox": {
        "fileswritten": [],
        "dns": [],
        "cryptousage": [],
        "filesread": [
            {
                "name": "/data/app/dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh-1.apk",
                "pid": 846,
                "processname": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh",
                "time": 1.813291,
                "tid": 1073870640,
                "data": "504b0506000000000b..."
            }
        ],
        "sendsms": [],
        "servicestart": [
            {
                "tid": 1073870640,
                "processname": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh",
                "pid": 846,
                "name": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh.MyServers1",
                "time": 3.314782
            }
        ],
        "sendnet": [],
        "libraries": [],
        "phonecalls": [],
        "recvnet": [],
        "dexclass": [
            {
                "tid": 1073870640,
                "processname": "dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh",
                "time": 1.752926,
                "pid": 846,
                "path": "/data/app/dfkldsfdgjhdfg.fdgjndfkgirg.fghsdiuogh-1.apk"
            },
            ...
        ]
    }
}
```

##Downloading a sample
You can use two methods, first download to a file directly:
```
koodous_obj.download_to_file(sha256, "/home/name/filename")
```
Or you can obtain the download URL to use as you want:
```
url = koodous_obj.get_download_url(sha256)
print url
```
#Comments
##Posting a comment
```
text_posted = koodous_obj.post_comment(sha256, comment_text)
```
##See APK comments
```
comments = koodous_obj.get_comments(sha256)
```
##Delete a comment
```
koodous_obj.delete_comment(comment_id)
```

##Analyze a sample
```
koodous_obj.analyze(sha256) 
#Wait 2 minutes and try:
analysis = koodous_obj.get_analysis(sha256)
```

#Utils
We implement some tools to interact with APKs and not related explicit with Koodous:
##SHA256 file
```
>>> import koodous
>>> koodous.utils.sha256('asd')
'133ee989293f92736301280c6f14c89d521200c17dcdcecca30cd20705332d44'
```

Unpack and APK and generate one file with all content uncompressed.
```
>>> import koodous
>>> koodous.utils.unpack('sample_test.apk', 'destination_file')
```
