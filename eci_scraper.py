from PIL import Image, ImageChops, ImageEnhance
from selenium import webdriver
import pytesseract
import time

url = "https://electoralsearch.in/"
start_time = time.time()
#BORDER TRIMMING FUNCTION
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 1.7, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

#INITIATE WEBDRIVER
driver = webdriver.Chrome()
driver.get(url)

button = driver.find_element_by_id('continue')
button.click()

username = driver.find_element_by_id("name1")
username.send_keys("Narendra Modi")

#ATTEMPT CAPTCHA TILL SUCCESSFUL LOGIN or MAX ATTEMPTS
i = 0
while(True):
	if (i == 20):
		break
	time.sleep(1)
	url = driver.current_url
	if (url == "https://electoralsearch.in/##resultArea"):
		break
	else:
		try:
		    element = driver.find_element_by_id("captchaDetailImg")
		except:
		    print ("Couldn't retrieve by element")
		time.sleep(1)

		element.screenshot('cropped_image.png')
		img = Image.open("cropped_image.png")
		img = trim(img)
		img = img.convert('L')
		img = ImageEnhance.Contrast(img)
		img = img.enhance(4.0)
		
		try:
			captcha_string = pytesseract.image_to_string(img)
		except:
			print ("Couldn't perfrom OCR")

		captcha_text = driver.find_element_by_id("txtCaptcha")
		captcha_text.send_keys(captcha_string)
		driver.find_element_by_id("btnDetailsSubmit").click()
		time.sleep(3)
		i += 1

#PRINT TIME TAKEN
end_time = time.time()
print("Captcha bypassed in %g seconds" % (end_time - start_time))

