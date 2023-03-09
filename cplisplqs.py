import cv2

# Load the image
img = cv2.imread("path/to/image.jpg")

# Create a human figure detector
human_cascade = cv2.CascadeClassifier("path/to/haarcascade_fullbody.xml")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect human figures in the image
humans = human_cascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangles around the detected humans
for (x, y, w, h) in humans:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the image with detected humans
cv2.imshow("Detected Humans", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
