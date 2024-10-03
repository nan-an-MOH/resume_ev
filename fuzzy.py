from fuzzywuzzy import fuzz
from math import sqrt

skills_ds_p1 = {
    'statistic' : ['statistic','statistics','statistical'],
    'regression' : ['regression'],
    'python' : ['python'], 
    'sas' : ['sas'],
    'model' : ['model', 'models', 'modeling', 'modelling'], 
    'machine learning' : ['ml', 'machine learning'],
    'artificial intelligence' : ['ai', 'artificial intelligence'],
    'data science' : ['data science', 'data scientist'],
    'nlp' : ['natural language process', 'natural language processing', 'nlp'],
    'data' : ['data']
}

skills_ds_p2 = {
    'healthcare' : ['healthcare', 'health care'],
    'sql' : ['sql', 'postgresql', 'mysql', 'sqlite'],
    'excel' : ['excel'], 
    'database' : ['database', 'databases', 'dbms'], 
    'communication' : ['communication'],
    'power bi' : ['power bi'], 
    'dashboard' : ['dashboard', 'dashboards', 'dashboarding'], 
    'visualization' : ['visualisation', 'visualization', 'visualizations', 'visualisations'], 
    'neural networks' : ['neural networks', 'neural network', 'gan', 'cnn', 'rnn'],
    'deep learning' : ['deep learning'],
    'spacy' : ['spacy'],
    'bert' : ['bert'], 
    'hugging face' : ['hugging-face', 'hugging face', 'huggingface'],
    'large language model' : ['llm', 'llms', 'large language model', 'large language models'], 
    'biostatistic' : ['biostatistic','biostatistics','biostatistical', 'bio-statistic', 'bio-statistics', 'bio-statistical'],
    'epidemi' : ['epidemiology','epidemic','epidemical'], 
    
}

skills_ds_p3 = {
    'databricks' : ['databricks'],
    'aws' : ['aws', 'amazon web services'],
    'azure' : ['azure'],
    'sagemaker' : ['sagemaker'],
    'pytorch' : ['pytorch'],
    'tensorflow' : ['tensorflow'],
    'keras' : ['keras'],
}

extracurricular = {
    'hackathon': ['hackathon'],
    'competition': ['competition'],
    'volunteer': ['volunteer'],
    'certificate': ['certificate'],
    'online courses': ['online courses'],
    'club': ['club']
}

skill_list = [skills_ds_p1, skills_ds_p2, skills_ds_p3, extracurricular]

def evaluate(skill_dict, full_text):
    skill_list = list(skill_dict.values())
    cat_list = []
    for category in skill_list:
        score_list = []
        for skill in category:
            score_list.append(fuzz.token_set_ratio(skill, full_text))
        cat_list.append(max(score_list))
    sum0, sum1 = 0, 0
    for n in cat_list:
        sum0 = sum0 + n * n
        sum1 = sum1 + 100 * 100
    return (sqrt(sqrt(sqrt(sqrt(sum0/sum1)))))


if __name__ == "__main__":
    pass