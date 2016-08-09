#### Animal Wildlife Estimator Using Social Media (A.W.E.S.O.M.E.)
##### Author: Sreejith Menon

###### Project home-page: https://smenon8.github.io/AnimalWildlifeEstimator/
###### Project Description : 
Identify and quantify bias of human photographers when it comes to sharing pictures of animals on social media. 
The project broadly attempts to build a population estimation model of a particular species in a particular region using pictures which are shared as public albums in social media. For purposes of simulating the shared pictures on social media, data was generated from Amazon Mechanical Turk jobs. Amazon Mechanical Turk is used to ask random virtual workers from across the globe asking them if they will or will not share a particular image in a group of 20 images. 

2 experiments have been conducted till date. 


###### Features implemented - to date
* Extract features from IBEIS through a function call.
* Completely automated the process for selection of images and creation of Amazon Mechanical Turk jobs.
* Completely automated deployment, approval and download for all the mechanical turk jobs.
* Completely automated parsing of .results file from the mechanical turk engine and return a python object/csv/json ready for processing.
* API available for both single as well multiple feature extraction for an images or a list of images (can be specified as a csv).
* API available to join features with the results and return python data-frames/csv/json for statistical calculation.
* API available for generating rank list of most shared pictures.
* API available for generating rank list by share proportion based on ecological features like species, sex, age, view_point of the animal.
* API available for generating rank lists for a specific feature across all albums or individual albums (number of shares for zebra in a particular album versus number of shares for giraffes etc.)
* API available to append the results from Amazon Mechanical Turk API with tags from Microsoft Image Tagging API and generate a rank list of most shared tags.
* Added functionality to generate reports of all statistics in HTML format with bar charts wherever necessary.
* API available for data prepartion for applying classifiers using the Bag-of-words methodology.
* API available for building learning models like Logistic Regression, Support Vector Machines, Decision Trees and Random Forests and returning the predictions as well as performance metrics for the classifier.
* API available for visualizing the shared/not shared pictures on map and create clusters of share-no share homogenous region.



