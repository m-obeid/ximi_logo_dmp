
![Logo](https://raw.githubusercontent.com/m-obeid/ximi_logo_dmp/main/icon.ico)


#### 🔗 Links

[![download](https://img.shields.io/static/v1?label=download&message=latest&color=success&style=for-the-badge&logo=github)](https://www.github.com/m-obeid/ximi_logo_dmp/archive/main.zip)
[![youtube](https://img.shields.io/youtube/channel/subscribers/UC6h62_q0jJfn8kgiP39q0GQ?label=SUBSCRIBE&logo=youtube&style=for-the-badge)](https://www.youtube.com/@pocoguy)
[![tiktok](https://img.shields.io/static/v1?label=TikTok&message=@pocoguy.exe&color=ee1d52&style=for-the-badge&logo=tiktok)](https://www.tiktok.com/@pocoguy.exe)
[![website](https://img.shields.io/static/v1?label=My%20Website&message=POCO.GA&color=black&style=for-the-badge&logo=html5)](https://www.tiktok.com/@pocoguy.exe)
# 📱 ximi_logo_dmp
Universal Xiaomi Logo Tool tested on several firmwares and physically on the POCO F1.

The name "ximi" is basically Xiaomi but also a reference to the TikTok device naming scheme for Xiaomi, popular in the TechTok community. Hilarious idea but yeah, lmao.
## 🧑🏽‍💻 Authors

- GitHub: [@m-obeid](https://www.github.com/m-obeid)


## ⚠️ Note (for legal reasons)

I do not own the Xiaomi mascot Mitu and am not affiliated with Xiaomi in any way.

I'M NOT RESPONSIBLE FOR BRICKED PHONES, YOU GETTING FIRED BECAUSE THE ALARM DIDN'T WORK OR ANY DAMAGE CAUSED BY THIS TOOL. 
YOU ARE ADVISED TO VERIFY THE INTEGRITY OF THE FINAL PACKAGE MANUALLY, EVEN WHEN THIS TOOL VERIFIES IT,
BEFORE FLASHING IT TO YOUR DEVICE! YOU DECIDED TO DO THIS; BLAME YOURSELF FOR NOT BEING CAREFUL ENOUGH.
## 📥 Installation & How to use

Download this repository as ZIP and extract to folder. Run Terminal or Command Prompt in it. If you are on Windows, also download platform-tools and extract to the program folder.

Now do these steps to use it properly:
- Make sure your device is connected to your computer, USB debugging is enabled, bootloader is unlocked and optionally rooted.
  - When no root, make sure you at least have TWRP recovery.
  - Your device should be booted into system.

- Run this command in the logo_dmp command prompt / terminal window:
  ```bash
  ./logo_dmp dump
  ```
- Wait until it finishes the process.

- Now that we have either an logo.img or splash.img in our folder, let's unpack it:
  ```bash
  ./logo_dmp unpack logo.img
  ```
  or
  ```bash
  ./logo_dmp unpack splash.img
  ```
  - This will create BMP files in our folder. Edit them to your liking, but there are some rules:
    - The image must stay in the same resolution, 24bpp, BMP format, or it might not work.
    - Don't rename the files. The program expects to find the files in the correct order later, so make sure every image has it's name.
- So we finally made our cool boot logo, so let's actually install it for the _uniqueness_ 😎:
  ```bash
  ./logo_dmp rebuild logo.img
  ```
  or
  ```bash
  ./logo_dmp rebuild splash.img
  ```
  - This will create a new logo.img aka. splash.img, which you can flash in `fastboot` mode using:
    ```bash
    fastboot flash logo logo_new.img
    ``` 
    or
    ```bash
    fastboot flash splash splash_new.img
    ``` 
  - Tip: use an hex editor to compare the files. every BMP file header should start at the same location as it's original one, and the size should be the same.
- If you restart your device, and everything goes well, it should work. If it doesn't, then your phone might be bricked on the low level bootloader now 💀

This tool has been tested several times using a few samples of logo.img and splash.img, and seems to work. I'm still a bit insecure so make sure to manually check ...
## ❓ FAQ

#### Can I share the logo.img / splash.img files?

Yes, but note that the format is model specific, sometimes firmware version specific, and it's recommended to only share your BMPs for them to build their own versions

#### Does this work on any device?

I'm not sure, but it seems to be the case.


## 📱 My Logo

I made a Ximi logo for my device. Here you can download my BMP files.

[![portfolio](https://img.shields.io/badge/XimiLogo_beryllium-anonfiles.com-000?style=for-the-badge)](https://anonfiles.com/H9o7J5P7y5/XimiLogo_beryllium_zip)
