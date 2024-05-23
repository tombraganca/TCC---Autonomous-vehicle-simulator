# def reset(self): 

# def step (self, action):
#         return obs, reward, done, extra_info

import glob
import os
import random
import sys
import time
import cv2

import numpy as np

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

SHOW_PREVIEW = False
IM_WIDTH = 640
IM_HEIGHT = 480

actor_list = []


# class CarEnv:
#     SHOW_CAM = SHOW_PREVIEW
#     STEER_AMT = 1.0
#     im_width = IM_WIDTH
#     im_heigth = IM_HEIGHT
#     front_camera = None
    
#     def __init__(self):
#         self.client = carla.Client("127.0.0.1", 2000)
#         self.client.set_timeout(2.0)
#         self.world = self.client.get_world()
#         self.blueprint_library = self.world.get_blueprint_library()
#         self.model_3 = blueprint_library.filter("model3")[0]
    
#     def reset(self):
#         self.collision_hist = []
#         self.actor_list = []
        
#         self.transform = random.choice(self.world.get_map().get_spawn_points())
#         self.vehicle = self.world.spawn_actor(self.model_3, self.transform)
        
#         self.actor_list.append(self.vehicle)
        
#         self.rgb_cam = self.blueprint_library.find("sensor.camera.rgb")
#         self.rgb.set_attribute("image_size_x", f"{self.im_width}")
#         self.rgb.set_attribute("image_size_y", f"{self.im_height}")
#         self.rgb.set_attribute("fov", "110")
        
#         transform = carla.Transform(carla.Location(x=2.5, z=0.7))
#         self.sensor = self.word.spawn_actor(self.rgb_cam, transform, attach_to=self.vehicle)
#         self.actor_list.append(self.sensor)
#         self.sensor.listen(lambda data: self.process_img(data))
        
#         self.vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))
#         time.sleep(4)
        
#         colsensor = self.blueprint_library.find("sensor.other.collision")
#         self.colsensor = self.world.spawn_actor(colsensor, transform, attach_to=self.vehicle)
#         self.actor_list.append(self.colsensor)
#         self.colsensor.listen(lambda event: self.collision_data(event))
        
#         while self.front_camera is None:
#             time.sleep(0.01)
            
#         self.episode_start = time.time()
#         self.vehicle.apply_control(carla.VehicleControl(throttle=0.0, brake=0.0))


# def collision_data(self, event):
#     self.collision_hist.append(event)
    
    
    
    
def process_img(image): 
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return 13/255.0
    
try:
    client = carla.Client("127.0.0.1", 2000)
    client.set_timeout(2.0)
    world = client.get_world()
    
    blueprint_library = world.get_blueprint_library()
    
    bp = blueprint_library.filter("model3")[0]
    print(bp)
    
    spawn_point = random.choice(world.get_map().get_spawn_points())
    
    vehicle = world.spawn_actor(bp, spawn_point)
    # vehicle.set_autopilot(True)
    
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0)) 
    actor_list.append(vehicle)
    
    cam_bp = blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
    cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
    cam_bp.set_attribute("fov", "110")
    
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    
    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda data: process_img(data))
    
    
    
    time.sleep(20)

finally:
    for actor in actor_list:
        actor.destroy()
    print("All cleaned up!") 

