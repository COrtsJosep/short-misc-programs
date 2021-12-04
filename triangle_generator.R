# Plots a randomly generated triangle.
give_me_a_triangle <- function(){
  angles <- sort(runif(3), decreasing = TRUE)
  angles <- angles*(pi/sum(angles))
  sines <- sin(angles)
  sides <- c(1, sines[2]/sines[1], sines[3]/sines[1])

  x <- c(0, sides[3]*cos(angles[1]), sides[3]*cos(angles[1]) + sides[1]*cos(-pi + angles[1] + angles[2]),
         sides[3]*cos(angles[1]) + sides[1]*cos(-pi + angles[1] + angles[2]) - sides[2]*cos(-pi + angles[1] + angles[2] + angles[3]) )
  y <- c(0, sides[3]*sin(angles[1]), sides[3]*sin(angles[1]) + sides[1]*sin(-pi + angles[1] + angles[2]),
         sides[3]*sin(angles[1]) + sides[1]*sin(-pi + angles[1] + angles[2]) + sides[2]*sin(-pi + angles[1] + angles[2] + angles[3]) )

  plot(x, y, main = "A Beautiful Triangle", col = 2, cex = 2, pch = 16,
       xlab = "X-Coordinate", ylab = "Y-Coordinate",
       xlim = c(-0.5, 1), ylim = c(0, 1))
  lines(x, y)
  cat("Obtusest angle measures", angles[1]*180/pi, "degrees.")
}

give_me_a_triangle()


##########


# Generates a gif with 10 triangle plots
library(magick)
dir.create(paste(getwd(), "/triangles", sep = ""))

for (i in 0:9){
  pathstr <- paste(getwd(), "/triangles/triangle", toString(i), ".png", sep = "")
  png(pathstr, width = 600)
  give_me_a_triangle()
  dev.off()
}

imgs <- list.files(paste(getwd(), "/triangles", sep = ""), full.names = TRUE)
img_list <- lapply(imgs, image_read)
img_joined <- image_join(img_list)
img_animated <- image_animate(img_joined, fps = 2)
image_write(image = img_animated,
            path = paste(getwd(), "/triangles/trianglesgif.gif", sep = ""))
