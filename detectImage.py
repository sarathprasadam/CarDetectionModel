from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import cv2
import numpy as np
import torch
import torchvision
from PIL import Image,ImageDraw
from torchvision import transforms as torchtrans
from torchvision.transforms import transforms
#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
from PIL import ImageTk
def imageDetect(master, imagepath, classVariable, canvas):
    # load image:
    car_image = cv2.imread(imagepath)
    original_size = (car_image.shape[1], car_image.shape[0])
    cv2.imwrite("Detections//original.jpg" ,car_image)
    #print(imagepath)
    # resize image:
    img_size = (128, 128)
    scale_x = original_size[0] / 128
    scale_y = original_size[1] / 128
    img = Image.fromarray(car_image)
    img1 = img.copy()
    img1 = img1.resize(size=img_size)
    arr1 = np.asarray(img1, dtype="uint8")
    # normalize image pixels:
    img_res = arr1 / 255.0
    img_res = img_res.astype(np.float32)
    #print(img_res)
    # transform image to tensor:
    transform = transforms.Compose([transforms.ToTensor()])
    image = transform(img_res)
    #cv2.imwrite("Detections//original.jpg", image)

    image1 = image.unsqueeze(0)
    device = torch.device('cpu')
    model_path = "Model//FasterRCNN_1"
    model = torch.load(model_path)
    print("Model Loaded")
    model.to(device)
    # set model to evaluation mode & make predictions:
    model.eval()
    with torch.no_grad():
        prediction = model(image1)
        print("prediction Completed")
        print(prediction)
    if len(prediction[0]['labels']) > 0:
        max_score_index = torch.argmax(prediction[0]['scores']).item()
        print("max score index:{}".format(max_score_index))
        max_label_index = prediction[0]['labels'][max_score_index].item()
        print("max label index:{}".format(max_label_index))
        predicted_class = carModel[max_label_index]
        print(predicted_class)
        classVariable.set(predicted_class)
        nms_prediction = apply_NonMaxSuppression(prediction, iou_thresh=0.01)
        print(nms_prediction)
        #setBBImage(convert_torch_to_pil(image),nms_prediction,canvas,showBbox='yes', predict='yes')
        #cv2.imwrite("Detections//test.jpg", car_image)
        #imagefile=setBBImage(convert_torch_to_pil(car_image), nms_prediction,scale_x,scale_y, canvas, showBbox='yes', predict='yes')

        imagefile=setBBImage(nms_prediction,scale_x,scale_y, canvas, showBbox='yes', predict='yes')


        return imagefile
    else:
        msg = "Sorry, could not predict Bounding Boxes / Car Model for this Image!"
        print("No prediction Done")
        messagebox.showerror(title="Error", message=msg)
        return None
        pass
    pass

def apply_NonMaxSuppression(orig_prediction, iou_thresh=0.3):
    '''
    This function is used to apply non-max suppression to prevent low probability bounding boxes to be displayed.
    Arguments:
    1. original prediction dictionary
    2. IOU cut-off threshold
    Returns:
    1. final prediction dictionary
    '''
    # torchvision returns the indices of the bboxes to keep:
    keep = torchvision.ops.nms(orig_prediction[0]['boxes'], orig_prediction[0]['scores'], iou_thresh)
    # create final prediction dictionary:
    final_prediction = orig_prediction
    final_prediction[0]['boxes'] = final_prediction[0]['boxes'][keep]
    final_prediction[0]['scores'] = final_prediction[0]['scores'][keep]
    final_prediction[0]['labels'] = final_prediction[0]['labels'][keep]
    return final_prediction[0]

def convert_torch_to_pil(img):
    '''
    This function converts a torchtensor back to PIL image:
    Arguments:
    1. torchtensor
    '''

    return torchtrans.ToPILImage()(img).convert('RGB')

def setBBImage(target,scale_x,scale_y,canvas,showBbox='yes', predict='no'):
    if predict == 'no':
        bbox_color = 'r'
    else:
        bbox_color = 'g'
    if showBbox == 'yes':
        '''
        img = Image.fromarray(img)
        resized_img = img.resize((canvas.winfo_width(), canvas.winfo_height()))
        '''
        image = Image.open("Detections//original.jpg" )
        resized_img = image.resize((canvas.winfo_width(), canvas.winfo_height()))
        img_tk = ImageTk.PhotoImage(resized_img)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        draw = ImageDraw.Draw(resized_img)
        for i in range(len(target['boxes'])):
            x = int(target['boxes'][i][0].item() * (resized_img.width / image.width) * scale_x)
            y = int(target['boxes'][i][1].item() * (resized_img.height / image.height) * scale_y)
            width = int(target['boxes'][i][2].item() * (resized_img.width / image.width) * scale_x) - x
            height = int(target['boxes'][i][3].item() * (resized_img.height / image.height) * scale_y) - y
            bbox_color = 'red'
            rect_id = canvas.create_rectangle(x, y, x + width, y + height, outline=bbox_color)
            draw.rectangle((x, y, x + width, y + height), outline=bbox_color)
        canvas.update()
        canvas.image = img_tk
        save_path = "Detections//image.jpg"  # Specify the desired save path and file name
        resized_img.save(save_path)

        return img_tk


