import time

from random import randint

import matplotlib.pyplot as plt


class PIDcontroller:
  """PID Controller"""
  def __init__(self, kp, ki, kd, int_windup, sample_interval):
    self.kp = kp
    self.ki = ki
    self.kd = kd
    self.int_windup = int_windup
    self.last_time = time.time()
    self.last_error = 0
    self.sample_interval = sample_interval
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
    current_time = time.time()
    delta_time = current_time - (self.last_time-1)
    delta_error = error - self.last_error
    
    time.sleep(self.sample_interval)
    
    if delta_time >= self.sample_interval:
      self.PTerm = self.kp * error
      self.ITerm += error * delta_time

      # windup guard
      if self.ITerm < -self.int_windup:
        self.ITerm = -self.int_windup
      elif self.ITerm > self.int_windup:
        self.ITerm = self.int_windup

      # ensures that no division by zero occurs
      if delta_time > 0:
        self.DTerm = delta_error / delta_time
        
    self.last_time = current_time
    self.last_error = error
    output = self.PTerm + (self.ki * self.ITerm) + (self.kd * self.DTerm)
    return output

# main function sets the setpoint randomly, then randomly changes it halfway through the main loop
def main():
  pid = PIDcontroller(kp=0.1,ki=0.7,kd=0.2,int_windup=10,sample_interval=0.5)
  value = randint(50, 90)
  value_array = []
  setpnt = randint(75, 175)
  print(f"Inital Setpoint: {setpnt}")
  
  for x in range(50):
    if x == 25:
      setpnt = randint(50, 150)
    pid.set_setpoint(setpnt)
    pid_output = pid.update(value)
    value += pid_output
    value_array.append(value)
  
  plt.plot(value_array)
  plt.show()
  print(f"\nFinal Setpoint: {setpnt}")
  print(f"Final Value: {value}")


if __name__ == "__main__":
  main()
