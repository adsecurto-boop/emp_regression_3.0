# EmpMonitor 3.0 Automated Regression Test Report

## 1. Execution Metadata Summary

- **Date & Time**: `2026-08-26 14:01:59`
- **Agent Version Evaluated**: `3.0.1`
- **Local Active Host Email (L1)**: `autotest@gmail.com`
- **Searched Dashboard User (L4)**: `auto test`
- **Dashboard Registered Email (L4)**: `autotest@gmail.com`
- **Screencast Stream Status (L4)**: `OFFLINE / FALLBACK`
- **Final System Verdict**: **`HEALTHY`**

---

## 2. Layer 1 System Configuration Audit

- **Local INI Path**: `C:\Users\GBSBHL1261\AppData\Roaming\screen\OjUxFCN\empm.ini`
- **INI File Size**: `4.43 KB` (EV-001 Requirement: > 3.0 KB)

### Binary Presence & Running Process Status

- **Binary `empmonitor.exe`**: N/A (Legacy < 3.1.0)
- **Binary `UpdateMgr_Emp.exe`**: N/A (Legacy < 3.1.0)
- **Binary `esr.exe`**: N/A (Legacy < 3.1.0)
- **Binary `emp_psa_service.exe`**: N/A (Legacy < 3.1.0)
- **Process `empmonitor.exe`**: N/A (Legacy < 3.1.0)
- **Process `updatemgr_emp.exe`**: N/A (Legacy < 3.1.0)
- **Process `esr.exe`**: N/A (Legacy < 3.1.0)
- **Process `emp_psa_service.exe`**: N/A (Legacy < 3.1.0)

### Sanitized `config.js` Contents (Masked)
```json
{
    "id": "OjUpSmK",
    "api": "https://storelogs.dev.empmonitor.com/api/v1/",
    "login": "https://track.empmonitor.com/api/v3/",
    "pipeline": "https://track.empmonitor.com/api/v3/",
    "realtime": "wss://realtime.empmonitor.com",
    "updates": "https://updates.empmonitor.in/",
    "mode": "personal"
}
```

