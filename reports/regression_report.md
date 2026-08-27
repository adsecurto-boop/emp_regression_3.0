# EmpMonitor 3.0 Automated Regression Test Report

## 1. Execution Metadata Summary

- **Date & Time**: `2026-08-27 09:36:05`
- **Target Environment**: `DEV`
- **Agent Version Evaluated**: `3.5.0`
- **Local Active Host Email (L1)**: `autotest@gmail.com`
- **Searched Dashboard User (L4)**: `auto test`
- **Dashboard Registered Email (L4)**: `autotest@empmonitor.com`
- **Cross-Environment Leak Check**: `LEAK DETECTED` (CRITICAL LEAK: 1 invalid environment reference(s) found)
- **Screencast Stream Status (L4)**: `STANDBY`
- **Final System Verdict**: **`FAILED`**

### ⚠️ Discrepancy Warnings

- 🔴 **[DISCREPANCY]**: Network Connectivity Blocked: TCP handshake failed for activity.dev.emmonitor.com
- 🔴 **[DISCREPANCY]**: Network Routing Cross-Environment Leak: CRITICAL LEAK: Live production endpoint detected in Dev agent configuration (service.empmonitor.com - Live production service endpoint)!
- 🔴 **[DISCREPANCY]**: Email Discrepancy Mismatch! Local Host Email ('autotest@gmail.com') != Dashboard Email ('autotest@empmonitor.com')

---

## 2. Layer 1 System Configuration Audit

- **Local INI Path**: `C:\Users\GBSBHL1261\AppData\Roaming\screen\OjUxFCN\empm.ini`
- **INI File Size**: `4.47 KB` (EV-001 Requirement: > 3.0 KB)

### Binary Presence & Running Process Status

- **Binary `empmonitor.exe`**: MISSING
- **Binary `UpdateMgr_Emp.exe`**: MISSING
- **Binary `esr.exe`**: MISSING
- **Binary `emp_psa_service.exe`**: MISSING
- **Process `empmonitor.exe`**: INACTIVE
- **Process `updatemgr_emp.exe`**: INACTIVE
- **Process `esr.exe`**: INACTIVE
- **Process `emp_psa_service.exe`**: INACTIVE

### Sanitized `config.js` Contents (Masked)
```json
Not Found
```

### Sanitized `empm.ini` Attributes (Masked)
```ini
last_sync_time = @DateTime(\0\0\0\x10\0\0\0\0\0\0%\x8e`\x2\xe\xbb\xa5\0)
currentdate = @Variant(\0\0\0\xe\0%\x8e`)
datasendingperiodsec = 180
lastsettingsaccessdatetime = @DateTime(\0\0\0\x10\0\0\0\0\0\0%\x8e`\0\xe1>\xf9\x1)
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
data\features\screencast = 1
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
data\screen_record\audio = 0
data\screen_record\is_enabled = 0
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
data\tracking\domain\appblocklist = 
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
data\tracking\domain\websiteblocklist = @Variant(\0\0\0\t\0\0\0\x1\0\0\0\n\0\0\0 \0w\0w\0w\0.\0\x66\0\x61\0\x63\0\x65\0\x62\0o\0o\0k\0.\0\x63\0o\0m)
data\tracking\geolocation = @Invalid()
data\tracking\keystrokepolicymode = *******
data\tracking\networkbased = @Invalid()
data\tracking\projectbased = @Invalid()
data\tracking\unlimited\day = "1,2,3,4,5,6,7"
data\trackingmode = unlimited
data\usbdisable = 0
data\userblock = 0
data\webcam\frequencyperhour = 1
error = @Variant(\0\0\0\x94)
message = User configs
```

---

## 3. Layer 3 (L3) - Outbound Network & Firewall Audit

- **Target Routing Environment:** `dev`
- **Active Firewall Exceptions:**
  - `empmonitor.exe`: `Allowed (Default Outbound Policy)`
  - `UpdateMgr_Emp.exe`: `Allowed (Default Outbound Policy)`
  - `esr.exe`: `Allowed (Default Outbound Policy)`
  - `emp_psa_service.exe`: `Allowed (Default Outbound Policy)`
- **API Connectivity Matrix:**
  - `track.dev.empmonitor.com`: `SUCCESS (Resolved IP: 140.245.4.33)`
  - `activity.dev.emmonitor.com`: `BLOCKED ([Errno 11001] getaddrinfo failed)`
  - `remote-dev.empmonitor.com`: `SUCCESS (Resolved IP: 140.245.4.33)`
  - `service.dev.empmonitor.com`: `SUCCESS (Resolved IP: 140.245.4.33)`
  - `updates.empmonitor.in`: `SUCCESS (Resolved IP: 129.154.230.99)`
- **Leak Integrity check:** `LEAK DETECTED (CRITICAL LEAK: 1 invalid environment reference(s) found)`

---

## 4. Layer 2 Host Log Harvest (Last 200 Lines)

```text
2026-08-27T03:33:54Z - critical: > Driver error: ""

