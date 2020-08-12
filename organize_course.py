import pandas as pd


def organize_course(input_file_name):

    df = pd.read_csv(input_file_name)

    df = df.drop(columns=['開班／選課人數', '教室【校區】', '選別', '學期數'])    # 刪除不必要資料

    # 更改列名稱
    df = df.rename(columns={'科目': '科目名稱'})
    df = df.rename(columns={'上課日期／節次': '正課時間'})
    df = df.rename(columns={'任課教師': '正課教師'})

    def insert_colums(index, colums_name, df):
        col_name = df.columns.tolist()                            # 將數據框的列名全部提取出來存放在列表裏
        # 在列索引為index的位置插入
        col_name.insert(index, colums_name)
        # DataFrame.reindex() 對原行/列索引重新構建索引值
        df = df.reindex(columns=col_name)
        return df

    df = insert_colums(1, '科目代碼', df)
    df = insert_colums(6, '實習課時間', df)
    df = insert_colums(6, '實習課教師', df)
    df['科目代碼'], df['科目名稱'] = df['科目名稱'].str.split(' ', 1).str           # 分離科目代碼與科目名稱
    df['正課時間'], df['實習課時間'] = df['正課時間'].str.split('節', 1).str        # 分離課程時間
    try:
        df['正課教師'], df['實習課教師'] = df['正課教師'].str.split('實', 1).str
    except ValueError:
        print('')

    def course_schedule(course):                            # 處理課程時間
        for i in range(len(df.index)):
            str = df[course][i]
            str = str.replace('星期', '')                      # 刪除字串中多餘文字
            str = str.replace('節', '')
            str = str.replace(' ', '')
            str = str.replace(':', '')
            str = str.replace(chr(160), '')  # 刪除特殊空白

            str_len = len(str)

            if str_len == 0:
                str = '00000'
            elif str_len > 5:
                str = str[0:3]+str[str_len-2:str_len]
            elif str_len < 5:
                str += str[1:3]

            df.loc[i, course] = str

    course_schedule('正課時間')
    course_schedule('實習課時間')

    def teacher_name(name):
        for i in range(len(df.index)):
            str = df[name][i]
            if str == str:                                                # 如果無教師則不執行
                str = str.replace('\r\n\t\t\t\t', '')
                str = str.replace(' ', '')
                str = str.replace('正課:', ' ')
                str = str.replace('習:', '')
                # 刪除特殊字元
                str = str.replace(chr(13), '')
                str = str.replace(chr(10), '')
                str = str.replace(chr(9), '')
                str = str[1:len(str)]
            df.loc[i, name] = str

    teacher_name('正課教師')
    teacher_name('實習課教師')
    df.to_csv(input_file_name, index=False, header=False)
