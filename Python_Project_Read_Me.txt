1. The final project can be accessed through this Google Drive link: https://drive.google.com/drive/folders/1EMVyExIyRTomVXDZi2yuxlvgr1JXRmF9?usp=sharing.
2. Please refer to this video link for more information on the project: https://youtu.be/_yctNlVNzuw.
3. Before proceeding, download all the files from the drive.
4. Run the MFG_Project_Main_Code.py file and refer to the video link below for guidance before running the code.
5. The MFG_Project_Main_Code.py file runs two Python files as applications.
6. Upon running the file, the MFG598_Emotion_Detection.py code opens as app1, which captures an image of your current emotional state and saves it as a photo.png file.
7. The saved photo is then used to predict the emotion using the ferNet.h5 model, which uses KNN to predict emotion by comparing the facial photos in the train folder.
8. The ferNet.h5 model is a well-known model trained from FER2013 (Facial Expression Recognition 2013 Dataset).
9. The FER2013 contains approximately 30,000 facial RGB images of different expressions, with a size restricted to 48×48 pixels, and the primary labels of the dataset can be divided into seven types: 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral.
10. The predicted emotion is saved in the emotion_out.txt file.
11. Using the saved emotion_out.txt file, the second code, MFG598_Movie_Recommend_Emotion_Based.py, is opened as app2.
12. Seven CSV files have been created for movie recommendations based on specific emotions, namely anger, disgust, fear, happiness, neutral, sadness, and surprise. These files contain movie names, genres, and ratings for the respective emotions, and are based on research papers.
13. Based on the saved text file, the app will open the respective emotion.csv file and display the movie recommendation for the current emotion. If the user doesn't like the recommended movie, they can click the next button, which will recommend another movie a thousand times.
14. If the user likes the movie, they can press the movie button, which saves the movie name as selected_movie.txt.
15. In the future, if you wish to watch a movie similar to the recommended one, I have created another app that recommends movies based on the plot and content of the recommended movie, using the tmdb_5000_credits.csv and tmdb_5000_movies.csv files.
16. In the MFG598_Movie_Recommend_Content_Based.py app, the code first prompts the user to enter the movie name (case-sensitive). Based on the information provided, the app uses a TfidfVectorizer to convert the movie overviews into vectors and calculates the cosine similarity between them.
17. It then creates a mapping between movie titles and their corresponding indices in the dataset and finds the movies with the highest cosine similarity scores to the input movie title.
18. The app displays the top 10 recommended movies and allows the user to load more recommendations by clicking a button.
19. If the input movie name is not available in tmdb_5000_movies.csv, the app will prompt the user to input a different movie.
20. To close all the applications, press the Esc key.
