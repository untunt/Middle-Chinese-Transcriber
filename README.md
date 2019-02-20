# unt’s Middle Chinese Phonology Transcriber

unt 的中古音韵转写器

# Format Codes

|Code|Explanation|Impl. Date|
|-|-|-|
|`trad`|Names of initials, finals and tones in traditional phonology<br>传统音韵学中的声母、韵母和声调名|I: 2018.3.20<br>Fo: 2018.3.31<br>Fi: 2018.4.20|
|`bax`|Baxter's transcription for MC (2014 version)<br>白一平的中古汉语转写（2014 版）<br>Ref.: William H. Baxter & Laurent Sagart, *Old Chinese: A New Reconstruction*|IFo: 2019.2.12|
|`bax1`|[Baxter's transcription for MC (1992 version)](https://en.wikipedia.org/wiki/Baxter%27s_transcription_for_Middle_Chinese "Baxter's transcription for Middle Chinese")<br>白一平的中古汉语转写（1992 版）<br>Ref.: William H. Baxter, *A Handbook of Old Chinese Phonology*|IFo: 2019.2.12|
|`poly`|[Polyhedron's romanization of MC](https://zh.wikipedia.org/wiki/User:Polyhedron/%E4%B8%AD%E5%8F%A4%E6%BC%A2%E8%AA%9E%E6%8B%BC%E9%9F%B3 "中古汉语拼音")<br>Polyhedron 的中古汉语拼音|I: 2018.3.20<br>Fo: 2018.4.29|
|`hxs`|Xiaoshan Huang's reconstruction of EMC<br>黄笑山的早期中古汉语构拟<br>Ref.: 黄笑山《〈切韻〉和中唐五代音位系統》|F: Unfinished|
|`msoeg`|[msoeg's reconstruction of MC](https://zhuanlan.zhihu.com/p/23576833 "【汉语音韵学笔记】中古汉语")<br>msoeg 的中古汉语构拟|F: Unfinished|
|`unt`|unt's reading pronunciation of *Qieyun* (2019 version)<br>unt 切韵朗读音（2019 版）|IFo: 2019.2.14|
|`untF`|unt's reconstruction of MC (2016 version)<br>unt 的中古汉语构拟（2016 版）|I: 2018.3.31|
|`yugan`|unt's General Romanization (private use)<br>unt 的通用拼音（私用）|I: 2018.3.31|
|`yugun`|unt's General Romanization, without combining diacritics<br>unt 的通用拼音，不使用组合符号|I: 2018.3.31|

Letters in column *Impl. Date* (Implementation Date):

- *I* for initials, *F* for finals.
- *i* for input (recognition) and *o* for output (generation). Omitted for input & output.

MC: Middle Chinese

EMC: Early Middle Chinese

# CSV Structure

Additional fields (columns)

## Additional Fields of `list_finals.csv`

- `_no`: Rhyme number in *Guangyun* (广韵). However, numbering belonging to each volume of 2 volumes of tone 1 (平声) is not distinguished.
- `_class`: Rhyme class (摄) in rime table.
- `_rhyme`: Rhyme name (韵目) in *Guangyun*.
- `_div`: Division (等) of the final. Values: 一, 二, 三, 三A, 三B, and 四 (I, II, III, III type A, III type IV, and IV).
- `_round`: Rounding (呼) of the final. Values: 开 and 合 (open and close).
- `_multi`: Field(s) in which finals are divided in the same rhyme when this rhyme contains multiple finals. Values (flags): `d`, `c`, and `r`, standing for fields of division, *Chóngniǔ* (重纽, repeated initial), and rounding. Flags can appear at the same time.
- `_var`: Possible variant characters (异体字) of the rhyme name. Appears only in the first row of each rhyme.
