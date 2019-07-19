# Pose Estimator

## class PoseEstimator(front_radius=0.2, back_radius=0.2, dist_front_back=1.0, dist_wheels=0.75, max_ticks=512.0, start_coord=[[1.0, 0.0],[0.0, 0.0]], start_heading=0.0, start_time=0.0)

Create an object which is able to calculate the estimated pose of a tricycle platform on a 2D plane. The default values of the optional parameters are set to the given values in the code challenge specification. front_radius is the radius of the front wheel, back_radius is the radius of the back wheel, dist_front_back is the distance from the middle of the back axle to the pivot point of the front wheel, dist_wheels is the distance between the two wheels on the back axle, max_ticks is the number of ticks the encoder uses for a full revolution, start_coord is the list of [x,y] coordinates for the front and back, start_heading is the initial heading pose of the platform, and start_time is the starting reference time. When a new set of data is provided to the estimate method of this class, the new position is calculated and the internal reference data is updated to the new position data. This allows for continuous pose estimation for the platform over time.
   
The PoseEstimator class provides one method.

### estimate(new_time, steer_angle, ticks, ang_vel)

Estimate the new pose of the platform provided new time, steering angle, encoder ticks, and angular velocity. new_time is the time corresponding to the data passed in, steer_angle is the angle of the front wheel about the z axis (90 to -90 deg), ticks is the number of encoder ticks, and ang_vel is the angular velocity of the platform. This method will calculate and return the [x,y] coordinates of the center of the back axle and the platform heading in a list [x,y,heading]. 

### ex.
import numpy as np

time = 1.0        
steer_angle = 0.349
encoder_ticks = 512.0
ang_vel = np.pi/10.0

pose_info = PoseEstimator()
print(pose_info.estimate(time, steer_angle, encoder_ticks, ang_vel))

#### output:
[1.229824356966546, 0.12070043294093746, 0.3141592653589793]

# LIDAR Filters

## class RangeFilter(min_range, max_range)

Create an object which will provide a range filtering mechanism for LIDAR scan data. min_range is the minimum range for the filter, and max_range is the maximum range for the filter. 

The RangeFilter class provides one method.

### update(scan_data)

Applies the range limits set on object creation. scan_data is the data array from the LIDAR sensor. The method returns a list of equal length as scan_data that contains the values from scan_data with values below the minimum range set to the min_range value, and values above the maximum range set to the max_range value.

### ex.

filter = RangeFilter(1,3)

test_arr = [1, 2, 3, 4, 5, 0, 0, -1]

print(filter.update(test_arr))

#### output:
[1, 2, 3, 3, 3, 1, 1, 1]

## class TemporalMedianFilter(num_prev_scans)

Create an object which will provide a temporal median filtering mechanism for LIDAR scan data. num_prev_scans is the number of previous scans to use to calculate the new median for filtering. 

The TemporalMedianFilter class provides one method.

### update(scan_data)

Applies the filter using the number of previous scans set on creation. scan_data is the data array from the LIDAR sensor. The method returns a list of equal length as scan_data that contains the values resulting from taking the median of scan_data with the n number of previous scans specified.

### ex.

filter = TemporalMedianFilter(1)

test_arr_one = [0.0, 1.0, 2.0, 1.0, 3.0]
test_arr_two = [1.0, 5.0, 7.0, 1.0, 3.0]

print(filter.update(test_arr_one))
print(filter.update(test_arr_two))

#### output:
[0.0, 1.0, 2.0, 1.0, 3.0]
[0.5, 3.0, 4.5, 1.0, 3.0]
