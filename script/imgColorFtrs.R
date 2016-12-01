library(jpeg)

getAverageHSV <- function(imgPath) {
  rgbImg <- readJPEG(imgPath)
  red = as.vector(t(rgbImg[,,1]))
  green = as.vector(t(rgbImg[,,2]))
  blue = as.vector(t(rgbImg[,,3]))
  
  hsvImg <- rgb2hsv(red,green,blue)
  hMean <- mean(hsvImg[1,])
  sMean <- mean(hsvImg[2,])
  vMean <- mean(hsvImg[3,])
  
  result <- c(hMean,sMean,vMean)
  return(result)
}

calcEmotionalFtrs <- function(meanHSV) {
  s <- meanHSV[2]
  v <- meanHSV[3]
  
  pleasure <- 0.69 * v + 0.22 * s
  arousal <- -0.31 * v + 0.60 * s
  dominance <- 0.76 * v + 0.32 * s
  
  result <- c(pleasure,arousal,dominance)
  return(result)
}

calcContrast <- function(imgPath) {
  rgbImg <- readJPEG(imgPath)
  red = as.vector(t(rgbImg[,,1]))
  green = as.vector(t(rgbImg[,,2]))
  blue = as.vector(t(rgbImg[,,3]))
  
  # y is the luminance
  y <- 0.299 * red + 0.587 * green + 0.114 * blue
  
  contrast <- (max(y) - min(y))/mean(y)
  return(contrast)
  
}

vctrs <- list()
