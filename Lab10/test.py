import json
import requests

import speech_recognition as sr 


word = input("Enter a word you like: ")
url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'


# Hàm trả về ý nghĩa và ví dụ với ý nghĩa đó của từ 
def meanings_and_examples():
    # Tạo một LIST để chứa các phần tử của response["meanings"] để dễ xử lí hơn 
    arr = []
    response = requests.get(url)
    response = response.json()
    response = response[0]
    data = response["meanings"]

    #  Trong response["meanings"] chứa nhiều nghĩa khác nhau nên cần phải tạo một LIST arr[] ở trên để lưu trữ và xử lí 
    for i in range(len(data)):
        arr.append(data[i]["definitions"])
        
    # Trong data[i]["definitions"] - là một DICTIONARY, có chứa những thành phần khác nhau và độ dài (len) của chúng cũng khác nhau 
    # Tìm độ dài (len) của các DICT trong LIST arr 
    arr_len = []
    for i in range(len(arr)):
        arr_len.append(len(arr[i]))

    # Chuyển các phần tử của LIST arr[] vào cùng một LIST mới là new_arr[]
    new_arr = []
    for i in range(len(arr)):   
        for j in range(max(arr_len)):
                
            # Dùng hàm try_except để kiểm tra các ngoại lệ << Cụ thể ở đây là trường hợp chỉ số : i < j >>
            try:
                # Hàm thêm các thành phần của LIST arr[] vào LIST mới new_arr[]
                new_arr.append(arr[i][j])
            # Tại vì các thành phần trong LIST arr[] có chiều dài (len) không giống nhau [[ Ví dụ như: i > j hoặc i < j ]]
            except IndexError:
                pass
    
    # Tạo một DICTIONARY mới để lưu trữ ["definitions"] và ["example"] của từ ['word]
    dictionary = {}
    
    for i in range(len(new_arr)):
        # print(f"Definition[{i+1}]: " + new_arr[i]["definition"])
        dictionary[f"Definition[{i+1}]: "] = new_arr[i]["definition"]
        
        # Hàm try_except vẫn có công dụng như thế dùng để kiểm tra những ngoại lệ mà chúng ta sẽ gặp phải khi viết code 
        # Cần phải đoán trước được mình sẽ gặp lỗi gì 
        try:
            # print(f"Example[{i+1}]: " + new_arr[i]["example"] + "\n")
            dictionary[f"Example[{i+1}]: "] = new_arr[i]["example"]

        except KeyError:
            # print(f"Example[{i+1}]: NO EXAMPLE !!! \n")
            dictionary[f"Example[{i+1}]: "] = "NO EXAMPLE !!! \n"
        
        with open("link.json", "w") as file:
            json.dump(dictionary, file)

    # Hàm trả về một DICTIONARY 
    # Trong đó có chứa: keys và values lần lượt là các definitions và examples của từ  
    return dictionary

# meanings_and_examples()

# Hàm lấy về URL hay còn gọi là link của từ mà bạn vừa nhập 
def get_links():
    response = requests.get()
    response = response.json()
    response = response[0]

    return  response["sourceUrls"][0]
 
# print(get_links())

# Hàm lưu những dữ liệu liên quan đến WORD mà ta vừa tìm được qua các hàm trên
# Như: ý nghĩa, ví dụ, link 
def save():
    
    # Mục đích là ta sẽ lưu dưới dạng file JSON 
    # Gọi hàm meanings_and_examples() để trả về ["definitions"] và ["examples"] mà ta đã tìm được bằng hàm đó
    dictionary = meanings_and_examples()
    
    # Tạo một DICTIONARY mới gồm có key: word và value: "word" - từ mà bạn nhập vào 
    word_dict = {"word: ": word}
    link_dict = {"link: ": get_links()}
    
    # Dùng hàm DICT.update() để thêm vào DICTIONARY 
    word_dict.update(dictionary)
    word_dict.update(link_dict)
    
    # Lưu DICTIONARY vào file JSON
    with open("results.json", "w") as file:
        json.dump(word_dict, file)
    file.close()
    
# save()

def main():
    # Khởi tạo recognizer (dùng để nhận dạng giọng nói)
    r = sr.Recognizer()

    # Sử dụng microphone đẻ lấy giọng nói từ bạn
    with sr.Microphone() as source:
        print("Say something...")
        audio = r.listen(source)

        text = ""
        
        # Dùng hàm try_except để xử lí các ngoại lệ trong quá trình chuyển đổi giọng nói thành văn bản 
        # Và nếu khi bạn không sử dùng lệnh này chương trình sẽ có thể dừng đột ngột và không kịp thu 
        # âm thanh khi bạn nói ra ==> BẮT BUỘC BẠN PHẢI DÙNG LỆNH NÀY NHÁ BẠN "TRẺ TROU 2K3 MIỀN NAM"
        try:
            # Chuyển đổi giọng nói thành văn bản 
            text += r.recognize_google(audio, language='en-US')
        except sr.UnknownValueError:
            print("Unable to recognize voice")
        except sr.RequestError as e:
            print("Error during offline speech recognition: {0}".format(e))

        # Sử dụng if - else để thực hiện các yêu cầu của đề bài 
        if text == "save":
            save()
        elif text == "meaning" or text == "example":
            dictionary = meanings_and_examples()
            for key, value in dictionary.items():
                print(key + ": " +  value)
        elif text == "link":
            print("Link: ", end="")
            print(get_links())
        else:
            print("Invalid request!!!")

# Hàm main()
main()