### Sanitized `empm.ini` Attributes (Masked)
```ini
last_sync_time = @DateTime(\0\0\0\x10\0\0\0\0\0\0%\x8e_\x3\0\x43\xce\0)
is_system_locked = false
currentdate = @Variant(\0\0\0\xe\0%\x8e_)
datasendingperiodsec = 180
lastsettingsaccessdatetime = @DateTime(\0\0\0\x10\0\0\0\0\0\0%\x8e_\x1\xd3\x7f%\x1)
todayremainingbreakinseconds = 1800
from_remote\aduserinfosendpersec = 21600
from_remote\screenshotperiodsec = 60
screenshotquality = 20
token = ****************
email = autotest@gmail.com
crypto_password = ****************
code = 200
data\agentuninstallcode = 
data\announcemnts = @Invalid()
data\block\contact = undefined
data\block\email = undefined
data\block\logo = https://service.empmonitor.com/logo/1662536930741remote_lock_logo.png
data\breakinminute = 0
data\dlpfeatures\bluetoothblock = 0
data\dlpfeatures\bluetoothdetection = 0
data\dlpfeatures\clipboardblock = 0
data\dlpfeatures\clipboarddetection = 1
data\email_monitoring_block_websites = @Variant(\0\0\0\t\0\0\0\x1\0\0\0\n\0\0\0\x1a\0g\0l\0o\0\x62\0u\0s\0s\0o\0\x66\0t\0.\0i\0n)
data\features\screencast = 0
data\features\application_usage = 0
data\features\autocheckout = 0
data\features\block_websites = 1
data\features\email_monitoring = 1
data\features\file_upload_blocking = 1
data\features\file_upload_detection = 1
data\features\keystrokes = *
data\features\mobile_detection_webcam_alert_enabled = 0
data\features\realtimetrack = 1
data\features\remoteterminalaccess = 0
data\features\screen_record = 0
data\features\screenshots = 1
data\features\webcamcapture = 0
data\features\webcamcasting = 0
data\features\web_usage = 1
data\features\webcam_alert_enabled = 0
data\file_upload_block_websites = gemini.google.com, whatsapp.com, chatgpt.com, web.telegram.org, www.ilovepdf.com
data\file_upload_screenshot_alert = 1
data\first_name = auto
data\idleinminute = 5
data\issilahmobilegeolocation = 0
data\is_attendance_override = 0
data\last_name = test
data\logo = https://service.empmonitor.com/logo/1662536930741remote_lock_logo.png
data\logoutoptions\afterfixedhours = 8
data\logoutoptions\option = 2
data\logoutoptions\specifictimeutc = 23:59
data\logoutoptions\specifictimeuser = 23:59
data\logout_feature = true
data\manual_clock_in = 0
data\pack\expiry = 2037-12-31
data\pack\id = 1
data\roomid = a8a877faab1ec5ac0f53520f41a544cb:ebbc73a4ba20cd12389171e3b5a291bc
data\screen_record\audio = 1
data\screen_record\is_enabled = 1
data\screen_record\video_quality = 1
data\screenshot\frequencyperhour = 60
data\silahmobilegeolocationfrequency = 30
data\system\autoupdate = 0
data\system\tracking = 1
data\system\type = 1
data\system\visibility = true
data\systemlock = 0
data\timesheetidletime = 00:00
data\tracking\app\appblocklist = @Invalid()
data\tracking\app\keystrokeblocklist = ****************
data\tracking\app\keystrokewhitelist = ****************
data\tracking\domain\appblocklist = esr.exe
data\tracking\domain\daysandtimes = @Variant(\0\0\0\b\0\0\0\0)
data\tracking\domain\keystrokeblocklist = **********
data\tracking\domain\keystrokewhitelist = **********
data\tracking\domain\monitoronly = @Invalid()
data\tracking\domain\suspendkeystrokespasswords = *****
data\tracking\domain\suspendkeystrokeswhenvisited = **********
data\tracking\domain\suspendmonitorwhencontains = @Invalid()
data\tracking\domain\suspendmonitorwhenvisited = @Invalid()
data\tracking\domain\suspendmonitorwhenvisitedincategory = @Invalid()
data\tracking\domain\suspendprivatebrowsing = false
data\tracking\domain\websiteblocklist = www.facebook.com, www.ilovepdf.com
data\tracking\geolocation = @Invalid()
data\tracking\keystrokepolicymode = *******
data\tracking\networkbased = @Invalid()
data\tracking\projectbased = @Invalid()
data\tracking\unlimited\day = "1,2,3,4,5,6,7"
data\trackingmode = unlimited
data\usbdisable = 1
data\userblock = 0
data\webcam\frequencyperhour = 1
error = @Variant(\0\0\0\x94)
message = User configs
```

---

## 3. Layer 2 Host Log Harvest (Last 200 Lines)

