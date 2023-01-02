# ximi_logo_dmp v1 - by pocoguy
# some parts of this code were actually generated by chatgpt

import struct
import os
import sys
from subprocess import PIPE, Popen

HELP_INSTRUCTIONS = """
    [1] it MUST be saved as an BMP 24bpp image, as it is right now.
    [2] it MUST have the same resolution as the original.
    [3] it MUST have the same file name this program saved it as.

Note (for legal reasons): 
I'M NOT RESPONSIBLE FOR BRICKED PHONES, YOU GETTING FIRED BECAUSE THE ALARM DIDN'T WORK OR ANY DAMAGE CAUSED BY THIS TOOL. YOU ARE ADVISED TO VERIFY THE INTEGRITY OF THE FINAL PACKAGE MANUALLY, EVEN WHEN THIS TOOL VERIFIES IT, BEFORE FLASHING IT TO YOUR DEVICE! YOU DECIDED TO DO THIS; BLAME YOURSELF FOR NOT BEING CAREFUL ENOUGH

If something seems wrong with the logo files, DO NOT USE!"""

def unpack(filename):
    file_size = os.path.getsize(filename)

    # Open the binary file in read-only mode
    with open(filename, "rb") as file:
        # Initialize a counter for the image file names
        counter = 1

        # Loop until the end of the file is reached
        while True:
            # Read the BMP header (14 bytes)
            header = file.read(14)

            # Check for repeating back and forth (also means end has been reached)
            if file.tell() > file_size - 13:
                break

            # If the header is not present, the end of the file has been reached
            if not header:
                break
            
            # Check if the header is a valid BMP header
            if header[:2] == b'BM':
                # Extract the individual fields of the BMP header
                magic, size, reserved1, reserved2, offset = struct.unpack("<2sIHHI", header)

                hdict = {
                    "magic": magic,
                    "size": size,
                    "reserved1": reserved1,
                    "reserved2": reserved2,
                    "offset": offset,
                    "position": file.tell()
                }

                # Log the header information in a human-readable format
                print(f"dumping image_{counter}.bmp - header: {hdict}")

                # Read the rest of the BMP image data
                image_data = file.read(size - 14)

                # Save the image data to a file
                with open(f"image_{counter}.bmp", "wb") as image_file:
                    image_file.write(header + image_data)

                # Increment the counter for the next image file name
                counter += 1
            else:
                # If the header is not a valid BMP header, seek to the start of the next header
                file.seek(-13, 1)
        print("-------------")
        print("Extracted successfully! Please keep in mind that for the logo to work after rebuilding:")
        print(HELP_INSTRUCTIONS)

