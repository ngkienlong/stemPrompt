import streamlit as st
import pandas as pd

#-------------------------------------------------------------------------------------------------------
# Các lời nhắc mặc định
#-------------------------------------------------------------------------------------------------------
sRole = 'Bạn hãy bỏ qua những đối thoại phía trước. Tôi muốn bạn đóng vai chuyên gia giáo dục STEM.'
sExample = 'Trả lời theo ví dụ mẫu'
sCreative = 'Hãy nghĩ sáng tạo khi trả lời. Không cần nhắc lại câu hỏi, chỉ cần ghi kết quả.'
sSituation = 'Bạn cần đưa ra bối cảnh thực tế hoặc giả định mà hoạt động giáo dục này diễn ra.'

#-------------------------------------------------------------------------------------------------------
# Các ví dụ mẫu
#-------------------------------------------------------------------------------------------------------
exTinkering = '''
            "Làm một khuôn đá: Học sinh có thể sử dụng một số nguyên vật liệu để tạo ra một khuôn đá. 
            Sau đó, học sinh có thể đổ nước vào khuôn và để nó trong tủ đông để làm đá. 
            Học sinh có thể quan sát và giải thích sự thay đổi nhiệt độ và quá trình chuyển đổi từ nước sang đá".
            '''
exActivity = '''
            "Hoạt động 'Khám phá cách hoạt động của động cơ': Mục đích của hoạt động này là để học sinh tự khám phá
            cách lắp mạch điện đơn giản gồm động cơ, pin, công tắc.
            Học sinh được cung cấp một động cơ mini, một pin và một công tắc. 
            Học sinh được yêu cầu tự khám phá cách nối mạch các linh kiện với nhau để làm cho động cơ quay.
            Sau đó, học sinh được yêu cầu khám phá cách đảo chiều quay của động cơ.
            Cuối cùng giáo viên sẽ đặt câu hỏi để học sinh trình bày lại những gì đã khám phá được."
            '''
exUnplugged = '''
            "Hoạt động 'Căn phòng bí mật': Mục đích của hoạt động này là để học sinh làm quen về số nhị phân. 
            Giáo viên đưa tình huống như sau: một điệp viên và người đưa tin
            hẹn gặp nhau bí mật tại một công viên rất rộng có 8 khu vui chơi được đánh số từ 0 đến 7, 
            họ không biết mặt nhau nhưng họ có quy ước sẽ báo hiệu cho nhau bằng 3 viên đá màu xám, trắng, vàng 
            đặt ở một nơi ít người để ý gần cổng khu vui chơi. 
            Người điệp viên sẽ là người quyết định để lại hoặc lấy đi 1 hoặc 1 số viên đá trên.
            Bằng cách đó người điệp viên báo hiệu cho đồng đội của mình số thứ tự của khu vui chơi mà họ sẽ gặp.
            Học sinh hãy đề xuất cách sử dụng 3 viên đá màu để báo hiệu về địa điểm hẹn gặp.
            '''
# exActivity = '''
#             "Hoạt động 'Kéo kéo': Học sinh sẽ được chia thành các nhóm và cùng nhau thực hiện một hoạt động đơn giản, 
#             kéo một đối tượng trên bàn bằng một sợi dây hoặc một miếng vải. 
#             Giáo viên sẽ hướng dẫn học sinh quan sát và giải thích lực kéo là gì,
#             cách đo lực kéo và cách tăng giảm lực kéo bằng cách điều chỉnh sức kéo của mỗi nhóm."
#             '''
#-------------------------------------------------------------------------------------------------------
# Chọn nhu cầu
#-------------------------------------------------------------------------------------------------------
needs = ['Tìm ý tưởng bài học Tinkering','Tìm ý tưởng hoạt động','Tìm ý tưởng bài học Unplugged coding']
need = st.sidebar.selectbox('Bạn đang cần:',needs, index = 1)


