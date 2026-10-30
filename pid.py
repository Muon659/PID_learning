import time

import matplotlib.pyplot as plt


# these functions can link up to a sensor

def measure_temp():
  return 20

def setpoint():
  return 100

def controller_on():
  return True

class auger_pid_controller:
  """PID Controller"""
  def __init__(self, kp, ki, kd, int_windup, sample_time):
    self.kp = kp
    self.ki = ki
    self.kd = kd
    self.int_windup = int_windup
    self.last_time = time.time()
    self.last_error = 1#self.setpoint - self.measurement (bug)
    self.sample_time = sample_time
    self.PTerm = 0
    self.ITerm = 0
    self.DTerm = 0
    self.clear()

  def clear(self):
    self.setpoint = 0.0

  def set_setpoint(self, setpoint):
    self.setpoint = setpoint

  def update(self, measurement):
    error = self.setpoint - measurement
    #print(error)
    #print(measurement)
    current_time = time.time()
    delta_time = current_time - (self.last_time-1)
    delta_error = error - self.last_error
    time.sleep(self.sample_time)
    if delta_time >= self.sample_time:
      self.PTerm = self.kp * error
      self.ITerm += error * delta_time
      if self.ITerm < -self.int_windup:
        self.ITerm = -self.int_windup
      elif self.ITerm > self.int_windup:
        self.ITerm = self.int_windup
      if delta_time > 0:
        self.DTerm = delta_error / delta_time
    self.last_time = current_time
    self.last_error = error
    #print(delta_error)
    output = self.PTerm + (self.ki * self.ITerm) + (self.kd * self.DTerm)
    return output

class fan_pid_controller(auger_pid_controller):
  pass

def main():
  #auger_pid = auger_pid_controller(0.1,0.5,0.11,10,2)
  fan_pid = fan_pid_controller(0.1,0.7,0.2,10,2)
  temp = measure_temp()
  temp_array = []
  #while controller_on() == True:
  setpnt = setpoint()
  for x in range(50):
    if x == 20:
      setpnt = 50
    #setpnt = setpoint()
    #auger_pid.set_setpoint(setpnt)
    fan_pid.set_setpoint(setpnt)
    #auger_output = auger_pid.update(temp)
    fan_output = fan_pid.update(temp)
    #temp += auger_output
    temp += fan_output
    temp_array.append(temp)
  plt.plot(temp_array)
  plt.show()
  print(temp)


if __name__ == "__main__":
  main()