```text
2026-08-26T07:46:03Z - info: Position Updated
2026-08-26T07:46:03Z - info: Position Updated at : "Wed Aug 26 2026" , "13:16:03" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:46:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:46:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:46:53Z - info: Position Updated
2026-08-26T07:46:53Z - info: Position Updated at : "Wed Aug 26 2026" , "13:16:53" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:47:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:47:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:48:42Z - info: Adding new session data with id  QDateTime(2026-08-26 07:45:42.116 UTC Qt::UTC)
2026-08-26T07:48:42Z - info: Trying to send new session data
2026-08-26T07:48:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T07:48:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:48:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:48:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T07:49:03Z - info: Position Updated
2026-08-26T07:49:03Z - info: Position Updated at : "Wed Aug 26 2026" , "13:19:03" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:49:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:49:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:50:03Z - info: Position Updated
2026-08-26T07:50:03Z - info: Position Updated at : "Wed Aug 26 2026" , "13:20:03" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:50:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:50:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:51:42Z - info: Adding new session data with id  QDateTime(2026-08-26 07:48:42.106 UTC Qt::UTC)
2026-08-26T07:51:42Z - info: Trying to send new session data
2026-08-26T07:51:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T07:51:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:51:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:51:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T07:52:14Z - info: Position Updated
2026-08-26T07:52:14Z - info: Position Updated at : "Wed Aug 26 2026" , "13:22:14" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:52:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:52:44Z - info: Position Updated
2026-08-26T07:52:44Z - info: Position Updated at : "Wed Aug 26 2026" , "13:22:44" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:52:45Z - info: Keyboard layout changed: en-IN
2026-08-26T07:52:45Z - info: Keyboard layout changed: en-US
2026-08-26T07:52:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:53:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:53:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:54:42Z - info: Adding new session data with id  QDateTime(2026-08-26 07:51:42.108 UTC Qt::UTC)
2026-08-26T07:54:42Z - info: Trying to send new session data
2026-08-26T07:54:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T07:54:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:54:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:54:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T07:54:59Z - info: Position Updated
2026-08-26T07:54:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:24:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:55:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:55:49Z - info: Position Updated
2026-08-26T07:55:49Z - info: Position Updated at : "Wed Aug 26 2026" , "13:25:49" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:55:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:56:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:56:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:57:42Z - info: Adding new session data with id  QDateTime(2026-08-26 07:54:42.119 UTC Qt::UTC)
2026-08-26T07:57:42Z - info: Trying to send new session data
2026-08-26T07:57:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T07:57:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:57:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:57:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T07:57:59Z - info: Position Updated
2026-08-26T07:57:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:27:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:58:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:58:49Z - info: Position Updated
2026-08-26T07:58:49Z - info: Position Updated at : "Wed Aug 26 2026" , "13:28:49" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T07:58:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T07:59:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T07:59:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:00:42Z - info: Adding new session data with id  QDateTime(2026-08-26 07:57:42.112 UTC Qt::UTC)
2026-08-26T08:00:42Z - info: Trying to send new session data
2026-08-26T08:00:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T08:00:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:00:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:00:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:00:59Z - info: Position Updated
2026-08-26T08:00:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:30:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:01:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:01:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:02:09Z - info: Position Updated
2026-08-26T08:02:09Z - info: Position Updated at : "Wed Aug 26 2026" , "13:32:09" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:02:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:02:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:03:42Z - info: Adding new session data with id  QDateTime(2026-08-26 08:00:42.095 UTC Qt::UTC)
2026-08-26T08:03:42Z - info: Trying to send new session data
2026-08-26T08:03:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T08:03:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:03:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:03:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:04:19Z - info: Position Updated
2026-08-26T08:04:19Z - info: Position Updated at : "Wed Aug 26 2026" , "13:34:19" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:04:29Z - info: Position Updated
2026-08-26T08:04:29Z - info: Position Updated at : "Wed Aug 26 2026" , "13:34:29" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:04:42Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:04:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:05:41Z - info: System logout event
2026-08-26T08:05:41Z - critical: Stopping the websocket timers and closing websocket
2026-08-26T08:05:41Z - critical: WebSocket state changed: QAbstractSocket::ClosingState
2026-08-26T08:05:41Z - critical: retry timer for websocket is stopped
2026-08-26T08:05:41Z - critical: WebSocket state changed: QAbstractSocket::UnconnectedState
2026-08-26T08:05:41Z - info: Adding new session data with id  QDateTime(2026-08-26 08:03:42.149 UTC Qt::UTC)
2026-08-26T08:05:41Z - info: Trying to send new session data
2026-08-26T08:05:42Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T08:05:42Z - info: Desktop has changed
2026-08-26T08:05:44Z - info: Changing InputMonitor state RUNNING -> STARTING
2026-08-26T08:05:44Z - info: Unsetting mouse hook...
2026-08-26T08:05:44Z - info: Unsetting keyboard hook...
2026-08-26T08:05:44Z - info: Installing mouse hook...
2026-08-26T08:05:44Z - info: Installing keyboard hook...
2026-08-26T08:05:44Z - info: Changing InputMonitor state STARTING -> RUNNING
2026-08-26T08:05:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:06:42Z - info: Position Updated
2026-08-26T08:06:42Z - info: Position Updated at : "Wed Aug 26 2026" , "13:36:42" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:06:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:06:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:07:33Z - info: Position Updated
2026-08-26T08:07:33Z - info: Position Updated at : "Wed Aug 26 2026" , "13:37:33" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:07:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:08:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:09:43Z - info: Position Updated
2026-08-26T08:09:43Z - info: Position Updated at : "Wed Aug 26 2026" , "13:39:43" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:09:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:09:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:10:49Z - info: Position Updated
2026-08-26T08:10:49Z - info: Position Updated at : "Wed Aug 26 2026" , "13:40:49" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:10:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:11:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:12:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:12:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:12:59Z - info: Position Updated
2026-08-26T08:12:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:42:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:13:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:13:59Z - info: Position Updated
2026-08-26T08:13:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:43:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:14:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:15:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:15:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:16:09Z - info: Position Updated
2026-08-26T08:16:09Z - info: Position Updated at : "Wed Aug 26 2026" , "13:46:09" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:16:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:16:59Z - info: Position Updated
2026-08-26T08:16:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:46:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:17:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:18:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:18:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:19:09Z - info: Position Updated
2026-08-26T08:19:09Z - info: Position Updated at : "Wed Aug 26 2026" , "13:49:09" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:19:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:19:59Z - info: Position Updated
2026-08-26T08:19:59Z - info: Position Updated at : "Wed Aug 26 2026" , "13:49:59" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:20:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:21:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:21:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:22:09Z - info: Position Updated
2026-08-26T08:22:09Z - info: Position Updated at : "Wed Aug 26 2026" , "13:52:09" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:22:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  0  server message : "Exceeded the number of allotted requests in a specific time frame"
2026-08-26T08:22:49Z - critical: failed for URL:  QUrl("https://track.empmonitor.com/api/v3/user/system-info") netErrCode: QNetworkReply::AuthenticationRequiredError ,response: "{\"success\":false,\"error\":\"Exceeded the number of allotted requests in a specific time frame\",\"message\":\"Exceeded the number of allotted requests in a specific time frame\"}" ,netErrStr: "Host requires authentication"
2026-08-26T08:23:09Z - info: Position Updated
2026-08-26T08:23:09Z - info: Position Updated at : "Wed Aug 26 2026" , "13:53:09" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:23:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  0  server message : "Exceeded the number of allotted requests in a specific time frame"
2026-08-26T08:23:50Z - critical: failed for URL:  QUrl("https://track.empmonitor.com/api/v3/user/system-info") netErrCode: QNetworkReply::AuthenticationRequiredError ,response: "{\"success\":false,\"error\":\"Exceeded the number of allotted requests in a specific time frame\",\"message\":\"Exceeded the number of allotted requests in a specific time frame\"}" ,netErrStr: "Host requires authentication"
2026-08-26T08:24:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:24:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:25:20Z - info: Position Updated
2026-08-26T08:25:20Z - info: Position Updated at : "Wed Aug 26 2026" , "13:55:20" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:25:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:26:08Z - info: System login event
2026-08-26T08:26:08Z - critical: ReStarting the websocket timers and websocket connection
2026-08-26T08:26:08Z - info: Desktop has changed
2026-08-26T08:26:09Z - info: Changing InputMonitor state RUNNING -> STARTING
2026-08-26T08:26:09Z - info: Unsetting mouse hook...
2026-08-26T08:26:09Z - info: Unsetting keyboard hook...
2026-08-26T08:26:09Z - info: Installing mouse hook...
2026-08-26T08:26:09Z - info: Installing keyboard hook...
2026-08-26T08:26:09Z - info: Changing InputMonitor state STARTING -> RUNNING
2026-08-26T08:26:13Z - critical: Test url realtime  "wss://realtime.empmonitor.com"
2026-08-26T08:26:13Z - critical: WebSocket state changed: QAbstractSocket::ConnectingState
2026-08-26T08:26:13Z - critical: retry timer for websocket is stopped
2026-08-26T08:26:13Z - critical: WebSocket state changed: QAbstractSocket::ConnectedState
2026-08-26T08:26:13Z - critical: retry timer for websocket is stopped
2026-08-26T08:26:13Z - critical: connected to server
2026-08-26T08:26:13Z - critical: Message Received from server :  "Agent authenticated successfully"
2026-08-26T08:26:13Z - critical: Message Received from server :  "User connected to the dashboard, start sending the activity"
2026-08-26T08:26:14Z - info: Position Updated
2026-08-26T08:26:14Z - info: Position Updated at : "Wed Aug 26 2026" , "13:56:14" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:26:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:27:09Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:27:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:27:51Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-26T08:28:09Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:28:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:29:00Z - info: Keyboard layout changed: en-IN
2026-08-26T08:29:00Z - info: Keyboard layout changed: en-US
2026-08-26T08:29:08Z - info: Adding new session data with id  QDateTime(2026-08-26 08:26:08.766 UTC Qt::UTC)
2026-08-26T08:29:08Z - info: Trying to send new session data
2026-08-26T08:29:09Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""
2026-08-26T08:29:09Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
2026-08-26T08:29:14Z - info: Position Updated
2026-08-26T08:29:14Z - info: Position Updated at : "Wed Aug 26 2026" , "13:59:14" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:29:14Z - info: Position Updated
2026-08-26T08:29:14Z - info: Position Updated at : "Wed Aug 26 2026" , "13:59:14" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-26T08:29:49Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-26T08:30:09Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"
```

