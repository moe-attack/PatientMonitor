# README    

This app simulates an monitor for medical professionals to monitor their patients' Cholesterol and Blood Pressure using API.
The app is meant to demonstrate understanding towards Software Engineering and the key principles for Object Oriented Programming.
The following principle were considered and carried out in the implementation:
- Open-Close Principle
- Single-Responsibility Principle
- Dependency-Inversion Principle
- Acyclic Dependencies Principle
- Common Reuse Principle

The application also implemented MVC design pattern to separate the logic concerns.


### Class Diagram
![Class Diagram](./Class\ Diagram.png)

### How to Run the App:  
1. From the command line, navigate to the directory containing App, then run one of the following commands
```
py -m App.Controller.ViewController 
```
or
```
python -m App.Controller.ViewController
```
2. Enter the `practitioner ID`, not the identifier. The app will get the identifier from the ID. (A sample ID is 3337)
3. Wait while the data is being fetched  
4. Once the data is fetched, a list of all the patients will be present on the right side of the screen  
5. Click a `button` next to a patient to follow them  
6. Click the same button to unfollow that patient  
7. The app updates every 20 seconds by default. You can change this by setting N to a different integer value in the top left corner under the practitioner login box.  
8. The app has a default X of 140 and default Y of 90
