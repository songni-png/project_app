import streamlit as st

# # -> jupyter / ''' -> literal
# 텍스트
st.header('🖥️ 텍스트 출력')
st.write('') # 빈 줄 삽입

st.write('# 마크다운 H1 : st.write()')
st.write('### 마크다운 H3 : st.write()')
st.write('')

st.title('제목 : st.title()')
st.header('헤더 : st.header()')
st.subheader('서브헤더 : st.subheader()')
st.text('본문 텍스트 : st.text()')
st.write('')

st.markdown('## 마크다운 : st.markdown()')
st.markdown('''
            1. ordered item
                - unordered item
                - unordered item
            2. ordered item
            3. ordered item
            ''')
st.divider() # 구분선

# 마크다운
'''# 👑 Magic에 마크다운을 조합
 1. ordered item
     - 강조 : **unordered item**
     - 기울임: **unordered item**
2. ordered item
3. ordered item
'''

# 데이터프레임
import pandas as pd
df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
df # 데이터프레임 출력

# 차트
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,10,100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x,y)
fig # 차트 출력

# 사이드바
st.header('---- 사이드바')
st.sidebar.write('## 사이드바 텍스트')
st.sidebar.checkbox('체크박스 1')
st.sidebar.checkbox('체크박스 2')
st.sidebar.radio('라디오 버튼', ['radio 1', 'radio 2', 'radio 3'])
st.sidebar.selectbox('셀렉트박스', ['select 1', 'select 2', 'select 3'])

# 레이아웃: 컬럼
st.header('🤖 컬럼 레이아웃')
col_1, col_2, col_3 = st.columns([1,2,1]) # 컬럼 인스턴스 생성. 1:2:1 비율로 컬럼을 나눔

with col_1:
    st.write('## 1번 컬럼')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 1')
    st.checkbox('이것은 1번 컬럼에 속한 체크박스 2')

with col_2:
    st.write('## 2번 컬럼')
    st.radio('2번 컬럼의 라디오 버튼', ['radio 1', 'radio 2', 'radio 3'])  # 동일한 라디오 버튼을 생성할 수 없음
    # 사이드바에 이미 라디오 버튼이 생성되어 있기 때문에, 여기서는 라디오 버튼의 내용을 변경해야 오류가 발생하지 않음

col_3.write('## 3번 컬럼')
col_3.selectbox('3번 컬럼의 셀렉트박스', ['select 1', 'select 2', 'select 3'])
# 사이드바에 이미 셀렉트박스가 생성되어 있기 때문에, 여기서는 셀렉트박스의 내용을 변경해야 오류가 발생하지 않음

# 레이아웃: 탭
st.header('🤖 탭 레이아웃')
tab_1, tab_2, tab_3 = st.tabs(['탭AAAAA', '탭BBBBB', '탭CCCCC'])  # 탭 인스턴스 생성. 3개의 탭을 생성

with tab_1:
    st.write('## 탭AAAAA')
    st.write('이것은 탭A의 내용입니다.')

with tab_2:
    st.write('## 탭BBBBB')
    st.write('이것은 탭B의 내용입니다.')

tab_3.write('## 탭CCCCC')
tab_3.write('이것은 탭C의 내용입니다.')

# 사용자 입력
st.header('🤖 :blue[사용자 입력]')

# 텍스트 입력은 입력된 값을 반환
st.write('#### : orange[텍스트 입력]')
text = st.text_input('여기에 텍스트를 입력하세요') 
st.write(f'입력된 텍스트: {text}')

# 숫자 입력은 입력된 값을 반환
st.write('#### :orange[숫자 입력]')
number = st.number_input('여기에 숫자를 입력하세요')
st.write(f'입력된 숫자: {number}')

# 날짜

# 시간

# 파일 업로드는 업로드된 파일을 반환




check = st.checkbox('여기를 체크하세요') # 체크박스는 True/False 값을 반환
if check:
    st.write('체크되었습니다.')

radio = st.radio('여기에서 선택하세요', ['선택 1', '선택 2', '선택 3']) # 라디오 버튼은 선택된 값을 반환
st.write(radio+'가 선택되었습니다.')

select = st.selectbox('여기에서 선택하세요', ['선택 1', '선택 2', '선택 3']) # 셀렉트박스는 선택된 값을 반환
st.write(select+'가 선택되었습니다.')

slider = st.slider('여기에서 값을 선택하세요', 0, 100, 50) # 슬라이더는 선택된 값을 반환
st.write(f'현재의 값은 {slider} 입니다.')

multi = st.multiselect('여기에서 여러 값을 선택하세요', ['선택 1', '선택 2', '선택 3']) # 멀티셀렉트박스는 선택된 값을 리스트로 반환
st.write(f'{type(multi) = }, {multi}가 선택되었습니다.')

button = st.button('여기를 클릭하세요') # 버튼은 클릭 여부를 반환
if button:
    st.write('버튼이 클릭되었습니다.(일반 텍스트: st.write()')
    st.success('버튼이 클릭되었습니다.(메시지: st.success())')  # 성공 메시지 출력
    st.balloons() # 풍선 애니메이션 출력

# 캐싱
st.header('🤖 캐싱 적용')

import time

@st.cache_data
def long_running_function(param1):
    time.sleep(5)
    return param1*param1

start = time.time()
num_1 = st.number_input('입력한 숫자의 제곱을 계산합니다.') # 숫자 입력은 입력된 값을 반환
st.write(f'{num_1}의 제곱은 {long_running_function(num_1)} 입니다. 계산시간은 {time.time()-start:.2f}초 소요')


# 세션 상태
st.header('🤖 세션 상태')

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("session_state를 사용하지 않은 경우")
color1 = st.color_picker("Color1", "#FF0000")
st.divider() # 구분선
st.scatter_chart(df, x="x", y="y", color=color1)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(np.random.randn(20, 2), columns=["x", "y"])

st.header("session_state를 사용한 경우")
color2 = st.color_picker("Color2", "#FF0000")
st.divider() # 구분선
st.scatter_chart(st.session_state.df, x="x", y="y", color=color2)