---

## 4. Layer 4 Visual Evidence Artifacts

### Evidence: `01_employee_grid_match.png`
![01_employee_grid_match.png](evidence/01_employee_grid_match.png)
Link: [01_employee_grid_match.png](evidence/01_employee_grid_match.png)

### Evidence: `02_employee_edit_modal.png`
![02_employee_edit_modal.png](evidence/02_employee_edit_modal.png)
Link: [02_employee_edit_modal.png](evidence/02_employee_edit_modal.png)

### Evidence: `03_timesheets_module.png`
![03_timesheets_module.png](evidence/03_timesheets_module.png)
Link: [03_timesheets_module.png](evidence/03_timesheets_module.png)

### Evidence: `04_keystrokes_module.png`
![04_keystrokes_module.png](evidence/04_keystrokes_module.png)
Link: [04_keystrokes_module.png](evidence/04_keystrokes_module.png)

### Evidence: `05_app_history_module.png`
![05_app_history_module.png](evidence/05_app_history_module.png)
Link: [05_app_history_module.png](evidence/05_app_history_module.png)

### Evidence: `06_web_history_module.png`
![06_web_history_module.png](evidence/06_web_history_module.png)
Link: [06_web_history_module.png](evidence/06_web_history_module.png)

### Evidence: `07_screenshots_module.png`
![07_screenshots_module.png](evidence/07_screenshots_module.png)
Link: [07_screenshots_module.png](evidence/07_screenshots_module.png)

### Evidence: `08_productivity_module.png`
![08_productivity_module.png](evidence/08_productivity_module.png)
Link: [08_productivity_module.png](evidence/08_productivity_module.png)

### Evidence: `10_screencast_module.png`
![10_screencast_module.png](evidence/10_screencast_module.png)
Link: [10_screencast_module.png](evidence/10_screencast_module.png)
