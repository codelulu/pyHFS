<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <style type="text/css">
  %style%
  </style>
  <title>HFS %folder%</title>
  <link rel="shortcut icon" href="favicon.ico" />
</head>
<body>
%login-link%
%loggedin%
%upload-link%
<div id=folderlabel>folder</div>
<div id=folder>%folder%</div>
<div id=body>
%folder-comment%
%up%
%files%
</div>
<div id=footer>
<a href="http://www.rejetto.com/hfs/">HttpFileServer %version%</a>
<br />Servertime: %timestamp%
<br />Uptime: %uptime%
<br />Build-time: %build-time%
</div>
</body>
</html>

[style]
body, th { font-family:tahoma, verdana, arial, helvetica, sans; font-weight:normal; font-size:9pt; }
body { margin:0; background-color:#DDF; padding:10px; }
p { margin:0 }
a { text-decoration:none;  background-color:Transparent; color:#05F; }
a:visited { color:#55F; }
a:hover { background-color:#EEF; }
img { border-style:none }
td { font-size:10pt; background:#FFF; border:1px solid #BBF }
td img { vertical-align:top }
th, th a, th a:visited { color:#555; font-size:13pt; font-weight:bold; padding-bottom:0; }
#foldercomment { font-size:10pt; color:#888; background:#EEE; padding:3px; border:1px solid #DDD; border-bottom:3px solid #DDD; margin-top:2px; }
#tools { text-align:right; font-size: 8pt; }
#folder, .big { font-size:14pt; font-weight:bold;  }
#folderlabel, #folderstats, #footer { font-size: 8pt; }
#body {
  border-bottom: 4px solid #BBF;
     border-top: 4px solid #BBF;
    border-left: 1px dotted #BBF;
   border-right: 1px dotted #BBF;
  background:#F3F3FF;
  padding:15px;
  margin:15px;
}
.comment { font-size:7pt; color:#888; background:#EEE; padding:3px; border:1px solid #DDD; margin-top:2px; }
.button { float:right; padding:5px; padding-top:7px; margin:15px; border:2px solid black; background:white; font-size:8pt; font-weight:bold; }
.button img { vertical-align:text-bottom; }
.flag { font-weight:bold; font-size:8pt; background:white; color:red; text-align:center; border:1px solid red; }

[login-link]
<a href="~login" class=button><img src="/~img27" /> LOGIN</a>

[loggedin]
<span class=button><img src="/~img27" /> user: %user%</span>

[upload-link]
<a href="~upload" class=button><img src="/~img32" /> UPLOAD</a>

[up]
<a class=big href=".."><img src="/~img14" /> UP</a>

[nofiles]
<div class=big>No file</div>

[files]
<div id=folderstats>%number-folders% folders,  %number-files% files - Total: %total-size%</div>
<table cellpadding=5>
<th><a href="?sort=n">Filename</a>
<th><a href="?sort=s">Filesize</a>
<th><a href="?sort=t">Filetime</a>
<th><a href="?sort=d">Hits</a>
%list%
</table>
<div id=tools>
<a href="~files.lst?recursive">File list</a>
%archive%
</div>

[archive]
<br><a href="~folder.tar?recursive">Folder archive</a>

[protected]
<img src='/~img_lock'>

[file]
<tr><td>%new% %protected% <a href="%item-url%"><img src="/~img_file" /> %item-name%</a>%comment%<td align=right>%item-size%<td align=right>%item-modified%<td align=right>%item-dl-count%

[folder]
<tr><td>%new% %protected% <a href="%item-url%"><img src="/~img_folder" /> <b>%item-name%</b></a>%comment%<td align=center><i>folder</i><td align=right>%item-modified%<td align=right>%item-dl-count%

[link]
<tr><td>%new% <a href="%item-url%"><img src="/~img_link" /> <b>%item-name%</b></a>%comment%<td colspan=3 align=center><i>link</i>

[comment]
<div class=comment>%item-comment%</div>

[folder-comment]
<div id=foldercomment>%item-comment%</div>

[error-page]
<html>
  <head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <style>
    %style%
    </style>
  </head>
<body>
%content%
<hr>
<div style="font-family:tahoma, verdana, arial, helvetica, sans; font-size:8pt;">
<a href="http://www.rejetto.com/hfs/">HttpFileServer %version%</a>
<br />%timestamp%
</div>
</body>
</html>

[not found]
<h1>404 -  Not found</h1>
<a href="/">go to root</a>

[overload]
<h1>Server busy</h1>
Please, retry later.

[max contemp downloads]
<h1>Download limit</h1>
On this server there is a limit on the number of <b>simultaneous</b> downloads.
<br />This limit has been reached. Retry later.

[unauthorized]
<h1>Unauthorized</h1>
This is a protected resource.
<br />Your username/password doesn't match.

[deny]
<h1>Unallowed</h1>
This resource is not accessible.

[ban]
<h1>You are banned.</h1>
%reason%

[upload]
<html>
<head>
  <title>HFS %folder%</title>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <style type="text/css">
  %style%
  </style>
</head>
<body>
%login-link%
%loggedin%
<script language="javascript">
var s1, s2;
if (window.parent.progress) s1 = '" target=_parent', s2 = 'CLOSE';
else s1 = '+progress"', s2= 'ADD';
document.write('<a href="~upload'+s1+' class=button onClick="if (frm.upbtn.disabled) return false;"><img src="/~img10" /> '+s2+' PROGRESS FRAME</a>');
</script>
<a href="." target=_parent class=button><img src="/~img21" /> CANCEL UPLOAD</a>
<div style="margin-top:60px" id=folderlabel>folder</div>
<div id=folder>%folder%</div>
<div id=body>
<form name=frm action="." target=_parent method=post enctype="multipart/form-data" onSubmit="frm.upbtn.disabled=true; return true;">
%upload-files%
<input name=upbtn type=submit value="Upload files">
</form>
<br />Before uploading you may want to open a <a target=_blank href="/~progress">progress status window</a>.
</div>
<div id=footer>
<a href="http://www.rejetto.com/hfs/">HttpFileServer %version%</a>
<br />Servertime: %timestamp%
<br />Uptime: %uptime%
<br />Disk space: %diskfree%
</div>
</body>
</html>

[upload-file]
<input name=fileupload%idx% size=70 type=file><br />

[upload-results]
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <style type="text/css">
  %style%
  </style>
  <title>HFS %folder%</title>
</head>
<body>
%loggedin%
<div style="margin-top:60px" id=folderlabel>folder</div>
<div id=folder>%folder%</div>
<div id=body>
%uploaded-files%
<br /><br />
<a href="." target=_parent class=big><img src="/~img14" /> Back to the folder</a>
</div>
<div class=footer>
<a href="http://www.rejetto.com/hfs/">HttpFileServer %version%</a>
<br />Servertime: %timestamp%
<br />Uptime: %uptime%
<br />Disk space: %diskfree%
</div>
</body>
</html>

[upload-success]
<li><a href='%item-url%'>%item-name%</a>: <b>OK</b> --- %item-size%  (Speed %speed% KB/s)

[upload-failed]
<li>%item-name%: <b>FAILED</b> ---  %reason%

[upload+progress]
<html>
<head>
<frameset cols=200,*>
  <frame name=progress src="/~progress" scrolling=auto marginwidth=0>
  <frame src="~upload-no-progress" scrolling=auto>
</frameset>
</head>
<body>
</body>
</html>

[progress]
<html>
<head>
  <meta http-equiv="Refresh" content="7;URL=/~progress">
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <title>HFS - Progress status</title>
  <style>
  %style%
  .filename { font-weight:bold; font-size:8pt; }
  .bytes { font-size:7pt; }
  .perc { font-size:14px; vertical-align:middle; }
  .out_bar { width:100px; font-size:15px; background:black; border:black 1px solid; margin-right:5px; float:left; }
  .in_bar { height:16px; background:white; color:white;  }
  #body { margin-left:0; margin-right:0; }
  body { padding:2px; }
  #graph { border:white outset 2px; }
  </style>
</head>
<body>
<div class=big>Progress status</div>
Auto-refresh: 7 seconds
<br /><br /><img src="/~img_graph190x40" id="graph" />
<div id=body>
%progress-files%
</div>
<div id=footer>Uptime: %uptime%</div>
</body>
</html>

[progress-nofiles]
<div class=big>No file exchange in progress.</div>

[progress-upload-file]
<span class=flag>&nbsp;up&nbsp;</span>
<span class=filename>%filename%</span>
<div class=bytes>
%done-bytes% / %total-bytes% bytes
<br />Speed: %speed-kb% KB/s
</div>
<div style="margin-top:5px; margin-bottom:20px;">
  <div class=out_bar><div class=in_bar style="width:%perc%px"></div></div> <span class=perc>%perc%%</span>
</div>

[progress-download-file]
<span class=flag>&nbsp;down&nbsp;</span>
<span class=filename>%filename%</span>
<div class=bytes>
%done-bytes% / %total-bytes% bytes
<br />Speed: %speed-kb% KB/s
</div>
<div style="margin-top:5px; margin-bottom:20px;">
  <div class=out_bar><div class=in_bar style="width:%perc%px"></div></div> <span class=perc>%perc%%</span>
</div>

[newfile]
<span class=flag>&nbsp;NEW&nbsp;</span>
