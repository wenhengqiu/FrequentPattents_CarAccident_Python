# <center><font size=6>台北車禍數據之Frequent Patterns</font>
## 1、項目介紹
## <left><font color=blue>項目介紹</font>: 從台北2015年車禍數據中，尋找frequent patterns，從而發現車禍多發的關聯因素，以制定相應措施，減少車禍發生的概率
### <left><font color=blue>數據說明</font>: 發生時間、地點、死傷人數、車種、性別、年齡、天候、速限、道路型態、事故位置。
### <left><font color=blue>資料來源</font>: [臺北市政府警察局交通警察大隊](http://data.taipei/opendata/datalist/datasetMeta?oid=2f238b4f-1b27-4085-93e9-d684ef0e2735)
### <left><font color=blue>數據大小</font>: 49519筆
 
## 2、演算法實現
### Relim Algorithm 簡單介紹（Recursive Elimination based on FP-Growth）

- 第一步：假設數據集為:abcd,初始化頻繁模式前綴，考慮a時，前綴就是a，若ab頻繁，則就是ab
- 第二步：加入未考慮的事務項，看和頻繁模式前綴的組合是否頻繁，若是轉第三步，不是則繼續考慮下一個事務項，當全部事務項考慮完畢，則算法結束。
- 第三步：講第二步購成頻繁的模式輸出，並以此模式作為頻繁模式前綴，轉到第一步繼續考察。

## 3、檔案介紹
- AR_1000.txt: Association Rules前1000的Rules
- data_raw.csv: 原始數據，可以從[臺北市政府警察局交通警察大隊]下載
- FP_1000.txt: Freqeunt Patterns前1000的Patterns
- Group9_DM_hw2.pdf: 相關的報告
- hw2.py: 實現源碼
