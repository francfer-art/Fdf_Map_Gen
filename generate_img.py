from PIL import Image

def create_image_from_matrix_file(matrix_file, output_filename):
    """Create image from matrix data file"""
    with open(matrix_file, 'r') as file:
        matrix = [line.strip().split(",") for line in file]

    height = len(matrix)
    width = len(matrix[0])
    image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            color = tuple(int(component, 16) for component in matrix[y][x].split("x")[1].split(","))
            image.putpixel((x, y), color)

    image.save(output_filename)

# Example usage
matrix_file = 'map.fdf'
output_filename = 'output.fdf'
create_image_from_matrix_file(matrix_file, output_filename)
print(f"Image saved as {output_filename}")
