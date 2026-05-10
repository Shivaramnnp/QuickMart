import os
import time
import subprocess
import xml.etree.ElementTree as ET

def sh(cmd):
    # print("Running:", cmd)
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_ui_dump():
    try:
        sh("adb shell uiautomator dump /sdcard/window_dump.xml")
        dump = sh("adb shell cat /sdcard/window_dump.xml")
        return ET.fromstring(dump)
    except Exception as e:
        print("Dump failed:", e)
        return None

def find_node(root, attrib_name, attrib_value):
    if root is None: return None
    for node in root.iter('node'):
        if attrib_value in node.attrib.get(attrib_name, ''):
            return node
    return None

def click_node(node):
    bounds = node.attrib['bounds']
    bounds = bounds.replace('[', '').replace(']', ',').strip(',').split(',')
    x = (int(bounds[0]) + int(bounds[2])) // 2
    y = (int(bounds[1]) + int(bounds[3])) // 2
    sh(f"adb shell input tap {x} {y}")

def click_by_id(resource_id):
    print(f"Waiting for {resource_id}...")
    for _ in range(20):
        root = get_ui_dump()
        node = find_node(root, 'resource-id', resource_id)
        if node is not None:
            click_node(node)
            print(f"Clicked {resource_id}")
            return True
        time.sleep(1)
    print(f"Could not find node with id {resource_id}")
    return False

def type_text(text):
    sh(f"adb shell input text '{text}'")
    sh("adb shell input keyevent 66") # Enter

# Ensure clean state
sh("adb shell am force-stop com.shiva.quickMart")
sh("adb shell pkill -INT screenrecord || true")
time.sleep(2)
sh("adb shell rm /sdcard/demo.mp4 || true")

print("Starting screen record...")
subprocess.Popen("adb shell screenrecord --size 720x1280 --bit-rate 4000000 /sdcard/demo.mp4", shell=True)

try:
    print("Launching app...")
    sh("adb shell am start -n com.shiva.quickMart/.activities.LoginActivity")
    
    # Login Flow
    click_by_id("etPhone")
    time.sleep(0.5)
    type_text("9876543210")
    
    click_by_id("btnSendOtp")
    time.sleep(1)
    
    click_by_id("etOtp")
    time.sleep(0.5)
    type_text("1234")
    
    sh("adb shell input keyevent 4") # Back button
    time.sleep(0.5)
    click_by_id("btnVerifyOtp")
    
    # Home Flow
    click_by_id("btnAddToCart")
    time.sleep(1)
    
    # Scroll a little bit to make it look cool? No, just click the cart.
    click_by_id("fabCart")
    
    # Cart Flow
    click_by_id("btnIncrease")
    time.sleep(1)
    click_by_id("btnCheckout")
    
    # Checkout Flow
    click_by_id("etAddress")
    time.sleep(0.5)
    type_text("123\\ Main\\ Street")
    
    sh("adb shell input keyevent 4") # Back button
    time.sleep(1)
    click_by_id("rbOnline")
    time.sleep(1)
    
    click_by_id("btnPlaceOrder")
    
    # Order Success Flow
    click_by_id("btnContinueShopping")
    
    print("Done navigating!")
finally:
    print("Stopping recording...")
    sh("adb shell pkill -INT screenrecord || true")
    time.sleep(4)
    print("Pulling video...")
    sh("adb pull /sdcard/demo.mp4 /Users/shivarampatel/.gemini/antigravity/brain/a9394579-bdce-42da-be4f-83fcd964a327/quickmart_demo.mp4")
    print("Video pulled successfully.")
