import numpy as np

class PoseEstimator:
    def __init__(self, front_radius=0.2, back_radius=0.2, dist_front_back=1.0, dist_wheels=0.75, \
                max_ticks=512.0, start_coord=[[1.0, 0.0],[0.0, 0.0]], start_heading=0.0, start_time=0.0):
        self.FRONT_WHEEL_RADIUS = front_radius      #meters
        self.BACK_WHEEL_RADIUS = back_radius        #meters

        self.DIST_FRONT_BACK = dist_front_back      #meters
        self.DIST_REAR_WHEELS = dist_wheels         #meters

        self.MAX_ENCODER_TICKS = max_ticks          #ticks

        self.FRONT_WHEEL_CIRCUMFERENCE = 2.0 * np.pi * self.FRONT_WHEEL_RADIUS      #meters

        #Items to track
        self.front_pos = start_coord[0]         #[x,y] front
        self.back_pos = start_coord[1]          #[x,y] back
        self.cur_time = start_time              #seconds
        self.cur_heading = start_heading        #radians

        #For readability
        self.X_COORD = 0
        self.Y_COORD = 1
        self.HEAD_VAL = 2

    def __get_x_y_head_diff(self, ang_move, dist):
        heading = (self.cur_heading + ang_move) % (2.0*np.pi)       #radians

        x_diff = np.cos(heading) * dist     #meters
        y_diff = np.sin(heading) * dist     #meters

        return [x_diff, y_diff, heading]

    def estimate(self, new_time, steer_angle, ticks, ang_vel):
        #=====FRONT POINT
        front_wheel_dist_traveled = (ticks / self.MAX_ENCODER_TICKS) * self.FRONT_WHEEL_CIRCUMFERENCE       #meters traveled

        front_diff_info = self.__get_x_y_head_diff(steer_angle, front_wheel_dist_traveled)      #[x,y,head]

        new_front_coords = [(self.front_pos[self.X_COORD] + front_diff_info[self.X_COORD]), (self.front_pos[self.Y_COORD] + front_diff_info[self.Y_COORD])]     #[x,y]

        #=====BACK POINT
        time_elapsed = new_time - self.cur_time     #new data is forward in time
        rotation_angle = ang_vel * time_elapsed     #radians

        back_diff_info = self.__get_x_y_head_diff(rotation_angle, self.DIST_FRONT_BACK)    #[x,y,head]

        new_back_coords = [(new_front_coords[self.X_COORD] - back_diff_info[self.X_COORD]), (new_front_coords[self.Y_COORD] - back_diff_info[self.Y_COORD])]    #[x,y]

        #=====SAVE NEWLY CALCULATED POSE INFO AS CURRENT
        self.cur_heading = back_diff_info[self.HEAD_VAL]
        self.front_pos = new_front_coords                   #[x,y]
        self.back_pos = new_back_coords                     #[x,y]
        self.cur_time = new_time                            #seconds

        #return (self.back_pos + [self.cur_heading]) #[x,y,heading]
        return self.front_pos + self.back_pos
