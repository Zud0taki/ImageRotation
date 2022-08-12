# import necessary libraries and functions
import cv2
import glob
import math
from scipy import ndimage


# declare main method
def main(img_folder, txt_folder, out_folder):
    # variable declaration for the main method
    img_input = []
    txt_input = []
    txt_from_line = []
    x_list = []
    y_list = []
    x_exp_list = []
    y_exp_list = []
    export_list = []
    temp_x_list = []
    temp_y_list = []
    rotation_counter = 0

    # read files from paths and save in array
    img_folder = img_folder + "/*.jpg"
    for image in glob.glob(img_folder):
        img_input.append(image)
    txt_folder = txt_folder + "/*.txt"
    for text in glob.glob(txt_folder):
        txt_input.append(text)

    # check if img_input and txt_input have the same length
    if len(img_input) == len(txt_input):

        # get image and txt file name
        for f in range(len(img_input)):
            # read images and txt´s - check if names are the same
            img = cv2.imread(img_input[f], -1)
            txt_file = open(txt_input[f], "r")

            img_name = img_input[f]
            img_name = img_name.split("\\")
            img_name = img_name[len(img_name) - 1]
            img_name = img_name.split(".")
            img_name = img_name[0]

            txt_name = txt_input[f]
            txt_name = txt_name.split("\\")
            txt_name = txt_name[len(txt_name) - 1]
            txt_name = txt_name.split(".")
            txt_name = txt_name[0]

            # check if both names match
            if img_name == txt_name:
                for line in txt_file:
                    line = line.split()
                    txt_from_line.append(line)
                # get img_center for calc
                for d in range(len(txt_from_line)):
                    x_list.append(txt_from_line[d][1])
                    y_list.append(txt_from_line[d][2])
                    x_exp_list.append(txt_from_line[d][3])
                    y_exp_list.append(txt_from_line[d][4])

                img_size = img.shape
                img_x = img_size[1]
                img_y = img_size[0]
                img_center_x = img_x / 2
                img_center_y = img_y / 2
                origin = x_list[0], y_list[0]
                # mid_1 = x_list[0]
                # mid_2 = y_list[0]
                # mitte = (int(float(mid_1)*img_x), int(float(mid_2)*img_y))
                point = img_center_x, img_center_y
                # cv2.circle(img, mitte, radius, color, thickness)
                # cv2.imshow("img", img)
                # cv2.waitKey(0)

                for l in range(len(x_list)):
                    x_list[l] = float(x_list[l]) * img_x
                    y_list[l] = float(y_list[l]) * img_y
            rotation_counter = 0

            # calculate turned images and construct new annotation files
            while rotation_counter < 3:
                point = img_center_x, img_center_y
                if rotation_counter == 0:
                    for h in range(len(x_list)):
                        origin = x_list[h], y_list[h]

                        border_to_x = x_list[h]
                        x_to_center = img_center_x - border_to_x
                        border_to_y = y_list[h]
                        y_to_center = img_center_y - border_to_y

                        new_x = img_center_y + y_to_center
                        new_y = img_center_x - x_to_center

                        temp_x_list.append(new_x)
                        temp_y_list.append(new_y)

                        concat = "1" + " " + str(new_x / img_y) + " " + str(new_y / img_x) + " " + str(
                            y_exp_list[h]) + " " + str(x_exp_list[h])
                        export_list.append(concat)

                    rotated = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
                    centercoords = (int(new_x), int(new_y))
                    # TODO: Implement visualisation marker
                    # cv2.circle(rotated, centercoords, radius, color, thickness)
                    cv2.imwrite(out_folder + "/" + img_name + "_" + str(rotation_counter) + ".jpg", rotated)
                    txt_name_export = (out_folder + "/" + txt_name + "_" + str(rotation_counter) + ".txt")
                    txtfile = open(txt_name_export, 'w')
                    for element in export_list:
                        txtfile.write(str(element) + "\n")
                    txtfile.close()
                    export_list = []
                    print("Rotation_1_completed")
                    rotation_counter += 1

                if rotation_counter == 1:
                    for h in range(len(x_list)):
                        origin = x_list[h], y_list[h]

                        border_to_x = x_list[h]
                        x_to_center = img_center_x - border_to_x
                        border_to_y = y_list[h]
                        y_to_center = img_center_y - border_to_y

                        new_x = img_center_x + x_to_center
                        new_y = img_center_y + y_to_center

                        temp_x_list.append(new_x)
                        temp_y_list.append(new_y)

                        concat = "1" + " " + str(new_x / img_x) + " " + str(new_y / img_y) + " " + str(
                            x_exp_list[h]) + " " + str(y_exp_list[h])
                        export_list.append(concat)

                    rotated = cv2.rotate(img, cv2.cv2.ROTATE_180)
                    centercoords = (int(new_x), int(new_y))
                    # TODO: Implement visualisation marker
                    # cv2.circle(rotated, centercoords, radius, color, thickness)
                    cv2.imwrite(out_folder + "/" + img_name + "_" + str(rotation_counter) + ".jpg", rotated)
                    txt_name_export = (out_folder + "/" + txt_name + "_" + str(rotation_counter) + ".txt")
                    txtfile = open(txt_name_export, 'w')
                    for element in export_list:
                        txtfile.write(str(element) + "\n")
                    txtfile.close()
                    export_list = []
                    print("Rotation_2_completed")
                    rotation_counter += 1

                if rotation_counter == 2:
                    for h in range(len(x_list)):
                        origin = x_list[h], y_list[h]

                        border_to_x = x_list[h]
                        x_to_center = img_center_x - border_to_x
                        border_to_y = y_list[h]
                        y_to_center = img_center_y - border_to_y

                        new_x = img_center_y - y_to_center
                        new_y = img_center_x + x_to_center

                        temp_x_list.append(new_x)
                        temp_y_list.append(new_y)

                        concat = "1" + " " + str(new_x / img_y) + " " + str(new_y / img_x) + " " + str(
                            y_exp_list[h]) + " " + str(x_exp_list[h])
                        export_list.append(concat)

                    rotated = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
                    centercoords = (int(new_x), int(new_y))
                    # TODO: Implement visualisation marker
                    # cv2.circle(rotated, centercoords, radius, color, thickness)
                    cv2.imwrite(out_folder + "/" + img_name + "_" + str(rotation_counter) + ".jpg", rotated)
                    txt_name_export = (out_folder + "/" + txt_name + "_" + str(rotation_counter) + ".txt")
                    txtfile = open(txt_name_export, 'w')
                    for element in export_list:
                        txtfile.write(str(element) + "\n")
                    txtfile.close()
                    export_list = []
                    print("Rotation_3_completed")
                    rotation_counter += 1
                    print("Next_Image")
                    print(str(f))

            # empty lists for next image
            txt_from_line = []
            x_list = []
            y_list = []
            x_exp_list = []
            y_exp_list = []
