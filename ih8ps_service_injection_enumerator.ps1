<#
# I hate PowerShell Service Enumerator
# (C) Macarthur Inbody AGPLv3 2020
# The primary purpose of this script is to find all services where you're able 
# to modify it to do DLL injection and the service you're attacking is run as 
#SYSTEM user. Further it'll make sure that your user is able to do this.
# It'll give you a list of all of the possible services at the end reducing
# your search space.
# Basically it's looking for services where the listed user is in the ACL, that they have full control.
# It's also making sure we have the ability to modify things.
# The one thing it doesn't do is modify the registry settings.
#>
param([String]$user="User")

function get_vuln_services($user){
<#
1)This line takes all items from the services hive, 
2) formats it to a list. 
3) Then it looks for the string HKEY_LOCAL_MACHINE
4) then finds the strings that have "Name " in their line
5) Then it Enumerates over each item splitting the string by the ":". 
6) Then I remove the HKEY_LOCAL_MACHINE prefix.
7) Then it sets the value to be the variable $services.
#>
$services=(Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services' | Get-ItemProperty -name ServiceSidType, ObjectName -ErrorAction SilentlyContinue | Where-Object { $_.ServiceSidType -eq 1 -and $_.ObjectName -eq 'LocalSystem' } | findstr "PSChildName" | foreach-object {$_.split(':')[1].substring(1)});
	#Some variable intializations.
	$current_acl=''
	$command=''
	$split_len=0
	# I go through line by line through the services string. I split it on the newline barrior.
	ForEach ($service in $($services -split "`r`n")){
		<# 
		 # This line does the following.
		 # 1) get the ACL information from the registry hive service listed by $line.
		 # 2) pipes it to format-list
		 # 3) finds the string "Hector"(our user's name) in it.
		 # If it doesn't we don't match anything.
		#>
		$current_acl=(get-acl " HKLM:\SYSTEM\CurrentControlset\services\$service"| format-list | findstr "$user")
		#Check to make sure that it has the word Full in it.
		if ($current_acl -match "Full"){
			<#
			# This line does the following via compound if statements.
			# 1) run sc.exe qc "$service"
			# Our service we're looking for.
			# 2) find the string "denied" in it.
			# 3) Negate whatever the result is.
			# So if it's no found it converts it to true.
			# 5) also check the second set.
			# 6) run the service query configuration again.
			# 7) look for the string "DEMAND_START"
			# 8) If it all works we go onto the next line.
			#>
			<#
			# Basically we make sure that we're able to access the service and have the ability to modify things.
			# then we make sure that it's not one that's already running. Then we tell the user that it's something interesting.
			#>
			if(!(sc.exe qc "$service" | findstr 'denied') -and (sc.exe qc "$service" | findstr "DEMAND_START")){
				#"echo" out the line telling us to look into this service.
				Write-Host "Look into this one. '$service'"
			}
		}
	}
}
get_vuln_services($user)
