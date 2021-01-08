result_for_hvの仕様について

result_for_hvでは，変数"target_dir"に格納した名前のディレクトリについて，含まれる各datファイルを個体としてHVを計算します．
HVの計算は"hv.bat"を使用しています．
個体ファイルの形式は
・拡張子は.dat
・delimiterは" "(半角スペース)
・最小化問題を仮定
となっています．

HV計算用のファイル"result.obj"および"hv.csv"が出力されます．
"hv.csv"は("target_dir"内の.datファイル数, 1)の形式で出力されます．

その他の設定で"hv.bat"を動かしたい場合は，適当に変更してください．