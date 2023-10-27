import math

def calculate_triangle_angles(a, b, c):
    try:
        # Check if the input values can form a triangle
        if a + b > c and a + c > b and b + c > a:
            # Calculate angle A
            cos_A = (b**2 + c**2 - a**2) / (2 * b * c)
            angle_A = math.degrees(math.acos(cos_A))
            
            # Calculate angle B
            cos_B = (c**2 + a**2 - b**2) / (2 * c * a)
            angle_B = math.degrees(math.acos(cos_B))
            
            # Calculate angle C (by the sum of angles in a triangle)
            angle_C = 180 - angle_A - angle_B
            
            return angle_A, angle_B, angle_C
        else:
            raise ValueError("Invalid side lengths. They cannot form a triangle.")
    except ValueError as e:
        return None, None, str(e)

# Input side lengths
a = float(input("Enter the length of side a: "))
b = float(input("Enter the length of side b: "))
c = float(input("Enter the length of side c: "))

# Calculate angles and handle exceptions
angle_A, angle_B, angle_C = calculate_triangle_angles(a, b, c)

if angle_A is not None:
    # Print the results
    print(f"Angle A: {angle_A:.2f} degrees")
    print(f"Angle B: {angle_B:.2f} degrees")
    print(f"Angle C: {angle_C:.2f} degrees")
else:
    print(f"Error: {angle_C}")
