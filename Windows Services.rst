How to Create a Windows Service
==================================

https://www.iceflatline.com/2015/12/run-a-windows-application-as-a-service-with-srvany/

1) Download Windows Server 2003 Resource Kit Tools
    (https://www.microsoft.com/en-us/download/details.aspx?id=17657)
2) Install it & remember where the path is (Default: C:\Program Files (x86)\Windows Resource Kits\Tools )
3) Create the service
   ``C:\Program Files (x86)\Windows Resource Kits\Tools>"C:\Program Files (x86)\Windows Resource Kits\Tools\instsrv.exe" 
   "Django MyWebsite" "C:\Program Files (x86)\Windows Resource Kits\Tools\srvany.exe"`` 
   
   where you replace ``"Django MyWebsite"`` with the name of the service
   note, it needs the full/path/to/instsrv & srvany.exe 
4) Open the Registry Editor (``Regedit.exe``)
5) Go to ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\<My Service>``
6) Right Click (or edit at the top) -> New -> Key
      ``Key Name: Parameters``
      ``Class: <leave it blank>``
7) Go into the Parameters Key (should create a sub folder)
8) Right Click -> New -> String Value 
      ``Name: Application``
      ``Data: <your script to run the program>``  
      e.g. ``Data: C:\ProgramData\Anaconda3\python.exe C:\path\to\script.py var1 var2``
9) Close the Registry Editor
10) Go to the services page, and change the settings (I.e. run automatically at startup, which log in credentials to use, 
    what to do if failure etc.)
