"""Create desktop shortcut for the dashboard"""
import os
import pythoncom
import win32com.client

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
target = r'D:\抖音剪辑账号\仪表盘.html'
shortcut_path = os.path.join(desktop, '剪辑选题系统.lnk')

shell = win32com.client.Dispatch("WScript.Shell")
sc = shell.CreateShortcut(shortcut_path)
sc.TargetPath = target
sc.IconLocation = r'C:\Windows\System32\imageres.dll,195'
sc.WorkingDirectory = r'D:\抖音剪辑账号'
sc.Description = '拍摄+剪辑教学 · 每日选题仪表盘'
sc.Save()

if os.path.exists(shortcut_path):
    print(f'OK: {shortcut_path}')
else:
    print('FAILED')
