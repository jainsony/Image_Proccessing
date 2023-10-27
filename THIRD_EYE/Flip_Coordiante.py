import cv2

# Load your image
image = cv2.imread('lena.png', 1)

# Define a function to flip the y-axis coordinates of a point
def flip_coordinates(point):
    x, y = point
    return [x, image.shape[0] - y - 1]

# Apply the coordinate flip function to a point
original_point = [10, 10]
flipped_point = flip_coordinates(original_point)

# Display the original and flipped points
print("Original Point:", original_point)
print("Flipped Point:", flipped_point)

# Display the original and flipped images (for visualization)
cv2.circle(image, original_point, 5, (0, 0, 255), -1)  # Red circle at the original point
cv2.circle(image, flipped_point, 5, (0, 255, 0), -1)  # Green circle at the flipped point

cv2.putText(image, str(original_point), original_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(image, str(flipped_point), flipped_point, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)



cv2.imshow('Image with Points', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