#-------------------------------------------------------------------------------------------------------
# Một số thông tin cơ bản
#-------------------------------------------------------------------------------------------------------
duration = st.text_input('Thời lượng (phút):')
grade = st.text_input('Lớp:')
#-------------------------------------------------------------------------------------------------------
# Biến lưu các tùy chọn nhắc prompt
#-------------------------------------------------------------------------------------------------------
example = ''
withSituation = ''
def get_withSituation():
    global withSituation
    if st.checkbox(sSituation):
        withSituation = sSituation
    else:
        withSituation = ''

#-------------------------------------------------------------------------------------------------------
# Lấy ví dụ mẫu mặc định
#-------------------------------------------------------------------------------------------------------
def get_example():
    global example
    global need
    if need == 'Tìm ý tưởng bài học Tinkering':
        example = exTinkering
    elif need == 'Tìm ý tưởng hoạt động':
        example = exActivity
    elif need == 'Unplugged coding':
        example = exUnplugged
    else:
        pass

#-------------------------------------------------------------------------------------------------------
# Cho phép người dùng tự nhập ví dụ
#-------------------------------------------------------------------------------------------------------
def give_example():
    global example
    have_example = st.checkbox('Trả lời theo ví dụ mẫu sau (nếu không thì dùng vd mẫu mặc định)')
    if have_example:
        example = st.text_area('')
    else:
        pass


#-------------------------------------------------------------------------------------------------------
# Tìm ý tưởng dự án tinkering đáp ứng yêu cầu cần đạt có trong CT 2018
#-------------------------------------------------------------------------------------------------------
def brainstorm_lesson():
    outcome = st.text_area('Mục tiêu bài học (qua bài học này học sinh có thể ...):')
    give_example()
    get_withSituation()
    prompt = f'''{sRole}\nGợi ý cho tôi 5 món đồ mà học sinh có thể chế tạo để qua đó học sinh có thể {outcome}. 
    \n{withSituation}
    \n{sExample} : {example}
    \nThời lượng bài học là {duration} phút, học sinh đang học lớp {grade}. 
    \n{sCreative}'''
    st.write('### Prompt của bạn là:')
    st.write(prompt)
#-------------------------------------------------------------------------------------------------------
# Tìm ý tưởng hoạt động Unplugged coding
#-------------------------------------------------------------------------------------------------------
def brainstorm_unplugged():
    outcome = st.text_area('Mục tiêu của hoạt động (qua hoạt động này học sinh ...):')
    give_example()
    get_withSituation()
    prompt = f'''{sRole}\nGợi ý cho tôi 3 hoạt động Unplugged coding thú vị để qua đó học sinh {outcome}. 
    \n{withSituation}
    \n{sExample} : {example}
    \nThời lượng bài học là {duration} phút, học sinh đang học lớp {grade}. 
    \n{sCreative}'''
    st.write('### Prompt của bạn là:')
    st.write(prompt)
#-------------------------------------------------------------------------------------------------------
# Tìm hoạt động giáo dục cho một mục tiêu cụ thể
#-------------------------------------------------------------------------------------------------------
def brainstorm_activity():
    outcome = st.text_area('Mục tiêu của hoạt động (qua hoạt động này học sinh ...):')
    give_example()
    get_withSituation()
    prompt = f'''{sRole}\nGợi ý cho tôi 3 hoạt động thú vị để qua đó học sinh {outcome}.
    \n{withSituation}
    \n{sExample} : {example}
    \nThời lượng của hoạt động là {duration} phút, học sinh đang học lớp {grade}.
    \n{sCreative}
    '''
    st.write('### Prompt của bạn là:')
    st.write(prompt)


#-------------------------------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------------------------------
get_example()
    
if need == 'Tìm ý tưởng bài học Tinkering':
    brainstorm_lesson()
elif need == 'Tìm ý tưởng hoạt động':
    brainstorm_activity()
elif need == 'Tìm ý tưởng bài học Unplugged coding':
    brainstorm_unplugged()
else:
    pass