def rebuild(original, filename):
    o_file_size = os.path.getsize(original)
    image_data = []
    finished = False

    # Create a new copy of the original to override.
    # Why not just create a new one? For some reasons,
    # my POCO F1's files contained a battery icon PNG file
    # and to keep such things, I'm going to just override a copy of the original.
    with open(filename, "wb") as file:
        with open(original, "rb") as ofile:

            # Copy bytes from original to new file

            ofile.seek(0)
            file.write(ofile.read())
            ofile.seek(0)
            file.seek(0)

            # Initialize a counter for the image file names
            counter = 1

            # Loop until the end of the file is reached
            while True:
                # Read the BMP header (14 bytes)
                header = ofile.read(14)

                # Check for repeating back and forth (also means end has been reached)
                if ofile.tell() > o_file_size - 13:
                    break

                # If the header is not present, the end of the file has been reached
                if not header:
                    break
                
                # Check if the header is a valid BMP header
                if header[:2] == b'BM':
                    # Extract the individual fields of the BMP header
                    magic, size, reserved1, reserved2, offset = struct.unpack("<2sIHHI", header)

                    # Save the information extracted from the header
                    image_data.append({
                        "magic": magic,
                        "size": size,
                        "reserved1": reserved1,
                        "reserved2": reserved2,
                        "offset": offset,
                        "position": ofile.tell()
                    })

                    # Read the rest of the BMP image data (for no real reason)
                    ofile.read(size - 14)

                    # Increment the counter for the next image file name
                    counter += 1
                else:
                    # If the header is not a valid BMP header, seek to the start of the next header
                    ofile.seek(-13, 1)

            # Write the header from the original file to the new one
            ofile.seek(0)
            file.write(ofile.read(image_data[0]["position"] - 14))

            # Check if all files are available and validate before patch
            # Also add to image buffer which will be used instead of the files directly

            image_buf = []
            image_id = 1

            for img in image_data:
                image_fname = f'image_{image_id}.bmp'
                print(f"current image: {img}")
                if os.path.isfile(image_fname):
                    image_fsize = os.path.getsize(image_fname)
                    missing_bytes = b''
                    if (image_fsize > img["size"]):
                        overflow_bytes = image_fsize - img["size"]
                        print(f"ERROR: bitmap file {image_fname} is {overflow_bytes} bytes too big to fit. Make sure you saved as an 24bpp BMP and with the correct resolution!")
                        finished = False
                        break
                    if (image_fsize < img["size"]):
                        missing_byte_count = img["size"] - image_fsize
                        for b in range(missing_byte_count):
                            missing_bytes += b"\x00"
                        print(f"{missing_byte_count} null bytes appended to {image_fname} to fit image!")
                    
                    with open(image_fname, "rb") as bitmap:
                        bmpData = bitmap.read()
                        image_buf.append(bmpData + missing_bytes)

                    image_id += 1
                    finished = True
                else:
                    print(f"ERROR: file couldn't be built, because {image_fname} was not found or is not a file!")
                    finished = False
                    break

            image_id = 1
            for packet in image_buf:
                # Write offset data to original file position
                file.seek(image_data[image_id - 1]["position"] - 14)
                file.write(packet)
                image_id += 1

            lastImgOffset = image_data[len(image_data) - 1]["position"] + image_data[len(image_data) - 1]["size"]
            ofile.seek(lastImgOffset)
            file.seek(lastImgOffset)
            file.write(ofile.read())
            
            file.close()

            final_file_size = os.path.getsize(filename)

            if (o_file_size == final_file_size):
                print("Final filesize length check PASSED!")
            else:
                print("ERROR: Final filesize length check FAILED!")
                print(f"Off by {o_file_size - final_file_size} bytes")
                finished = False

            if finished:
                print("-----------")
                print("Repacking is successful! The exported image should be safe to flash, but still use at your own risk.")
            else:
                print("-----------")
                print("Repacking encountered an error. The exported image is INCOMPLETE or CORRUPTED, DO NOT FLASH!")

