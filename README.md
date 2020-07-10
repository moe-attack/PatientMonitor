# README    

### How to Run the App:  
1. From the command line, navigate to the directory containing App, then run one of the following commands
```
py -m App.Controller.ViewController 
```
or
```
python -m App.Controller.ViewController
```
2. Enter the `practitioner ID`, not the identifier. The app will get the identifier from the ID.  
3. Wait while the data is being fetched  
4. Once the data is fetched, a list of all the patients will be present on the right side of the screen  
5. Click a `button` next to a patient to follow them  
6. Click the same button to unfollow that patient  
7. The app updates every 20 seconds by default. You can change this by setting N to a different integer value in the top left corner under the practitioner login box.  
8. The app has a default X of 140 and default Y of 90

### How to Run the Machine Learning Algorithm  
1. Run all of the ANNR.R file. This saves the trained ANN in the file “./myModel.rds” and displays the accuracy, precision and recall of the model. Training the model takes 5-10 minutes  
2. Alternatively, you can read the model in a separate R file using readRDS(“./myModel.rds”).