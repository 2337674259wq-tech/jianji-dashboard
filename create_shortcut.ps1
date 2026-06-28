$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop '剪辑选题系统.lnk'
$targetPath = 'D:\抖音剪辑账号\仪表盘.html'

$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.IconLocation = 'C:\Windows\System32\imageres.dll,195'
$shortcut.WorkingDirectory = 'D:\抖音剪辑账号'
$shortcut.Description = '拍摄+剪辑教学 · 每日选题仪表盘'
$shortcut.Save()

Write-Output "OK: $shortcutPath"
