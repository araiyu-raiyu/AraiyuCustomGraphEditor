# AraiyuCustomGraphEditor

![customgrapheditor](https://user-images.githubusercontent.com/43115049/150816940-23c382bc-7a6c-4f20-a343-2f80eaacf7c6.JPG)
 
 
MAYAで使えるカスタムグラフエディターです。  
商用利用可、改変可など自由ですが、それによって発生した不具合は自己責任でお願いします。  
MAYA2020まで使用することができます。 

## 実行方法
1.AraiyuCustomGraphEditor.pyを C:\Users\ユーザー名\Documents\maya\scripts に落としてください  
2.MAYAで下記スクリプトをPythonで実行してください。  
```
import AraiyuCustomGraphEditor;reload(AraiyuCustomGraphEditor)
```

## 使い方
![showhidecurveeditor](https://user-images.githubusercontent.com/43115049/150819229-d182e92d-030a-479c-8be6-4aebea14e62a.JPG)  
アニメーションカーブの表示のON/OFFを切り替えます。  
グラフエディターのメニューバーにあるShow/Select Attributes... と全く同じ機能です。  

<br>

![Tool](https://user-images.githubusercontent.com/43115049/150819973-69f8c519-1b17-42cd-9144-c6f38ca952e4.JPG)  
個人的に使用頻度高めなツールが入っています。  
__Euler Filter__  
オイラーフィルターです。  
__Smooth Curve__  
アニメーションカーブをなだらかします。  
__Reverse Curve__  
アニメーションカーブを反転します。  
チェックが入っていると選択しているキーの真ん中あたりを軸に反転させます。  
チェックが無い状態だと０を中心に反転させます。  
__Snap Key__  
小数点フレームにあるキー整数フレームに変換してくれます。  
アニメーションカーブを選択した状態で実行してください。  

<br>

![keyloop](https://user-images.githubusercontent.com/43115049/150819986-a8bb2b55-6a98-497d-9fd5-cb3c8af85af4.JPG)  
タイムスライダ上にある最初のフレームと最後のフレームを一致させます。  
Start > End にチェックが入っていると、最初にあるフレームを最後のフレームに合わせます。End > Start にチェックが入っていると最後のフレームを最初に合わせます。  
Tangent、Positionにチェックが入っているものをコピペします。基本的には触る必要はありません。  
Set Timeにチェックを入れるとコピペをするフレームを任意で決めることができます。  

<br>

![movekey](https://user-images.githubusercontent.com/43115049/150820002-fed5ac3d-3df9-4a4b-8eca-e547a1740b7e.JPG)  
数値を入力した分だけキーを移動させます。  

<br>

![etctool](https://user-images.githubusercontent.com/43115049/150820011-7bdaf432-756d-4ab2-a29b-8ac88b758ca0.JPG)  
枠が余ったために作ったツール群です。使用頻度は高くない。  
__Delete Float Num Key__  
小数点フレームを削除してくれます。  
__Copy Key Cycle__  
アニメーションカーブを1ループ分だけコピペします。  
__Delete Flat AnimCurve__  
たいらなアニメーションカーブを削除します。
