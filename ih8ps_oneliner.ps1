<#
# I hate PowerShell Service Enumerator
# (C) Macarthur Inbody AGPLv3 2020
# This script will enumerate through services finding one where you have
# the ability to start it and also are able to change where the image is stored.
# Not a great script. But it works.
# Basically it's looking for services where the listed user is in the ACL, that they have full control.
# It's also making sure we have the ability to modify things.
# The one thing it doesn't do is modify the registry settings.
#>
#oneliner version.
#make sure to set $user at the front of the script to the user you want to target.
$user="User";$services=(Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services' | Get-ItemProperty -name ServiceSidType, ObjectName -ErrorAction SilentlyContinue | Where-Object { $_.ServiceSidType -eq 1 -and $_.ObjectName -eq 'LocalSystem' } | findstr "PSChildName" | foreach-object {$_.split(':')[1].substring(1)});$current_acl='';$command='';$split_len=0;ForEach ($service in $($services -split "`r`n")){$current_acl=(get-acl "HKLM:\SYSTEM\CurrentControlSet\Services\$service"| format-list | findstr 'Hector');if ($current_acl -match "Full"){if(!(sc.exe qc "$service" | findstr 'denied') -and (sc.exe qc "$service" | findstr "DEMAND_START")){Write-Host "Look into this one. '$service'";}}}

