# Image Database for Everyday Affective Spaces (IDEAS): an open-access database of standardized high-quality images of indoor environments

Please read this before using the IDEAS dataset. This folder contains the code and materials for the Image Database for Everyday Affective Spaces (IDEAS) dataset. The dataset is also available in [OSF](https://osf.io/g9ze5/). You can find the article [here](), and can contact the corresponding author by sending an email to `f.c.deniz@tue.nl`.

## Repository Structure

This repository seperated into multiple folders for processing the raw dataset and running the statistical analysis, explained below.

`Raw Data`: this folder contains the anonymized raw data collected from all studies. Within this folder, subfolders starting with `A` corresponds to arousal studies where participants rated tense arousal and energetic arousal. Subfolders starting with `V` correspond to valence studies where participants rated valence and approach-avoidance. **__The accompanying number indicates the study number: each study corresponds to a specific subset of images that were evaluated by participants from the total set of 1800 images. Overall, each image was evaluated by 24 raters.__**. `labjs_anonymized.csv` includes anonymized ratings collected in the study and `demographic_anonymized.csv` includes anonymzied demographic data of participants.

`Images`: this folder contains images collected in the IDEAS dataset.

`Data for equivalence testing`: this folder contains the processed individual ratings for all dependent variables used to conduct the two one-sided tests of equivalence (TOST). This dataset includes individual ratings from Deniz et al. (2025) for the nine reference images, as well as the ratings collected in our study. 

`Data for ICC analysis`: this folder contains the processed data for calculating ICC for all dependent variables.

`Data for demographic analysis`: this folder contains the processed demographic information obtained from Prolific. The files `valence_demographics_only.csv` and `arousal_demographics_only.csv` include only the demographic data of participants who took part in the two studies. The files `valence_demographic.csv` and `arousal_demographic.csv` include both participants’ demographic information and their individual ratings.

`Visual Features` folder includes low-, mid-, and high-level visual features that were extracted from images in IDEAS dataset. For more information about these visual features and how they were quantified please see Deniz et al. (2025).

`Attribution Data`: this folder contains all the information required to give correct attribution to image owners. For further information about the recommended practices for giving attritbution see section "Generate copyripght information".

`Mean Data`: this folder contains the mean ratings for all images across all dependent variables.

### Software requirements and data processing

The data processing for the IDEAS dataset is done in Python, and the statistical analysis run in R. 

#### Raw data processing in Python

We provide the processed data (e.g., mean ratings per image), but you can also process the raw data yourself using Jupyter Notebook and the file `Procesing Code\process.ipynb`. This notebook processes the raw data and converts it into several formats required for the statistical analyses. Specifically, it generates ICC data, which are saved in the `Data for ICC analysis` folder; demographic data, which are saved in the `Data for demographic analysis` folder; equivalence data, which are saved in the `Data for equivalence testing` folder; and mean scores, which are saved in the `Mean Data` folder. For more details on how the data are processed, see `useful_functions.py`.  
  
For Python, you can create a new virtual environment by first running `conda create --name IDEAS python==3.10` in the terminal. You can find more information about how to install conda [here](http://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). Following this, you can run `python -m pip install -r requirements.txt` to install all required packages in Python. **\[FIX\] (Note to self: This is missing flickrAPI and geopandas, add them later!!)**

`missing_ids.txt` includes anonymized participants ID of participants who removed from the dataset and analysis.

#### Statistical analysis

All statistical analyses conducted for the paper are documented in `Statistical Analysis Code\AIDEI.Rmd`, and all utility functions used in these analyses are provided in `utils.R`. Running or knitting `AIDEI.Rmd` reproduces all statistical analyses reported in the paper and generates all tables and figures included in the study.

### Generate copyright information

All images in the IDEAS dataset were collected from Flickr. Although all images were shared under Creative Commons licenses, the specific terms for attribution, use, and adaptation vary across images. Future studies should follow the relevant copyright requirements and provide appropriate credit to the original owner whenever the images are shared. All information needed for attribution is available in the `Attribution Data` folder. For additional guidance on recommended attribution practices, see https://wiki.creativecommons.org/wiki/Recommended_practices_for_attribution. More information about attribution data collected from FlickrAPI see https://www.flickr.com/services/api/flickr.photos.search.html and https://www.flickr.com/services/api/misc.urls.html. 

In addition, you can run `image_attribution.py` to generate attributions for images in the IDEAS dataset. To do so, replace `images_used` in the script with the names of the images for which you want attribution, and then run `python image_attribution.py`.

You can also retrieve metadata for images in the IDEAS dataset using the Flickr API. The file `get_metadata.py` provides an example of how we extracted location metadata and plotted these data. To use the Flickr API, you will need an API key, which can be requested from https://www.flickr.com/services/api/.

## Citation

If you use (part of) this dataset or code for your research, please cite our paper (place holder for now):

```
Deniz, Fatih Celalettin, Kynthia Chamilothori, Sanne Schoenmakers, and Yvonne De Kort. “Do (Not) Enter? Objective Visual Features of Indoor Scenes Predict Approach-Avoidance Responses and Core Affect.” Journal of Environmental Psychology, July 2025, 102686. https://doi.org/10.1016/j.jenvp.2025.102686.
```

## References

Deniz, F. C., Chamilothori, K., Schoenmakers, S., & de Kort, Y. (2025). Do (not) enter? Objective visual features of indoor scenes predict approach-avoidance responses and core affect. *Journal of Environmental Psychology*, 102686.