def dumpFromDevice(forceRecovery = False):
    # This function will run an automated script to dump the logo/splash file to disk
    if forceRecovery:
        print("WARN: force-recovery is on!")
    print("Waiting for device ...")
    os.system("adb wait-for-device")
    state = os.popen("adb get-state").read().strip()
    if (state == "device"):
        print("Device is currently in android mode!")
        if not forceRecovery:
            print("Checking root ... if you get a confirmation pop-up, click Allow!")
            state = os.popen("adb shell su -c echo ROOTED!").read().strip()

            if (state == "ROOTED!"):
                logoname = ""
                print("Device is rooted! Using direct dump ...")
                print("-> running commands")
                getAllBootdevices = os.popen(
                    "adb shell su -c ls -A1 /dev/block/bootdevice/by-name").read().strip()
                if ("\nlogo" in getAllBootdevices):
                    print("   logo partition found, dumping to file ...")
                    logoname = "logo"
                    os.system(
                        "adb shell \"su -c 'dd if=/dev/block/bootdevice/by-name/logo 2>/dev/null'\" > logo.img")
                elif ("\nsplash" in getAllBootdevices):
                    print("   splash partition found, dumping to file ...")
                    logoname = "splash"
                    os.system(
                        "adb shell \"su -c 'dd if=/dev/block/bootdevice/by-name/splash 2>/dev/null'\" > splash.img")
                else:
                    print(getAllBootdevices)
                    print("   neither logo or splash partition found?? - cancelled")
                    return
                if sys.platform == "win32":
                    print("Replacing 0x0D0A with 0x0A because Windows sucks ...")
                    with open(logoname + '.img', 'rb') as f:
                        data = f.read()
                        f.close()
                    data = data.replace(b'\r\n', b'\n')
                    with open(logoname + '.img', 'wb') as f:
                        f.write(data)
                print("File dump complete!")
                return
            else:
                print("Device is not rooted! Using fallback TWRP recovery method ...")
        print("Rebooting into recovery ...")
        os.system("adb reboot recovery");
        print("Attempting recovery dump method ...")
        print("-----------------------------------")
        print("Wait a few seconds ... if you are stuck here, your recovery might not be compatible :(")
        while True:
            state = Popen("adb get-state", shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = state.communicate()
            stateStr = stdout.decode('utf-8').strip()
            if stateStr == "recovery":
                print("Got recovery adb mode!")
                print("-> running commands")
                getAllBootdevices = os.popen("adb shell ls -A1 /dev/block/bootdevice/by-name").read().strip()
                if ("\nlogo" in getAllBootdevices):
                    print("   logo partition found, dumping to file ...")
                    os.system("adb shell \"dd if=/dev/block/bootdevice/by-name/logo 2>/dev/null\" > logo.img")
                elif ("\nsplash" in getAllBootdevices):
                    print("   splash partition found, dumping to file ...")
                    os.system("adb shell \"dd if=/dev/block/bootdevice/by-name/splash 2>/dev/null\" > splash.img")
                else:
                    print(getAllBootdevices)
                    print("   neither logo or splash partition found?? - cancelled")
                    os.system("adb reboot system")
                    break
                print("File dump complete!")
                os.system("adb reboot system")
                break
    else:
        print("Device is in " + state + "??")
        

# dumpFromDevice()

# unpack("newlogo.img")

# rebuild("newlogo.img", "possible.img")

if __name__ == '__main__':
    if (len(sys.argv) >= 2):
        if (sys.argv[1]):
            if (sys.argv[1] == "dump"):
                if (len(sys.argv) >= 3 and sys.argv[2] == "--force-recovery"):
                    dumpFromDevice(True)
                else:
                    dumpFromDevice()
            elif (sys.argv[1] == "unpack"):
                if (len(sys.argv) >= 3 and sys.argv[2] != ""):
                    if (os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2])):
                        unpack(sys.argv[2])
                    else:
                        print("error: is not file or file not found")
                else:
                    print("error: file not given")
            elif (sys.argv[1] == "rebuild"):
                if (len(sys.argv) >= 3 and sys.argv[2] != ""):
                    if (os.path.exists(sys.argv[2]) and os.path.isfile(sys.argv[2])):
                        rebuild(sys.argv[2], sys.argv[2].split(".")[0] + "_new.img")
                    else:
                        print("error: is not file or file not found")
                else:
                    print("error: file not given")
        else:
            print("error: no ACTION given")
    else:
        print("""ximi_logo_dmp v1 - by pocoguy

    Usage: logo_dmp [ACTION] <files>

Examples: logo_dmp dump
            -> dumps logo file from your device (over recovery mode or root)
          logo_dmp unpack < filename to logo.img / splash.img >
            -> unpacks BMP files from logo file
          logo_dmp rebuild < filename to original logo.img / splash.img >
            -> rebuilds the existing BMP files into a copy of the original.

To flash the new logo.img or splash.img, run:

fastboot flash logo logo.img
            or
fastboot flash splash splash.img
        
Instructions:
        """ + HELP_INSTRUCTIONS)