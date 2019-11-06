概要
----
Hypervolumeを計算するプログラム. 何も指定がない場合は, 最大化問題を仮定する. 
読み込んだ解集合に劣解が含まれていても, 参照点を強優越しない解が含まれていても, 重複解が含まれていても正しく動くように作っている. 


ファイル説明
-------------
args4j/  -- Javaのコマンド引数解析ライブラリ. Licensed under MIT by Kohsuke Kawaguchi and other contributors. http://args4j.kohsuke.org/
sampledata/ -- プログラム動作確認用のデータ. 
hv.bat -- Hypervolume計算プログラム, CUI向け.
hv-gui.bat -- Hypervolume計算プログラム, GUI向け.
indicator.jar -- Hypervolume計算プログラム本体.
readme.txt -- このファイル.
reference.csv -- hv-gui.batで参照点を指定するファイル.


使用方法
---------
GUI: 
ファイルをhv-gui.batにD&D. 参照点はreference.csvに指定する. 参照点の数は1つのみ. 
最小化, exact-calculationモードなどは, hv-gui.batを書き換えるなりして対応しろ. 

CUI: 
hv.batを実行. 引数なしで実行すると, パラメータの説明等が表示される.
ファイル名に+を指定すると, 標準入力からデータを読み込む. 独自フォーマットを使用したい場合は, これを利用して変換プログラムをかませるべし.


対応データフォーマット
-----------------------
* csvフォーマット
#で始まる行はコメント. 
解集合の区切りは, 1つ以上の空白行. 
ヘッダには対応していない. デリミタはタブのみ使用可能. 


* 独自フォーマット MTD (Markup Table Data)
拡張子は必ずmtd. 
##で始まる行はコメント. 
#で始まる行はMarkup部分. 

目的関数の値を書き始める前に以下の内容を記しておくこと (順不同). 
#nObjectives: [目的数]
#nTrials: [試行回数 (解集合の数)]
#isMaximize: [Boolean]
#nonDominated: [Boolean]
#nonOverlapping: [Boolean]

各解集合の前には, 解の数を
#nSols: [number]
の形式で書くこと. 解集合の区切りは1つ以上の空白行.

目的数以外は省略可能. isMaximize省略時はTrueを指定したものとみなされる. 
nonDominated, nonOverlappingの2つは省略時, Falseを指定したものとみなす. 
個体群サイズが非常に大きいときは, 劣解を取り除く処理に時間がかかる. 大きいデータを扱うときは予め劣解や重複解を取り除き, これらのフラグを立てておくと良い. 非劣解集合ではないのにnonDominatedがtrueである等, 嘘が含まれていた場合, 結果の正しさは保証されない. 

* 独自csvもどきフォーマット (sampledata/test.dat)
1行目: 目的数
2行目: 試行回数 (解集合の数)
以後, 
解の数
目的関数
...
の繰り返し.


オプションについて
-------------------
* verbose
Hypervolumeの平均と標準偏差をタブ区切りで出力する. 

* all
各解集合のHypervolumeを1行ごとに表示する.

* very-verbose
verboseの前に, 平均, 標準偏差, 空白行も表示する. 

* exact-calculation
目的関数が全て整数値を取る場合, 多倍長整数を用いてHypervolumeを厳密に計算する. 
(通常のモードでは, 64bit精度で, 有効数字15桁程度)
自動的にvery-verboseモードになる. 標準偏差の代わりに標本分散を表示する. 

* format (csv/mtd)
標準入力から読み込んだデータのフォーマットを指定する (csv or mtd). 
デフォルトはmtd. 

* sort
複数のファイルが引数に与えられた場合, ファイルをソートしてから結果を表示する. ファイル名に数字が含まれている場合は, 辞書順ではなく, 数値の大小も考慮して結果を表示する. 

例:
> hv.bat -r 0 kp10_hv10.mtd kp2_hv2.mtd kp5_hv5.mtd
10.0	2.0	5,0
> hv.bat -s -r 0 kp10_hv10.mtd kp2_hv2.mtd kp5_hv5.mtd
2.0	5,0	10.0


最小化問題について
-------------------
コマンドラインオプション
* minimize 最小化問題として扱う. 目的関数と参照点を-1倍する. 
* negate 最大化最小化関係なく, 目的関数と参照点を全て-1倍する. 

MTDでisMaximize = falseとしても, 目的関数と参照点が-1倍される. 

### 競合について
minimize, isMaximize = falseは最小化問題とみなす. 両方が指定されても-1倍は一度だけ. 
negateは, minimizeなどに関係なく-1倍する. minimizeやisMaximize = falseと同時に使用した場合, 最大化問題と同じになる. 

正しく計算される例:
hv.bat -r 15e3 mokp.csv
hv.bat -r 1.1 -n dtlz2.csv
hv.bat -r 1.1 -m dtlz2.csv
hv.bat -r 1.1 dtlz2.mtd			// isMaximize = falseが指定されている
hv.bat -r 1.1 -m dtlz2.mtd		// isMaximize = falseが指定されている


参照点について
---------------
コンマ区切りで指定する. 目的数に満たない場合は繰り返される.
...で終わる場合は, 等差・等比数列を使用する.  初項と第二項が与えられている場合は等差数列, 第三項も与えられている場合は
自動的に等差・等比数列か判断する. 

例 (4目的):
-r 0  ==> (0 0 0 0)
-r "0,1" == > (0 1 0 1)
-r "3,5,7" ==> (3 5 7 3)
-r "3,5,7,	 9" ==> (3 5 7 9)
-r 10 -m ==> (-10 -10 -10 -10)
-r 3,5,... ==> (3, 5, 7, 9)
-r 3,5,7,... ==> (3, 5, 7, 9)
-r "3,5,7,9,..." ==> (3, 5, 7, 9)
-r 10,100,... ==> (10, 100, 190, 280)
-r 10,100,1000,... ==> (10, 100, 1000, 10000)
