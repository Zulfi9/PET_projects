import streamlit as st
from typing import List, Set, AnyStr

import pandas as pd
from .utils import parse
import ast


@st.cache_data
def _load_base (path: str, index_col:str = 'id') -> pd.DataFrame:
    """ Load csv file to pandas.DataFrame"""
    db = pd.read_csv(path, index_col = index_col)
    db.index = db.index.astype(int)
    return db


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        """ Class init function, Load similarity matrix """
        self.distance_all = _load_base(distance_filepath, index_col = 'id')
        self.distance_all.columns = self.distance_all.columns.astype(int)
        self.distance = self.distance_all # copy ()
        # self.distance.index = self.distance.index.astype(int)
        # self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        """ Load movies db """
        self.movies_all = _load_base(movies_dataset_filepath, index_col='id')        
        self.movies_all['genres'] = self.movies_all['genres'].apply(parse)
        self.movies_all['years'] = pd.DatetimeIndex(
            self.movies_all.release_date).year.fillna(0).astype(int)
        self.movies_all['title_year'] = self.movies_all['title_x'] + \
        ' ('+self.movies_all['years'].astype(str)+')'
        self.movies_all['director'] = self.movies_all['crew'].apply(lambda x: "".join(
            [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director']))
        # self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        # self.movies.index = self.movies.index.astype(int)
        # self.movies['genres'] = self.movies['genres'].apply(parse)
        self.movies = self.movies_all

    def get_titles(self) -> List[str]:
        # return self.movies['title'].values
        return self.movies_all['title_year'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies_all['genres'].values.tolist() for item in sublist]
        return set(genres)
    
    def get_years(self) -> Set[str]:
        return set(self.movies_all.years)
    
    def get_film_id(self, title_year:str) -> int:
        return self.movies_all.loc[self.movies_all.title_year == title_year].index[0]
    
    def get_film_director(self, id: int) -> int:
        return self.movies_all.loc[id].director
    
    def get_film_genres(self, id: int) -> List[str]:
        return self.movies_all.loc[id].genres
    
    def get_similarity(self, id1: int, id2: int) -> AnyStr:
        return str(round(self.distance[id1][id2]*100))
    
    def get_film_original_title(self, id: int) -> AnyStr:
        return self.movies_all.loc[id].original_title
    
    def get_film_overview(self, id: int) -> AnyStr:
        return self.movies_all.loc[id].overview


    
    def set_filter(self, year: int, genre: str) -> None:
        self.movies = self.movies_all
        if year:
            # movie rows filtered
            self.movies = self.movies.loc[self.movies.years == year]
        if genre:
            self.movies = self.movies.loc[self.movies.genres.apply( #movies row
                lambda x: genre in x)]
            # distance row filtered
            self.distance = self.distance.loc[self.movies.index]

    def remove_filter(self) -> None:
        self.movies = self.movies_all
        self.distance = self.distance_all
        


    def recommendation(self, title_year: str, top_k: int = 5) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        # filtered = self.movies.genres
        indices = pd.Series(
           self.movies_all.index, index = self.movies_all['title_year'])
        # print ('\n---indices :', indices)
        idx = indices[title_year]
        # print ('\n---idx :', idx)
        sim_scores = list(enumerate(self.distance[idx]))
        # print ('\n---sim_scores :', sim_scores)
        sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
        sim_scores = sim_scores[1: top_k+1]
        movie_ind = [i[0] for i in sim_scores]
        # print('movie_ind :', movie_ind)
        return list(self.movies['title_year'].iloc[movie_ind])

