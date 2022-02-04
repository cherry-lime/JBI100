# Visualization tool for the course Visualization (JBI100) - Group 6

## About this app

This is the visualization tool making use of the Great Britain Road Safety date set

## Requirements

* Python 3 (add it to your path (system variables) to make sure you can access it from the command prompt)

## How to run this app

We suggest you to create a virtual environment for running this app with Python 3. Start by unzipping the project in the folder you want to save it
and open your terminal/command prompt in the root folder.


Start by opening the command prompt
cd into the folder where you want to save the files and run the following commands.

```
> cd <folder name on your computer>
> python -m venv venv
```
If python is not recognized use python3 instead

In Windows: 

```
> venv\Scripts\activate
```
In Unix system:
```
> source venv/bin/activate
```

Install all required packages by running:
```
> pip install -r requirements.txt
```

Run this app locally with:
```
> python app.py
```
You will get a http link, open this in your browser to see the results. You can edit the code in any editor (e.g. Visual Studio Code) and if you save it you will see the results in the browser.

## What we changed

We took the provided template code to use as a base for our tool. We used the code for the layout (as we have the graphs on the right side and the menu for selecting attributes and changing graphs on the left side). However, we added the rest ourselves. 
We made use of the libraries Dash and Plotly to render the graphs. We made use of the library Pandas to process the data set.

## Resources

* [Dash](https://dash.plot.ly/)
* [Plotly](https://plotly.com/)
* [Pandas](https://pandas.pydata.org/)
