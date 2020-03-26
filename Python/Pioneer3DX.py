import sim

class Pioneer3DX:

    def __init__(self, clientID):
        self.clientID = clientID
        self.pioneer3DX_array = [None] * 19
        self.position_coordX = [None] * 3
        self.position_coordXc = [None] * 3
        self.velocity = [None]* 2
        self.name = "Pioneer_p3dx"
        self.left_motor = 'Pioneer_p3dx_leftMotor'
        self.right_motor = 'Pioneer_p3dx_rightMotor'
        self.ultrasonic_sensors = "Pioneer_p3dx_ultrasonicSensor"
        ### Load Mobile Robot Pioneer parameters
        # self.pioneer3DX_array[0] represents the entire mobile robot block
        # self.pioneer3DX_array[1] represents only the left motor 
        # self.pioneer3DX_array[2] represents only the right motor
        error,self.pioneer3DX_array[0] = sim.simxGetObjectHandle(self.clientID,self.name,sim.simx_opmode_blocking)
        error,self.pioneer3DX_array[1] = sim.simxGetObjectHandle(self.clientID,self.left_motor,sim.simx_opmode_blocking)
        error,self.pioneer3DX_array[2] = sim.simxGetObjectHandle(self.clientID,self.right_motor,sim.simx_opmode_blocking)

        # self.pioneer3DX_array[3:18] represents the 16 ultrasonic sensors
        num = 1
        while num < 17:
            error,self.pioneer3DX_array[2+num] = sim.simxGetObjectHandle(self.clientID,self.ultrasonic_sensors+str(num),sim.simx_opmode_blocking)
            num+=1


        error, linearVelocity, angularVelocity = sim.simxGetObjectVelocity(self.clientID,self.pioneer3DX_array[0], sim.simx_opmode_streaming)
        error, position = sim.simxGetObjectPosition(self.clientID,self.pioneer3DX_array[0],-1, sim.simx_opmode_streaming)
        error, angle = sim.simxGetObjectOrientation(self.clientID,self.pioneer3DX_array[0],-1,sim.simx_opmode_streaming)
        print("Pioneer 3DX loaded")
        

    def send_ControlSignals(self,Ud):
        # left_speed = (v - e w)/R 
        # right_speed = (v + e w)/R
        # Ud[0] is the linear velocity given as parameter
        # Ud[1] is the angular velocity given as parameter
        # e is half of the distance between the left and right wheels
        # R is the radius of the wheels
        R = 0.0925
        e = 0.17

        left_speed  = (Ud[0] - e*Ud[1])/R
        right_speed = (Ud[0] + e*Ud[1])/R

        # Send Control Signal to each motor (first left and second right)
        error = sim.simxSetJointTargetVelocity(self.clientID,self.pioneer3DX_array[1],left_speed,sim.simx_opmode_streaming)
        error = sim.simxSetJointTargetVelocity(self.clientID,self.pioneer3DX_array[2],right_speed,sim.simx_opmode_streaming)



    def get_PositionData(self):
        error, linearVelocity, angularVelocity = sim.simxGetObjectVelocity(self.clientID,self.pioneer3DX_array[0], sim.simx_opmode_buffer)
        ## Pioneer Position
        error, position = sim.simxGetObjectPosition(self.clientID,self.pioneer3DX_array[0],-1, sim.simx_opmode_buffer)
        ## Pioneer Orientation (alpha, beta e gama)
        error, angle = sim.simxGetObjectOrientation(self.clientID,self.pioneer3DX_array[0],-1,sim.simx_opmode_buffer)
        
        # Linear Transform to find the Control Point
        #X = Xc + [0.15*cos(orientation(3)); 0.15*sin(orientation(3))]; 
        
        print(position)

    #def get_UltrasonicData(self):

    