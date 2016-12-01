from skimage import io, color, feature, transform
import numpy as np

def calc_contrast(r, g, b):
	# y is the luminance
	y = 0.299 * r + 0.587 * g + 0.114 * b
	return (np.max(y) - np.min(y))/np.mean(y)

def get_spat_arrng_ftrs(gray_img):
	# resize img to 600 * 600
	resized_img = transform.resize(gray_img, (600,600))
	left = resized_img.transpose()[:300].transpose()
	right = resized_img.transpose()[300:].transpose()

	I_anti = np.identity(600)[::-1] # anti - diagonal identity matrix
	inner = feature.hog(left) - feature.hog(I_anti.dot(right))

	return np.linalg.norm(inner)

def calc_color_ftrs(h, s, v):
	v_mean = np.mean(v)
	s_mean = np.mean(s)

	# emotional features
	pleasure = 0.69 * v_mean + 0.22 * s_mean
	arousal =  -0.31 * v_mean + 0.60 * s_mean
	dominance = 0.76 * v_mean + 0.32 * s_mean

	# HSV-itten color histogram features
	counts_hue, _ = np.histogram(h, bins = 12) # 12 bins of hue
	counts_saturation, _ = np.histogram(s, bins = 5) # 5 bins of saturation
	counts_brightness, _ = np.histogram(v, bins = 3) # 3 bins of brightness (v)

	return dict(pleasure = pleasure, arousal = arousal, dominance = dominance, 
				hsv_itten_std_h = np.std(counts_hue), hsv_itten_std_s = np.std(counts_saturation), hsv_itten_std_v = np.std(counts_brightness))

def get_arr(imgObj):
	first = np.array([pix[0] for row in imgObj for pix in row])
	second = np.array([pix[1] for row in imgObj for pix in row])
	third = np.array([pix[2] for row in imgObj for pix in row])

	return (first, second, third)

def __main__():
	imgFlNm = "/Users/sreejithmenon/Dropbox/Social_Media_Wildlife_Census/All_Zebra_Count_Images/8598.jpeg"

	rgbImg = io.imread(imgFlNm)
	hsvImg = color.rgb2hsv(rgbImg)
	grayImg = color.rgb2gray(rgbImg)

	red, green, blue = get_arr(rgbImg)
	hue, saturation, value = get_arr(hsvImg)

	contrast = calc_contrast(red, green, blue)
	emoFtrs = calc_color_ftrs(hue, saturation, value)

	print("Contrast : %f" %contrast)
	print(emoFtrs)

	print(get_spat_arrng_ftrs(grayImg))

if __name__ == "__main__":
	__main__()