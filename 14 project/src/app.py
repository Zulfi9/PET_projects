import os

import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.echo_expander import echo_expander
from dotenv import load_dotenv

from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)


recsys = ContentBaseRecSys(
    movies_dataset_filepath = MOVIES,
    distance_filepath = DISTANCE,
)

# ver = st.sidebar.radio ("Select version", ('ver.1', 'ver. 2'))
# with st.sidebar:
#     add_vertical_space(10)
# st.sidebar.write(
#     """manhackc@student.21-school.ru
#     21 TGU_DS_103
#     Tribe: Uranus
#     19.04.2023 - 08.08.2023
#     """
# )

st.markdown(
    "<h1 style='text-align: center; '>СЕРВИС РЕКОМЕНДАЦИИ ФИЛЬМОВ</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center; '>Поиск осуществляется на основе схожести с выбранным Вами фильмом</h3>",
    unsafe_allow_html=True
)

selected_movie = None

selected_movie = selectbox(
    "Выбери или начни печатать название понравившегося фильма :",
    recsys.get_titles(),
    no_selection_label ='---'
)

if selected_movie:
    col1, col2 = st.columns([1, 4])
    film_id = recsys.get_film_id(selected_movie)
    with col2:
        st.markdown("**Выбранный фильм** : " +
                    selected_movie + "<br>" +
                    "**Режиссер** : " +
                    recsys.get_film_director(film_id) + "<br>" +
                    "**Жанр** : " + ", ".join(recsys.get_film_genres(film_id)) + "<br>" +
                    "**Описание** : " + recsys.get_film_overview(film_id),
                    unsafe_allow_html=True)
        
    with col1:
        st.image(omdbapi.get_posters([recsys.get_film_original_title(film_id)]),
                 use_column_width=True)
        
st.markdown("""По умолчанию поиск выполняется по всем записям.
            Для сужения поиска Вы можете выбрать <strong>год</strong> или
            <strong>жанр</strong> искомого фильма.
            Например, если Вы выберете жанр "fantasy", поиск будет производиться только по фильмам, где жанр "fantasy", даже если исходный фильм был другого жанра.""", unsafe_allow_html=True)

filter_col = st.columns([3, 3])
with filter_col[0]:
    selected_genre = selectbox(
        "Выбери или начни печатать название жанра понравившегося фильма : ",
        recsys.get_genres(),
        no_selection_label='Все жанры'
    )

with filter_col[1]:
    selected_year = selectbox(
        "Выбери или начни печатать год выпуска понравившегося фильма : ",
        recsys.get_years(),
        no_selection_label='Все года'
    )

if selected_year or selected_genre:
    recsys.set_filter(selected_year, selected_genre)
else:
    recsys.remove_filter()

st.markdown("""Если Вы выбрали интересующие параметры, нажмите на кнопку и Вы увидите, какие фильмы мы рекомендуем Вам посмотреть""",
            unsafe_allow_html=True)

st.divider()

btn_pressed = st.button('Показать рекомендации')

# print(btn)

if btn_pressed:
    if selected_movie:
        recommended_movie_names = recsys.recommendation(
            selected_movie, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.write("""Нет рекомендаций по заданным параметрам. Для поиска рекомендованных фильмов, пожалуйста, повторите поиск, изменив выбранные параметры.""")
        else:
            st.subheader("Рекомендуем посмотреть:")
            title = [recsys.get_film_original_title(
                recsys.get_film_id(name)
            ) for name in recommended_movie_names]
            recommended_movie_posters = omdbapi.get_posters(title)
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.image(
                        recommended_movie_posters[index],
                        use_column_width=True)
            movies_col = st.columns(len(recommended_movie_names))
            for index, col in enumerate(movies_col):
                with col:
                    st.markdown("<h3 style='text-align: center;'>" + 
                                recommended_movie_names[index]+"</h3>",
                                unsafe_allow_html=True)
                    rec_id = recsys.get_film_id(
                        recommended_movie_names[index])
                    
                    # st.markdown(
                    #     "<p style='text-align: center;'><strong>" +
                    #     "Year of prodaction:</strong><br>" +
                    #     recsys.get_years(rec_id)+"<br>" + 
                    #     "<strong>Director</strong> : <br>" +
                    #     recsys.get_film_director(film_id) + "<br>" +
                    #      "<strong>Genre:</strong><br>" +
                    #      ", ".join(
                    #          recsys.get_film_genres(rec_id))+"</p>",
                    #          unsafe_allow_html=True)
                    # st.markdown(
                    #     "<p style='text-align: center; '><strong>Similarite:<br>" +
                    #     recsys.get_similarity(recsys.get_film_id(selected_movie), rec_id) + "%</strong></p>",
                    #     unsafe_allow_html=True
                    # )
    else:
                    st.write('Сперва нужно выбрать фильм...')
 
                
                    


# if st.button('Show Recommendation'):
#     st.write("Recommended Movies:")
#     recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
#     # recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
#     movies_col = st.columns(TOP_K)
#     for index, col in enumerate(movies_col):
#         with col:
#             st.subheader(recommended_movie_names[index])
#             # st.image(recommended_movie_posters[index])
