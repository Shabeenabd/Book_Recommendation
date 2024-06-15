import streamlit as st
import pickle
import numpy as np

book_data=pickle.load(open('artifacts/book_data.pkl','rb'))
similarity_data=pickle.load(open('artifacts/similarity_data.pkl','rb'))


def get_book_details(book):
    book_details=np.array(book_data[book_data['Book-Title']==book])[0]
    return book_details


def recommend_book(book):
    index = np.where(similarity_data.index==book)[0][0]
    similar_items = sorted(list(enumerate(similarity_data.iloc[index])),key=lambda x:x[1],reverse=True)[1:11]
    similar_books=[]
    for i in similar_items:
        similar_books.append(similarity_data.index[i[0]])
    return similar_books




st.set_page_config(layout="wide")
_,c,_=st.columns([1,5,1])
with c:
    st.title('Book Recommendation System',anchor=False)    
st.title('') 
_,center,_=st.columns([1,5,1])
with center:
  selected_book=center.selectbox('',book_data['Book-Title'],index=None,placeholder="select a book",key='booked')
  st.title('')
  if selected_book:
    temp=get_book_details(selected_book)
    _,img,details,_=st.columns([.5,4,3  ,.5])
    with img:
            st.title(temp[0])
            st.title('')
            st.image(temp[4],width=300)
            
    with details:
            for i in range(5):
                    st.title('')
            st.markdown(f'<b style="font-size:20px;">Author &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{str(temp[1])}</b>', unsafe_allow_html=True)
            st.markdown(f'<b style="font-size:20px;">Year &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{str(temp[2])}</b>', unsafe_allow_html=True)
            st.markdown(f'<b style="font-size:20px;">Publisher&nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{temp[3]}</b>', unsafe_allow_html=True)
            st.markdown(f'<b style="font-size:20px;"> Rating &nbsp;&nbsp;:&nbsp;&nbsp; &nbsp;&nbsp;</b><b style="font-size:30px;">{np.round(temp[5],1)}</b>', unsafe_allow_html=True)


    st.title('')
    st.title('')
    _,ctntn,_=st.columns(3)
    with ctntn:
        recom_butt=st.button('show recommendation',type="primary")
    st.title('')
    if recom_butt:
        similar_books=recommend_book(selected_book)
        cols1=st.columns(5)
        for i,j in enumerate(cols1):
             with j:
                temp=get_book_details(similar_books[i])
                st.image(temp[4])
                st.write(similar_books[i    ])
                
        st.header('')
        cols2=st.columns(5)
        for i,j in enumerate(cols2):
             with j:
                temp=get_book_details(similar_books[i+5])
                st.image(temp[4])
                st.write(similar_books[i+5])
                
                    

            


