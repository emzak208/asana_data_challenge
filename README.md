#### Asana Data Science Challenge
##### Eric Chang

To reproduce the results, first place `takehome_users-intern.csv` and `takehome_user_engagement-intern.csv` into `/data`.

Replace the `REPO_PATH` variables with your local path, then run the adoption data creation script:
```
python3 src/create_adoption_data.py
```

To run the feature extraction step (the repository needs to be set in this script, also):
```
Rscript src/feature_engineering.R
```

The report in `reports/report.Rmd` can then be rendered using Rmarkdown.

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data               <- Datasets used in the analysis.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    └── src                <- Source code for use in this project.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>