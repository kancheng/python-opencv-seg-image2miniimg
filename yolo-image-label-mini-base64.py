import cv2
import numpy as np
import base64

def pair_list(numbers):
    pairs=[]
    for i in range(0 , len(numbers), 2):
        if i+1 < len(numbers):
            pairs.append([numbers[i], numbers[i+1]])
    return pairs

# # Read image
image = cv2.imread("./yolo-coco128seg/coco128.jpg")

h, w = image.shape[:2]
print("H : ", h , "; W : ", w)

with open("./yolo-coco128seg/coco128.txt", "r") as f:
    data = f.read()
print("Context : \n",data,"\nType : ", type(data), "; ")
data = data.split('\n')
data = [x.strip() for x in data if x.strip()!='']

print("YOLO OBJ : ", len(data))

new_data = []
for obj in data:
    raw_olist = obj.split(' ')
    olist = [x.strip() for x in raw_olist if x.strip()!='']
    del olist[0]
    new_data.append(olist)

for i in range(len(new_data)):
    print("INFO. Coordinates", i," : ", new_data[i])
    for xy in range(len(new_data[i])):
        if xy%2 == 0:
            newx = int(float(new_data[i][xy])*h)
            print("x :", new_data[i][xy], " to ", newx)
            new_data[i][xy] = newx
        elif xy%2 != 0:
            newy = int(float(new_data[i][xy])*w)
            print("y :", new_data[i][xy], " to ", newy)
            new_data[i][xy] = newy
# print("OBJ : ", new_data)
# print("OBJ Type: ", type(new_data))
# print("OBJ Len : ", len(new_data))
point_group = []
point_images = []
point = []
for i in range(len(new_data)):
    # print("INFO. Coordinates", i," : ", new_data[i])
    point_group = pair_list(new_data[i])
    # print(len(point_group))
    point_images.append(point_group)
temcon =''
for key in range(len(point_images)) :

    # Example polygon vertex coordinates
    polygon_points = np.array(point_images[key])
    # print( polygon_points)
    # EX :
    # polygon_points = np.array([[100, 50], [200, 80], [250, 200], [150, 250], [60, 170]])

    # Calculate the center of gravity (center point) of a polygon
    center_x = np.mean(polygon_points[:, 0])
    center_y = np.mean(polygon_points[:, 1])
    center = (int(center_x), int(center_y))
    print(f"The coordinates of the center point of the polygon are: {center}")

    # Creates a blank mask the same size as the image
    mask = np.zeros_like(image)

    # Fill polygon area
    cv2.fillPoly(mask, [polygon_points], (255, 255, 255))

    # Use masks to cut images
    result = cv2.bitwise_and(image, mask)
    # print(result)
    # print(image)
    # Find the bounding rectangle of the polygon used to cut the image
    x, y, w, h = cv2.boundingRect(polygon_points)
    # print(x, y, w, h)
    # cropped_image = result[y:y+h, x:x+w]
    # print(y-10)
    # cropped_image1 = result[y-10:y+h+10, x-10:x+w+10]
    # cropped_image2 = image[y-10:y+h+10, x-10:x+w+10]
    sy = y-10
    ey = y+h
    sx = x-10
    ex = x+w
    # cropped_image1 = result[sy:ey, sx:ex]
    # cropped_image2 = image[sy:ey, sx:ex]
    cropped_image1 = result[y:ey, x:ex]
    cropped_image2 = image[y:ey, x:ex]
    # print(cropped_image1)
    # print(cropped_image2)
    # Save the cropped image
    tn1 = './out/cropped_image_mask_' + str(key) + '.jpg'
    tn2 = './out/cropped_image_raw_' + str(key) + '.jpg'
    # print(tn1,tn2,cropped_image1,cropped_image2)
    cv2.imwrite(tn1, cropped_image1)
    cv2.imwrite(tn2, cropped_image2)
    # img_constant=cv2.copyMakeBorder(img,top_size,botton_size,left_size,right_size,borderType=cv2.BORDER_CONSTANT,value=0)
    bimage1 = cv2.imencode('.png',cropped_image1)[1]
    base64_head1 = 'data:image/png;base64,'
    base64_main1 = str(base64.b64encode(bimage1))[2:-1]
    # print(base64_main)
    image_code1 = base64_head1 + base64_main1
    bimage2 = cv2.imencode('.png',cropped_image2)[1]
    base64_head2 = 'data:image/png;base64,'
    base64_main2 = str(base64.b64encode(bimage2))[2:-1]
    # print(base64_main)
    image_code2 = base64_head2 + base64_main2
    temcon = temcon + "<img src='" + image_code1 + "' alt='img' /><img src='" + image_code2 + "' alt='img' />"

con = "<!DOCTYPE html><html><head><title>YOLO</title></head><body><h1>YOLO FORMAL</h1><p>This is a images.</p>" + temcon + "</body></html>"

file = open("index_yolo.html", 'w')
file.write(con)
file.close()

