Capstone project work started.

#1 First step is to set up a Git Repo - Created a remote repo and cloned it in local.
    a) Created capstone_project private repo.
    b) Adding a README.md to it in the first commit.

#2 Added a new branch called 'my-work-branch'
    a) Merged It

#3 Added Extraction and Transform functionality in 'main' branch directly

#4 Added 'application-front-end' branch to create a small menu for front-end requirements
    a) pip install streamlit - Streamlit is an open source app to build small apps
    b) pip install 'protobuf~=3.20.0' - Streamlist ddid not work with protobuf 4.23.2 version I had so installed the compatible version
    c) pip install streamlit-aggrid - Display results in aggrid format

#5 Added Plots using Plotly
    a) #pip install plotly

#6 Remove all unused files and merge the 'application-fron-ent' branch in 'main' branch

#7 Commit with all Loan App API requirement 5 finished.



Technical Difficulties and Research

1. MySQL connection was not passed on from an import file/connection function when required. To get around this problem the initial fix made was to get the mysql connection and close it multiple times.
2. Related to MySQL - Last requirement was done with only one connection request
3. Researched for solutions to display/update results in a more user friendly way - thats how streamlit was chosen