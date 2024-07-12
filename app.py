import streamlit as st
import pickle
import numpy as np
import time

book_data=pickle.load(open('artifacts/book_data.pkl','rb'))
similarity_data=pickle.load(open('artifacts/similarity_data.pkl','rb'))
popular_books=pickle.load(open('artifacts/top_50_books.pkl','rb'))

def get_book_details(book):
    book_details=np.array(book_data[book_data['Book-Title']==book])[0]
    return book_details


def recommend_book(book):
    similar_items = sorted(list(enumerate(similarity_data.loc[book])),key=lambda x:x[1],reverse=True)[1:11]
    similar_books=[]
    for i in similar_items:
        similar_books.append(similarity_data.index[i[0]])
    return similar_books

def update_recom():
    if st.session_state.recom==0:
          st.session_state.recom=1
    else:
         st.session_state.recom=0

def render(selected_book):
        temp=get_book_details(selected_book)
        with st.container(border=True,):
            _,img,details=st.columns([1,4,4])
            with img:
                st.title(temp[0])
                st.image(temp[4],width=250)
                st.title('')
            with details:
                for i in range(2):
                        st.title('')
                st.markdown(f'<b style="font-size:20px;">Author &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{str(temp[1])}</b>', unsafe_allow_html=True)
                st.markdown(f'<b style="font-size:20px;">Year &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{str(temp[2])}</b>', unsafe_allow_html=True)
                st.markdown(f'<b style="font-size:20px;">Publisher&nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{temp[3]}</b>', unsafe_allow_html=True)
                st.markdown(f'<b style="font-size:20px;"> Rating &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{np.round(temp[5],1)}</b>', unsafe_allow_html=True)

        st.title('')
        _,ctntn,_=st.columns([1,.7,1])
        with ctntn:
            if st.session_state.recom==0:
                recom_butt=st.button('show recommendation',type="primary",use_container_width=True,on_click=update_recom)
            else:
                 recom_butt=st.button('hide recommendation',type="primary",use_container_width=True,on_click=update_recom)
            st.title('')
        if st.session_state.recom==1:
                get_recommendation(selected_book)
        


def update_session(new_book,reset=None):
    st.session_state.book=new_book
    if reset:
          st.session_state.level=0
          st.session_state['booked']=None
    else:
         st.session_state.level=1
         st.session_state.recom=0


def get_recommendation(selected_book):
        similar_books=recommend_book(selected_book)
        cols1=st.columns(5,gap='medium')
        for i,j in enumerate(cols1):
             with j:
                with st.container(border=True,height=450):
                        temp=get_book_details(similar_books[i])
                        st.image(temp[4],use_column_width=True)
                        st.button('view',key=i,on_click=update_session,args=(similar_books[i],))
                        st.write(similar_books[i])
                    
        st.header('')
        cols2=st.columns(5)
        for i,j in enumerate(cols2):
             with j:
                with st.container(border=True,height=480):
                    temp=get_book_details(similar_books[i+5])
                    st.image(temp[4],use_column_width=True)
                    st.button('view',key=i+5,on_click=update_session,args=(similar_books[i+5],))
                    st.write(similar_books[i+5])
                    
                    
                



st.set_page_config(layout="wide")
if 'book' and 'level' and 'recom' not in st.session_state:
     st.session_state.book=0
     st.session_state.level=0
     st.session_state.recom=0

explore,trending=st.tabs(['Explore','Trending'])
with explore:
    _,center,_=st.columns([1,15,1])
    with center:
        title,home=st.columns([8,2])
        with home:
            st.title('')   
            st.button('home',on_click=update_session,args=(0,1))
        with title:
            st.title('Book Recommendation System',anchor=False)    
        if st.session_state.level==0:
            selected=center.selectbox('book',book_data['Book-Title'],index=None,placeholder="select a book",label_visibility='hidden',key='booked')
            st.write('')
            if selected :
                st.session_state.book=selected

        if st.session_state.book!=0:
            render(st.session_state.book)
                    

with trending:
    st.title('Popular Books',anchor=False)    

    cols=st.columns(5,gap='large')
    for r in range(10):
        for i,j in enumerate(cols):
            with j:
                st.write(' ')
                with st.container(border=True,height=460):  
                    # _,c,_=st.columns([1,8,1])
                    # with c:
                        temp=get_book_details(popular_books[i+(r*5),0])
                        st.write('Rating  : ',np.round(popular_books[i+(r*5),1],2))
                        st.image(temp[4],use_column_width=True,)
                        st.write(popular_books[i,0])
            
    
