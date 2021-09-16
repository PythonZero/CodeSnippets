# Authenticate as yourself

```bash
gcloud auth application-default login
```

Once you've authenticated as yourself, you can use the account credentials it generated 
* Mac - `~/.config/gcloud/application_default_credentials.json`
* Windows - `C:\Users\your_username\AppData\Roaming\gcloud`)
* The location where it is generated is printed in the terminal after you log in successfully 

Debug code
```
ssh -i "path/to/.pub" -R 12345:localhost:12345 ubuntu:192.168.0.1
```
