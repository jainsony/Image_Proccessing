# PAPER WRITING

1. ABSTRACT




KEYWORDS: autonomous robot, path following, low maintainence, indoor robotics,
marker based robot, navigation, A-star



2. INTRODUCTION

    In modern robotics, there are lot of challenges like path finding, navigation, self-driven system and etc.
    so there are some segments we talk about and focus in some important points 

    2.1 What is mobile robot

        Robot localization, the ability of a mobile robot to determine its position and orientation within its environment, is crucial for autonomous operation. This process enables robots to navigate, interact with their surroundings, and perform tasks independently.

        A variety of sensors can be utilized for robot localization, each providing unique information about the robot's motion and surroundings. Odometry measures wheel rotations and other motion parameters to estimate changes in position. Encoders, rotary sensors that measure angular rotation, are often used for wheel rotation to estimate distance traveled. Gyroscopes measure angular rate of rotation, providing information about orientation and changes in orientation. Accelerometers measure acceleration of a body, providing data on speed and direction of travel. GPS provides absolute position outdoors, particularly useful for outdoor robots. LiDAR emits laser beams and measures reflection time to create 3D maps of the environment for position estimation. Cameras extract visual features like corners, edges, and landmarks, matching them to known maps for position estimation.

        The choice of sensors depends on the robot's environment and application. For instance, GPS-denied environments require LiDAR or cameras for localization.

        Once sensor data is gathered, localization algorithms are employed to estimate the robot's position and orientation. Common algorithms include dead reckoning, which estimates position by integrating odometry measurements over time but is susceptible to error accumulation; particle filtering, which utilizes a weighted set of particles to represent possible robot positions, offering better accuracy but higher computational demands; and Kalman filtering, a statistical state estimation algorithm that uses a model of robot motion to estimate position and orientation, balancing accuracy and computational efficiency.

        Robot localization presents several challenges, including sensor noise and uncertainty, as all sensors produce noisy and uncertain measurements, which must be considered when estimating position and orientation. Environmental dynamics, as dynamic and unpredictable environments can make it difficult to maintain accurate position estimation over time, and computational complexity, as some localization algorithms are computationally expensive, limiting their use on robots with limited resources.

        Despite these challenges, robot localization is an active research area, with researchers developing new sensors and algorithms to improve accuracy and reliability in diverse environments. As these advancements continue, autonomous mobile robots will become increasingly capable of operating in complex and dynamic environments.

        This paper is based on robot can be control wihtout using a bit of machine learning models, and at low computation[reference a* requires huge memory], specifically in indoor robotics but with some limitations.

    2.2 Environment

        Environment is  the crucial factor for robot different types of robot are made to 

        different types ke robot bnaye jaate hai alag-alag environment ke liye kyuki hr Environment characterstics alag hoti hai jese indoor robotics ki baat ki jaaye to surface plane hona bhaut jarrori hota hai jisse calculation constraints simple rhe or koi complexity increase na ho. 

        In various appproaches, robotist uses map which are generated with help of lidars, some of them dont generate the whole area map they only use local map [reference]
        hence in this approach there system works using the visuals what robot sees.

        In our system we tried something different we only use camera and observe environment for robot and continue our further navigation.

    2.3  About maintenence 

        It requires lot of software engineers or in main context I mean is to code the whole system whicle is very complex.
        and lot of expensive sensors is used.
        Lot of computation require to render the information from sensor and as well for number of complex algorithms.
        It is made up of different algorithms and to apply those algorithms we need different softwares like
        In modern robotics researchers and people uses ROS for indoor and outdoor robotics systems [references]
        
        But in our research our system only works on Image processing based system and it may possible for better accuracy cheap sensors can be used.
        It is semi autonomous system and can be done fully autonomous after some configuration
    

3. Methods and Materials

    3.1 Respective and base frame

        We have the main frame which is camera and it will treat as an static frame one it is fixed then by continously capturing frames we can update our obstacles.
        which helps us to prevent collision of robot from obstackles.

        Once the system is fixed, we detect our robot in the frame by marker based detection [reference] so many people uses marker based object identification [reference] once it is set we can initialise some sub-destination points which will lead the robot to the destination point.
            
        we can also use multiple robots with different markers for different robots as every robot will be at different positions.

    3.2 Path finding algorithm

        the Pythagorean theorem is employed as a fundamental tool to determine the shortest distance between the detected robot's position and its intended destination. The theorem, which states that the square of the hypotenuse of a right-angled triangle is equal to the sum of the squares of the other two sides, provides a direct and efficient method for calculating the straight-line distance between two points in a two-dimensional space. reference[].

        By treating the robot's current coordinates and the destination coordinates as the endpoints of the hypotenuse and one of the legs of a right triangle, respectively, the Pythagorean theorem allows us to calculate the length of the hypotenuse, which represents the shortest path between the two points. This approach eliminates the need for complex pathfinding algorithms and ensures that the robot takes the most direct route to its destination.

        diagrams

        The application of the Pythagorean theorem in this context demonstrates its versatility as a mathematical tool and highlights its relevance in various fields, including robotics and path planning. reference[pythogorus used for path planning]

        The sub-destination points and main destination point itself works as an attraction point another it can be said as SINK POINT.
        and the coordinate where the robot is detected is a source point.

    # This gave us the idea of vector filed

    3.3 Robot localisation and navigation 

        Robot is detected by marker identification approach [reference] we are using color masks to get the robot location in another words coordinates of robot.
        For marker we are using masking based marker there are two masks applied one to locate robot and another to calculate orientation with respect to main frame which fixed and static.

        as our system is set and we have sub-destination points we can easily calculate our shortest distance using Pythagorean theorem and its orientation with respect to main frame using Laws of cosines.

        diagrams


    3.4 PID Controller

        Now we have all the elements which we require to use our system, to further more enhancement of system we can use PID controller as we are mostly dealing with collection of straight path.

        If we more talk about PID Controller, It is difficult to tune for complex paths but in our case we have mostly collection of straight line paths.
        PID applied to control speed and turning angles for the robot

        show data without PID, with PID

        diagrams

        and some explaination license

4. Results

    4.1 masking based marker detection

    4.2 data 

    - time to reach from point to gloal point.
    using A* and without A*(predefined paths)

    - command generation optimisation
    time & using pid and without pid 


5. Conclusion

    

        # reference in indoor robotics there is a 
        # system called move base which uses following [key points] we can take that  













TOPICS
- my point is 
in which kind of path robot can move faster and archieve the goal point.
focusing on [low cost, less data, easy handling, low computaiton:energy efficient]
not that which is best algorithm for path finding.

- Challenges
odometry itself is a very big challenge to solve for accurate odometry the encoder data should be precisely correctly.[give some reference]

as we talk about static map, map needs to be made to localise the robot 

Discription:
Autonomous drive robot for indoor robotics

Mobile Robotics

Mobile robotics is a field of robotics that deals with the design, construction, operation, and application of robots that can move around their environment. Mobile robots are used in a wide variety of applications, including:

Autonomous navigation: 
Mobile robots can be programmed to navigate through their environment without human intervention. This is useful for tasks such as delivering goods, cleaning floors, and inspecting infrastructure.
    example - as we can see this in industries for supply chain management.
    
Exploration and mapping: 
Mobile robots can be used to explore unknown environments and create maps. This is useful for tasks such as search and rescue, disaster relief, and environmental monitoring.
    example - If there is unfamiliar environment these robots can be used for research purposes like in mars rovers those robots works on the similar phenomena
