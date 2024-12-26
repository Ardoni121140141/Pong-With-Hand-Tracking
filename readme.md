<div align="center">
<img src="Images/Mentahan/BIReadme.png" width="100%" />
<h1> Pong With Hand Tracking </h1>

[![Github Commit](https://img.shields.io/github/commit-activity/m/Ardoni121140141/Tubes-Multimedia---Pong-With-Hand-Tracking)](#)
[![Github Contributors](https://img.shields.io/badge/all\_contributors-3-blue.svg)](#)
</div>

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Table Of Contents**
[Introduction]()

[Member Of Team](#member-of-team)

[Role & Position Member Of Team](#id--position-member-of-team)

[Technology Application](#technology-application)

[Installation Steps](#installation-steps)

[Weekly Logbook](#weekly-logbook)

[Report](https://www.overleaf.com/read/xpcxmdtnpbxt#63b1b0)

[Program Demonstration](#program-demonstration)

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Introduction**
This project combines the concept of the classic game Pong with motion tracking technology. In this program, the user moves the paddle by utilizing hand movements detected through a webcam camera. This project uses MediaPipe to detect the user's finger position in real-time, and Pygame to display game elements such as the ball, paddle, and score on the screen. This project is an assignment from the Multimedia Systems/Technology course with the Course code IF4021 taught by Lecturer Mr. Martin Clinton Manullang, S.T., M.T.

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Member Of Team**
| [<img src="Images/Mentahan/Ardoni.png" width="100px;"/><br /><sub><b>Ardoni Yeriko</b></sub>](https://github.com/Ardoni121140141)<br /> 121140141 <br /> | [<img src="Images/Mentahan/Kevin.png" width="100px;"/><br /><sub><b>Kevin Simorangkir</b></sub>](https://github.com/kevinsimorangkir21)<br />121140150 <br /> | [<img src="Images/Mentahan/Rizki.png" width="100px;"/><br /><sub><b>Rizki Alfaina</b></sub>](https://github.com/RizkiAlfaina) <br/> 12140228 <br /> |
|--|--|--|

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **ID & Position Member Of Team**
<div align="left">

| Name | ID Student | Username
| :---: | :---: | :---: |
| Ardoni Yeriko Rifana Gultom   | 121140141 | Ardoni121140141
| Kevin Simorangkir             | 121140150 | kevinsimorangkir21
| M. Rizki Alfaina              | 121140228 | RizkiAlfaina

</div>

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Technology Application**
<div align="left">

| Technology | Name | Description |
| :---: | :---: | :---: |
| <img src="Images/Logo Apps/Python.png" style="width:50px;"/> | **Python** | Python is an interpreted, high-level and general-purpose programming language. Python's design philosophy emphasizes code readability with its notable use of significant whitespace. |
| <img src="Images/Logo Apps/Pygame.png" style="width:50px;"/> | **Pygame** | Pygame is a cross-platform set of Python modules designed for writing video games. It includes computer graphics and sound libraries designed to be used with the Python programming language. |
| <img src="Images/Logo Apps/Mediapipe.png" style="width:50px;"/> | **MediaPipe** | MediaPipe is a cross-platform framework for building multimodal applied machine learning pipelines. MediaPipe is used for object detection, face detection, hand tracking, and pose detection. |
| <img src="Images/Logo Apps/OpenCV.png" style="width:50px;"/> | **CV2** | CV2 is a library used for computer vision and machine learning. It is used for image processing, object detection, and other computer vision tasks. |

</div>

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Installation Steps**
### <img src="Images/Mentahan/Panah2.png" width="30px;"/> **Preparation of Needs**
Some of the preparations needed to carry out this research project are as follows:

<li> Install python software/code first </li>

```bash
https://www.python.org/downloads/
```

<li> After installing, first check whether Python has been installed properly using the following command, make sure the Python version you are using is between 3.10 and 3.12. : </li>

```bash
python --version
```

<li> Once the python version appears, please open a text editor that supports it such as Visual Studio Code and the web-based Google Collab. Here are the links to use both (please download and install) :</li>

```bash
[Software VISUAL STUDIO CODE](https://code.visualstudio.com/)
```

```bash
[Software GOOGLE COLLAB](https://colab.research.google.com/)
```

### <img src="Images/Mentahan/Panah2.png" width="30px;"/> **Program Running Stage**
<li> Open a terminal / something like GitBash etc. Please clone this Repository by following the following command and copy it in your terminal: </li>

```bash
git clone https://github.com/Ardoni121140141/Pong-With-Hand-Tracking.git
```

<li>Please change the directory to point to the clone folder with the following command:</li>

```bash
cd Pong-With-Hand-Tracking
```

<li> To install requirements, please use the following command: </li>

```bash
pip install -r requirements.txt
```

<li> After that, please run the following command to run the program:</li>

```bash
python main.py
```

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Weekly Logbook**
| Week | Task | Person | Status |
| :---: | :---: | :---: | :---: |
| Week 1 | - Installing OpenCV, Pygame and Mediapipe modules <br> - Save the requirements.txt file for the purpose of installing dependencies. <br> - Creating basic code to detect hand gestures using MediaPipe | Ardoni Yeriko & Kevin Simorangkir | Done |
| Week 2 | - Creating a Paddle in a Pong Game (`paddle.py`) <br> - Creating a Pong game using Pygame, Creating a collision detection system and check the winner (`game.py`) <br> - Implementing hand tracking using MediaPipe for Game Pong (`main.py`) <br> | Ardoni Yeriko, Kevin Simorangkir & Alfaina | Done
| Week 3 | - Implementing the game logic for the Pong game <br> - Finalizing the program code <br> - Preparation and Finalization of the Report <br> | Ardoni Yeriko, Kevin Simorangkir & Alfaina | Done |
| Week 4 | - Finalizing the report and code <br> -  Collecting programs and reports | Ardoni Yeriko, Kevin Simorangkir & Alfaina | Done |

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Report**
The following is a report of the program that we made: 
[Report](https://www.overleaf.com/read/xpcxmdtnpbxt#63b1b0)

## <img src="Images/Mentahan/Panah.svg" width="30px;"/> **Program Demonstration**
The following is a demonstration of the program that we made:

<a href="https://youtu.be/9QVruUd-VEs?si=4nSlnVnqBwENb50m" target="_blank">
  <img src="https://i.ytimg.com/vi/9QVruUd-VEs/maxresdefault.jpg" alt="Presentation Video">
</a>