2026-08-27T03:33:54Z - critical: > Native error code: ""

2026-08-27T03:33:54Z - critical: > Error type 0

2026-08-27T03:34:14Z - info: Requesting for url : /auth/authenticate   Reply code : 0  server message : ""  error message : ""

2026-08-27T03:34:14Z - info: Changing tracking mode from " initial " to " "unlimited" "
2026-08-27T03:34:14Z - info: DB opened
2026-08-27T03:34:14Z - warning: QObject: Cannot create children for a parent that is in a different thread.
(Parent is activity_tracker::ui::qt::NetworkAccessManager(0x1ec8a7ffcc0), parent's thread is QThread(0xd721b0f880), current thread is QThread(0x1ec867c7ac0)
2026-08-27T03:34:14Z - critical: thisApp()->m_isLogoutEnabled in worker  true
2026-08-27T03:34:14Z - info: Setting the logout btn visility to true
2026-08-27T03:34:14Z - critical: QJsonArray(["www.facebook.com"])
2026-08-27T03:34:14Z - info: Exclude website list (data/tracking/domain/excludeWebsiteList): ()
2026-08-27T03:34:14Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-27T03:34:14Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/me"  Reply code :  200  server message : "Logged in user"
2026-08-27T03:34:14Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"
2026-08-27T03:34:17Z - info: > Installing AppAndBrowser monitor hook...

2026-08-27T03:34:17Z - info: Creating InputMonitorManager

2026-08-27T03:34:17Z - info: Creating InputMonitor

2026-08-27T03:34:17Z - info: Inside thread

2026-08-27T03:34:17Z - info: Entered InputMonitor run thread

2026-08-27T03:34:17Z - info: Dummy window created

2026-08-27T03:34:17Z - info: Keyboard layout changed: en-US

2026-08-27T03:34:17Z - info: Installing mouse hook...

2026-08-27T03:34:17Z - info: Installing keyboard hook...

2026-08-27T03:34:17Z - info: Changing InputMonitor state STARTING -> RUNNING

2026-08-27T03:34:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:35:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:35:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:36:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:36:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:36:48Z - info: Position Updated

2026-08-27T03:36:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:06:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:36:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"

2026-08-27T03:37:16Z - info: Adding new session data with id  QDateTime(2026-08-27 03:34:16.079 UTC Qt::UTC)

2026-08-27T03:37:16Z - info: Trying to send new session data

2026-08-27T03:37:16Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""

2026-08-27T03:37:16Z - info: Memory Usage : 16.4883 MB

2026-08-27T03:37:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:37:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:38:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:38:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:39:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:39:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:39:48Z - info: Position Updated

2026-08-27T03:39:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:09:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:39:48Z - info: Position Updated

2026-08-27T03:39:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:09:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:39:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"

2026-08-27T03:40:16Z - info: Adding new session data with id  QDateTime(2026-08-27 03:37:16.080 UTC Qt::UTC)

2026-08-27T03:40:16Z - info: Trying to send new session data

2026-08-27T03:40:16Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""

2026-08-27T03:40:16Z - info: Memory Usage : 17.3203 MB

2026-08-27T03:40:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:40:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:41:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:41:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:42:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:42:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:42:48Z - info: Position Updated

2026-08-27T03:42:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:12:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:42:48Z - info: Position Updated

2026-08-27T03:42:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:12:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:42:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"

2026-08-27T03:43:16Z - info: Adding new session data with id  QDateTime(2026-08-27 03:40:16.080 UTC Qt::UTC)

2026-08-27T03:43:16Z - info: Trying to send new session data

2026-08-27T03:43:16Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""

2026-08-27T03:43:16Z - info: Memory Usage : 17.2891 MB

2026-08-27T03:43:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:43:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:44:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:44:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:45:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:45:48Z - info: Position Updated

2026-08-27T03:45:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:15:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:45:48Z - info: Position Updated

2026-08-27T03:45:48Z - info: Position Updated at : "Thu Aug 27 2026" , "09:15:48" , Latitude:  21.2013 ,  Longitude:  81.3239

2026-08-27T03:45:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:45:50Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"

2026-08-27T03:46:16Z - info: Adding new session data with id  QDateTime(2026-08-27 03:43:16.152 UTC Qt::UTC)

2026-08-27T03:46:16Z - info: Trying to send new session data

2026-08-27T03:46:16Z - info: Requesting for add-activity   Reply code : 200  server message : "Data saved"  error message : ""

2026-08-27T03:46:16Z - info: Memory Usage : 17.2539 MB

2026-08-27T03:46:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"

2026-08-27T03:46:48Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info is already the latest"

2026-08-27T03:47:16Z - warning: Could not get the INetworkConnection instance for the adapter GUID.

2026-08-27T03:47:16Z - info: Requesting url :  "https://storelogs.dev.empmonitor.com/api/v1/desktop/upload-screenshots"  Reply code :  0  server message : "Successfully screenshot uploaded"



!!!!!!!!! Application started at Thu Aug 27 03:47:17 2026 GMT UTC time

2026-08-27T03:47:17Z - info: Changing tracking mode from " initial " to " "unlimited" "
2026-08-27T03:47:17Z - critical: thisApp()->m_isLogoutEnabled in settings  true
2026-08-27T03:47:17Z - info: QVariant(QString, "Allow")
2026-08-27T03:47:17Z - info: QVariant(QString, "Allow")
2026-08-27T03:47:17Z - info: Shared key "emp_monitor_shared_memory_for_user_GBSBHL1261"
2026-08-27T03:47:17Z - info: Setting shared key
2026-08-27T03:47:17Z - info: Assigning registry value
2026-08-27T03:47:17Z - info: Registering instances
2026-08-27T03:47:17Z - info: Worker thread instance
2026-08-27T03:47:17Z - info: Network thread instance
2026-08-27T03:47:17Z - critical: Trying to get watchdog service
2026-08-27T03:47:17Z - warning: QWidget::setLayout: Attempting to set QLayout "" on QStackedWidget "", which already has a layout
2026-08-27T03:47:17Z - info: VERSION:  3.0.1
2026-08-27T03:47:17Z - info: Setting the logout btn visility to true
2026-08-27T03:47:18Z - warning: QCssParser::parseHexColor: Unknown color name '#solid'
2026-08-27T03:47:18Z - warning: Could not parse application stylesheet
2026-08-27T03:47:17Z - info: Setting network thread
2026-08-27T03:47:17Z - info: Setting worker thread
2026-08-27T03:47:17Z - warning: serialnmea: No known GPS device found. Specify the COM port via QT_NMEA_SERIAL_PORT.
2026-08-27T03:47:17Z - info: DB opened
2026-08-27T03:47:17Z - info: Last application was not closed properly and last clock data staretd at  QDateTime(2026-08-27 03:34:16.076 UTC Qt::UTC)  is not closed properly.
2026-08-27T03:47:17Z - info: Find the time of prevous app shutdown.  QDateTime(2026-08-27 03:47:16.049 UTC Qt::UTC)
2026-08-27T03:47:17Z - info: recovering not closed clock data  QDateTime(2026-08-27 03:34:16.076 UTC Qt::UTC)  from previous app
2026-08-27T03:47:17Z - info: Position Updated
2026-08-27T03:47:17Z - info: Position Updated at : "Thu Aug 27 2026" , "09:17:17" , Latitude:  21.2013 ,  Longitude:  81.3239
2026-08-27T03:47:17Z - warning: Could not get the INetworkConnection instance for the adapter GUID.
2026-08-27T03:47:17Z - warning: Could not get the INetworkConnection instance for the adapter GUID.
2026-08-27T03:47:17Z - critical: thisApp()->m_isLogoutEnabled in worker  true
2026-08-27T03:47:17Z - critical: QJsonArray(["www.facebook.com"])
2026-08-27T03:47:17Z - info: Exclude website list (data/tracking/domain/excludeWebsiteList): ()
2026-08-27T03:47:17Z - info: timerForStorageDevice started
2026-08-27T03:47:17Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/config"  Reply code :  200  server message : "User configs"
2026-08-27T03:47:17Z - info: Requesting url :  "https://track.empmonitor.com/api/v3/user/system-info"  Reply code :  200  server message : "User system info"
2026-08-27T03:47:18Z - warning: Could not get the INetworkConnection instance for the adapter GUID.
2026-08-27T03:47:18Z - critical: Skipping the non-removable device:  "C:/"
```

---

## 5. Layer 4 Visual Evidence Artifacts

### Evidence: `01_employee_grid_match.png`
![01_employee_grid_match.png](evidence/01_employee_grid_match.png)
Link: [01_employee_grid_match.png](evidence/01_employee_grid_match.png)