carModel = ['__background__', 'Audi TTS Coupe 2012','Acura TL Sedan 2012','Dodge Dakota Club Cab 2007',
                'Hyundai Sonata Hybrid Sedan 2012', 'Ford F-450 Super Duty Crew Cab 2012', 'Geo Metro Convertible 1993',
                'Dodge Journey SUV 2012','Dodge Charger Sedan 2012','Mitsubishi Lancer Sedan 2012',
                'Chevrolet Traverse SUV 2012','Buick Verano Sedan 2012','Toyota Sequoia SUV 2012',
                'Hyundai Elantra Sedan 2007','Dodge Caravan Minivan 1997','Volvo C30 Hatchback 2012',
                'Plymouth Neon Coupe 1999','Chevrolet Malibu Sedan 2007','Volkswagen Beetle Hatchback 2012',
                'Chevrolet Corvette Ron Fellows Edition Z06 2007','Chrysler 300 SRT-8 2010','BMW M6 Convertible 2010',
                'GMC Yukon Hybrid SUV 2012','Nissan Juke Hatchback 2012','Volvo 240 Sedan 1993','Suzuki SX4 Sedan 2012',
                'Dodge Ram Pickup 3500 Crew Cab 2010','Spyker C8 Coupe 2009','Land Rover Range Rover SUV 2012',
                'Hyundai Elantra Touring Hatchback 2012','Chevrolet Cobalt SS 2010','Hyundai Veracruz SUV 2012',
                'Ferrari 458 Italia Coupe 2012','BMW Z4 Convertible 2012','Dodge Charger SRT-8 2009',
                'Fisker Karma Sedan 2012','Infiniti QX56 SUV 2011','Audi A5 Coupe 2012','Volkswagen Golf Hatchback 1991',
                'GMC Savana Van 2012','Audi TT RS Coupe 2012','Rolls-Royce Phantom Sedan 2012','Porsche Panamera Sedan 2012',
                'Bentley Continental GT Coupe 2012','Jeep Grand Cherokee SUV 2012','Audi R8 Coupe 2012',
                'Cadillac Escalade EXT Crew Cab 2007','Bentley Continental Flying Spur Sedan 2007',
                'Chevrolet Avalanche Crew Cab 2012','Dodge Dakota Crew Cab 2010','HUMMER H3T Crew Cab 2010',
                'Ford F-150 Regular Cab 2007','Volkswagen Golf Hatchback 2012','Ferrari FF Coupe 2012',
                'Toyota Camry Sedan 2012','Aston Martin V8 Vantage Convertible 2012','Audi 100 Sedan 1994',
                'Ford Ranger SuperCab 2011','GMC Canyon Extended Cab 2012','Acura TSX Sedan 2012','BMW 3 Series Sedan 2012',
                'Honda Odyssey Minivan 2012','Dodge Durango SUV 2012','Toyota Corolla Sedan 2012',
                'Chevrolet Camaro Convertible 2012','Ford Edge SUV 2012','Bentley Continental GT Coupe 2007',
                'Audi 100 Wagon 1994','Ford E-Series Wagon Van 2012','Jeep Patriot SUV 2012','Audi S6 Sedan 2011',
                'Mercedes-Benz S-Class Sedan 2012','Hyundai Sonata Sedan 2012',
                'Rolls-Royce Phantom Drophead Coupe Convertible 2012','Ford GT Coupe 2006','Cadillac CTS-V Sedan 2012',
                'BMW X3 SUV 2012','Chevrolet Express Van 2007','Chevrolet Impala Sedan 2007',
                'Chevrolet Silverado 1500 Extended Cab 2012','Mercedes-Benz C-Class Sedan 2012','Hyundai Santa Fe SUV 2012',
                'Dodge Sprinter Cargo Van 2009','GMC Acadia SUV 2012','Hyundai Genesis Sedan 2012',
                'Dodge Caliber Wagon 2012','Jeep Liberty SUV 2012','Mercedes-Benz 300-Class Convertible 1993',
                'Ford Expedition EL SUV 2009','BMW 1 Series Coupe 2012','Jaguar XK XKR 2012','Hyundai Accent Sedan 2012',
                'Isuzu Ascender SUV 2008','Nissan 240SX Coupe 1998','Scion xD Hatchback 2012','Chevrolet Corvette ZR1 2012',
                'Bentley Arnage Sedan 2009','Chevrolet HHR SS 2010','Land Rover LR2 SUV 2012','Hyundai Azera Sedan 2012',
                'Chrysler Aspen SUV 2009','Buick Regal GS 2012','BMW 3 Series Wagon 2012','Jeep Compass SUV 2012',
                'Ram C-V Cargo Van Minivan 2012','Spyker C8 Convertible 2009','Audi S4 Sedan 2007',
                'Rolls-Royce Ghost Sedan 2012','AM General Hummer SUV 2000','Ford Freestar Minivan 2007',
                'Bentley Mulsanne Sedan 2011','Audi TT Hatchback 2011','Mercedes-Benz SL-Class Coupe 2009',
                'Chevrolet Silverado 1500 Hybrid Crew Cab 2012','Buick Enclave SUV 2012','Chevrolet TrailBlazer SS 2009',
                'HUMMER H2 SUT Crew Cab 2009','McLaren MP4-12C Coupe 2012','Dodge Challenger SRT8 2011',
                'Suzuki SX4 Hatchback 2012','Bugatti Veyron 16.4 Convertible 2009','Toyota 4Runner SUV 2012',
                'Buick Rainier SUV 2007','Chrysler Sebring Convertible 2010','Acura Integra Type R 2001',
                'Audi V8 Sedan 1994','Audi RS 4 Convertible 2008','Honda Accord Coupe 2012','Audi S4 Sedan 2012',
                'Aston Martin Virage Coupe 2012','Chevrolet Sonic Sedan 2012','Chevrolet Monte Carlo Coupe 2007',
                'Volvo XC90 SUV 2007','Ford Mustang Convertible 2007','Aston Martin Virage Convertible 2012',
                'smart fortwo Convertible 2012','FIAT 500 Abarth 2012','Infiniti G Coupe IPL 2012',
                'Dodge Caliber Wagon 2007','Hyundai Tucson SUV 2012','Acura ZDX Hatchback 2012',
                'BMW ActiveHybrid 5 Sedan 2012','Ferrari California Convertible 2012','Nissan Leaf Hatchback 2012',
                'Lamborghini Diablo Coupe 2001','Audi S5 Convertible 2012','BMW 6 Series Convertible 2007',
                'Ferrari 458 Italia Convertible 2012','Chevrolet Silverado 2500HD Regular Cab 2012',
                'Chevrolet Corvette Convertible 2012','Bugatti Veyron 16.4 Coupe 2009','Tesla Model S Sedan 2012',
                'FIAT 500 Convertible 2012','Hyundai Veloster Hatchback 2012','Lincoln Town Car Sedan 2011',
                'Lamborghini Aventador Coupe 2012','Dodge Ram Pickup 3500 Quad Cab 2009','Nissan NV Passenger Van 2012',
                'Honda Odyssey Minivan 2007','Maybach Landaulet Convertible 2012','Chevrolet Silverado 1500 Regular Cab 2012',
                'Suzuki Kizashi Sedan 2012','Chevrolet Tahoe Hybrid SUV 2012','Mercedes-Benz Sprinter Van 2012',
                'Suzuki Aerio Sedan 2007','Audi S5 Coupe 2012','Aston Martin V8 Vantage Coupe 2012',
                'Chevrolet Malibu Hybrid Sedan 2010','Ford F-150 Regular Cab 2012','Ford Fiesta Sedan 2012',
                'Ford Focus Sedan 2007','Bentley Continental Supersports Conv. Convertible 2012',
                'Chevrolet Silverado 1500 Classic Extended Cab 2007','BMW X5 SUV 2007','Jeep Wrangler SUV 2012',
                'Acura TL Type-S 2008','Chrysler Crossfire Convertible 2008','Lamborghini Gallardo LP 570-4 Superleggera 2012',
                'Mercedes-Benz E-Class Sedan 2012','Chevrolet Express Cargo Van 2007','GMC Terrain SUV 2012',
                'Dodge Magnum Wagon 2008','Honda Accord Sedan 2012','Chrysler PT Cruiser Convertible 2008',
                'Mazda Tribute SUV 2011','BMW M3 Coupe 2012','Eagle Talon Hatchback 1998','Daewoo Nubira Wagon 2002',
                'BMW X6 SUV 2012','Lamborghini Reventon Coupe 2008','Cadillac SRX SUV 2012',
                'MINI Cooper Roadster Convertible 2012','Acura RL Sedan 2012','BMW 1 Series Convertible 2012',
                'Dodge Durango SUV 2007','BMW M5 Sedan 2010','Chrysler Town and Country Minivan 2012']