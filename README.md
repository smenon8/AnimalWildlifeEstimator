#### Animal Photo Bias Scripts
##### Author: Sreejith Menon

###### Project home-page: http://compbio.cs.uic.edu/~sreejith/PhotoBias.html

###### Features implemented - to date
1. Create mechanical turk jobs - only user input needed is number of jobs we need.

2. Create deployment, approval and download scripts for all the mechanical turk jobs.

3. Parse .results file and have a python object/csv/json ready for processing. 

4. Extract all essential features given a list of images (can be specified as a csv)

5. Join features with the results and return python data-frames/csv/json for statistical calculation.

6. Generate general rank lists (by number of shares per images, species, age etc.)

7. Generate a per job rank list (number of shares for zebra in a particular album versus number of shares for giraffes etc.)

8. Generate rank list by share proportion based on ecological features like species, sex, age, view_point of the animal.

9. Generate rank list by share proportion based on album features and other image EXIF information.

10. Append the results from Amazon Mechanical Turk API with tags from Microsoft Image Tagging API and generate a rank list by share proportion.

11. Build a regression model with all the ecological factors and tags from Microsoft Image Tagging API using the bag-of-words model.

12. Evaluate various performance metrics of the learned algorithm using parameters like ROC/AUC, RSS, RMSE and F-scores.





