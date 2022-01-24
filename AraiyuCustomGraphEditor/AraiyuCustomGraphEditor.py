# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

# Copyright (c) 2022 Araiyu
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php


if cmds.window('AraiyCustomGraphEditor' , exists=True):#同じウィンドウがあれば削除して再生性
    cmds.deleteUI('AraiyCustomGraphEditor' , window = True)

invis_panel = cmds.getPanel(invisiblePanels=True)#表示していないパネルを取得
graphpanels = cmds.getPanel(scriptType='graphEditor')#グラフエディタのパネルを取得
graphpanels.remove('graphEditor1')


for o_graphp in graphpanels:
    if o_graphp in invis_panel:
        cmds.deleteUI(o_graphp,panel=True)

grp_panel_no_a = str( len(cmds.getPanel( scriptType='graphEditor' )) + 1 )
outline_ed_name = "graphEditor" + grp_panel_no_a + 'OutlineEd'
mel.eval('string $outlineed_name = "%s"' % outline_ed_name)
getGraphEditors = pm.getPanel(scriptType="graphEditor")
graph_ed_name = "graphEditor" + grp_panel_no_a + 'GraphEd'


def visAnimCurveCommand(attrname, status):
    mel.eval("filterUISelectAttributesCheckbox " + attrname  + str(status) + " " + "$outlineed_name" + ";")
    mel.eval("filterUISelectAttributesCheckbox " + attrname  + str(status) + " " + "$outlineed_name" + ";")
    mel.eval("filterUISelectAttributesCheckbox " + attrname  + str(status) + " " + "$outlineed_name" + ";")



#アニメーションレイヤーの表示切替
def nonActiveAnimLayerHide():
    cmds.outlinerEditor(outline_ed_name, e=1, animLayerFilterOptions="selected")
def nonActiveAnimLayerShow():
    cmds.outlinerEditor(outline_ed_name, e=1, animLayerFilterOptions="allAffecting")


#infinityの表示切替
def switchVisInfinities():
    grp_panel_no_b = str( len(cmds.getPanel( scriptType='graphEditor' )) )
    graph_ed_name = "graphEditor" + grp_panel_no_b + 'GraphEd'
    mel.eval('string $o_graph_ed_name = "%s"' % graph_ed_name)
    infinityCheckBoxStatus = cmds.checkBox('InfinityCheckBox', q=True, v=True)


    if infinityCheckBoxStatus == 1:
        mel.eval('animCurveEditor -edit -displayInfinities true $o_graph_ed_name;')
    else:
        mel.eval('animCurveEditor -edit -displayInfinities false $o_graph_ed_name;')



def preInfinity(whatpreinfinity):
    #sellists = cmds.ls(sl=True)
    if whatpreinfinity == "cycle":
        cmds.setInfinity( pri="cycle")
    if whatpreinfinity == "offset":
        cmds.setInfinity( pri="offset")
    if whatpreinfinity == "linear":
        cmds.setInfinity( pri="linear")
    if whatpreinfinity == "constant":
        cmds.setInfinity( pri="constant")


def postIninity(whatpostinfinity):
    if whatpostinfinity == "cycle":
        cmds.setInfinity( poi="cycle")
    if whatpostinfinity == "offset":
        cmds.setInfinity( poi="offset")
    if whatpostinfinity == "linear":
        cmds.setInfinity( poi="linear")
    if whatpostinfinity == "constant":
        cmds.setInfinity( poi="constant")



#スナップ
def snapAnimCurve():
    selectAnimCurves = cmds.keyframe(q=True, name=True, n=True) #選択しているアニメーションカーブのリスト
    keyFrameNumList = []


    for selectAnimCurve in selectAnimCurves:
        keyFrameNumList = cmds.keyframe(selectAnimCurve, q=True, sl=True)#選択しているキーのリスト


        if len(keyFrameNumList):
            for keyFrameNum in keyFrameNumList:
                cmds.setKeyframe(insert=True, t=[int(keyFrameNum)], at=selectAnimCurve) #小数点フレームを整数に変換してキーを打つ


                if keyFrameNum %1 != 0: #最後の小数点フレームにキーを打つ。但し最後が整数フレームの場合は打たない
                    cmds.setKeyframe(selectAnimCurve, insert=True, t=[int(keyFrameNum+1)])


                floatKeyframe = keyFrameNum % 1
                if floatKeyframe != 0: #キーを１で割って余りが０以外ならキーを削除。
                    cmds.cutKey(selectAnimCurve, cl=True, time=(keyFrameNum, keyFrameNum))#少数化フレームを削除



#カーブの反転
def reverseAnimCurve():

    if cmds.checkBox("reverseCurveCheckBox", q=True, value=True) == 1:
        keyFrameTimeLang = cmds.keyframe(q=True) #選択したキーフレームのタイムレンジを取得

        selectionAnimCurves = cmds.keyframe(q=True, name=True) #選択しているアニメーションカーブのリスト
        keyFrameValueListInRevese = []
        
        for selectAnimCurve in selectionAnimCurves:
            keyFrameValueListInRevese = cmds.keyframe(selectAnimCurve, q=True, sl=True, vc=True)#選択したキーの値のリスト
            KeyFrameMaxValue = max(keyFrameValueListInRevese)
            KeyFrameMinValue = min(keyFrameValueListInRevese)
            KeyFrameAverageValue = (KeyFrameMaxValue + KeyFrameMinValue) /2
            cmds.scaleKey(selectAnimCurve, valuePivot=KeyFrameAverageValue, valueScale=-1, t=(keyFrameTimeLang[0], keyFrameTimeLang[-1]))

    if cmds.checkBox("reverseCurveCheckBox", q=True, value=True) == 0:
        keyFrameTimeLang = cmds.keyframe(q=True) #選択したキーフレームのタイムレンジを取得

        selectionAnimCurves = cmds.keyframe(q=True, name=True) #選択しているアニメーションカーブのリスト
        
        for selectAnimCurve in selectionAnimCurves:
            cmds.scaleKey(selectAnimCurve, valuePivot=0, valueScale=-1, t=(keyFrameTimeLang[0], keyFrameTimeLang[-1]))



#小数点フレームを削除
def deleteFloatFrame():
    cmds.selectKey(unsnappedKeys=1)
    cmds.cutKey(animation="keys", clear=1)



#ループの最初と最後のキーを合わせる
def animCurveKeyCycle():


    if cmds.checkBox("SetAnimCycleTime", q=True, value=True) == 0:


        #チェックボックスの状態を取得
        checkTangent = cmds.checkBox("checkTan", q=True, v=True)
        checkPosition = cmds.checkBox("checkPos", q=True, v=True)
        starendtCheck = cmds.radioButtonGrp("startEndMode", q=True, select=True)


        #アニメーションカーブの一覧を取得
        seletAnimCurves = cmds.keyframe(q=True, name=True)


        for selctAnimCurve in seletAnimCurves:


            #タンジェントの処理
            if checkTangent == True:
                #タンジェントのコピー
                keyInTangents = cmds.keyTangent(selctAnimCurve, q=1, ia=1)
                keyOutTangents = cmds.keyTangent(selctAnimCurve, q=1, oa=1)


                if starendtCheck == 1:
                    #スタートのタンジェントをエンドにペースト
                    cmds.keyTangent(selctAnimCurve, index=(len(keyInTangents)-1,), e=1, oa=keyInTangents[0])
                
                if starendtCheck == 2:
                    #エンドのタンジェントをスタートにペースト
                    cmds.keyTangent(selctAnimCurve, ia=keyOutTangents[-1], index=(0,), e=1)
            elif checkTangent == False:
                pass


            #値の処理
            if checkPosition == True:
                #値のコピー
                keyValue = cmds.keyframe(selctAnimCurve, q=1, vc=1)


                if starendtCheck == 1:
                #スタートの値をエンドにペースト
                    cmds.keyframe(selctAnimCurve, index=(len(keyValue) -1,), vc=keyValue[0], e=1)
                #keyValueはリスト。オブジェクトを選択していた場合、オブジェクトのすべてのアトリビュートが格納されている
                #キーが打たれている場所のキーのすべてのアトリビュートが入っている。
                #index=(len(keyValue) -1,)は選択したアニメーションカーブに打たれているキーの合計数に-1した整数。


                #エンドの値をスタートにペースト
                if starendtCheck == 2:
                    cmds.keyframe(selctAnimCurve, index=(0,), vc=keyValue[- 1], e=1)    


            elif checkPosition == False:
                pass



    #SetTimeにチェックが入っている。フレームを指定する場合の処理
    if cmds.checkBox("SetAnimCycleTime", q=True, value=True) == 1:


        #チェックボックスの状態を取得
        checkTangent = cmds.checkBox("checkTan", q=True, v=True)
        checkPosition = cmds.checkBox("checkPos", q=True, v=True)
        starendtCheck = cmds.radioButtonGrp("startEndMode", q=True, select=True)


        #アニメーションカーブの一覧を取得
        seletAnimCurves = cmds.keyframe(q=True, name=True)


        startFrame = cmds.intField("startIntBox", q=True, v=True)
        endFrame = cmds.intField("endIntBox", q=True, v=True)


        for selctAnimCurve in seletAnimCurves:


            #タンジェントの処理
            if checkTangent == True:
                #タンジェントのコピー
                keyInTangents = cmds.keyTangent(selctAnimCurve, q=1, ia=1)
                keyOutTangents = cmds.keyTangent(selctAnimCurve, q=1, oa=1)


                #スタートのタンジェントのコピー
                startInTangents = cmds.keyTangent(selctAnimCurve, q=1, ia=1, t=(startFrame,startFrame))
                startOutTangents = cmds.keyTangent(selctAnimCurve, q=1, oa=1, t=(startFrame,startFrame))
                #エンドのタンジェントのコピー
                endInTangents = cmds.keyTangent(selctAnimCurve, q=1, ia=1, t=(endFrame,endFrame))
                endtOutTangents = cmds.keyTangent(selctAnimCurve, q=1, oa=1, t=(endFrame,endFrame))


                if starendtCheck == 1:
                    #スタートのタンジェントをエンドにペースト
                    #cmds.keyTangent(selctAnimCurve, index=(len(keyInTangents)-1,), oa=keyInTangents[0], e=1)
                    cmds.keyTangent(selctAnimCurve, t=(endFrame,endFrame), oa=startInTangents[0], e=1)
                    cmds.keyTangent(selctAnimCurve, t=(endFrame,endFrame), oa=startOutTangents[0], e=1)
                    
                if starendtCheck == 2:
                    #エンドのタンジェントをスタートにペースト
                    cmds.keyTangent(selctAnimCurve, t=(startFrame,startFrame), ia=endtOutTangents[0], e=1)
                    cmds.keyTangent(selctAnimCurve, t=(startFrame,startFrame), ia=endInTangents[0], e=1)
            elif checkTangent == False:
                pass


            #値の処理
            if checkPosition == True:


                #キーの値を取得
                keyValue = cmds.keyframe(selctAnimCurve, q=1, vc=1)
                startValue = cmds.keyframe(selctAnimCurve, q=1, vc=1, t=(startFrame,startFrame))
                endValue = cmds.keyframe(selctAnimCurve, q=1, vc=1, t=(endFrame,endFrame))


                if starendtCheck == 1:
                #スタートの値をエンドにペースト
                    cmds.keyframe(selctAnimCurve, t=(endFrame,endFrame), vc=startValue[0] , e=1)
                    #vc=で指定した値に変えることができた。なのでvc＝にスタートフレームの値を入れると良さげだが。。？


                #エンドの値をスタートにペースト
                if starendtCheck == 2:
                    cmds.keyframe(selctAnimCurve, t=(startFrame,startFrame), vc=endValue[0], e=1)   


            elif checkPosition == False:
                pass
    



#UIでサイクルのスタートエンドコピーのとこのSetTimeのチェックOnOff判定
def onIntBoxEdit():
    cmds.intField("startIntBox", editable=True, e=True, q=True)
    cmds.intField("endIntBox", editable=True, e=True, q=True)
def offIntBoxEdit():
    cmds.intField("startIntBox", editable=False, e=True, q=True)
    cmds.intField("endIntBox", editable=False, e=True, q=True)



#たいらなキーをすべて削除
def deleteFlatAnimCurve():
    selAnimCurves = cmds.keyframe(q=True, name=True) #選択しているアニメーションカーブのリスト
    for selAnimCurve in selAnimCurves:
        selAnimCurveValue = cmds.keyframe(selAnimCurve, q=True, sl=True, vc=True)#アニメーションカーブの値をリストにする
        if len(set(selAnimCurveValue)) == 1:#setを使って、値のリストの中身がすべて同じかどうか調べる
            cmds.cutKey(selAnimCurve, cl=True)
        else:
            print("Non_Flat_AnimationCurve")



#5枠目のカーブを縦とか横に移動させるやつ
def moveCurveUp():
    moveFloatValue = cmds.floatField("moveFloatGraphBox", q=True, v=True)
    cmds.keyframe(animation="keys", relative=True, valueChange=float(moveFloatValue))
def moveCurveDown():
    moveFloatValue = cmds.floatField("moveFloatGraphBox", q=True, v=True)
    cmds.keyframe(animation="keys", relative=True, valueChange= - float(moveFloatValue))
def moveCurveLeft():
    moveFloatValue = cmds.floatField("moveFloatGraphBox", q=True, v=True)
    cmds.keyframe(animation="keys", relative=True, timeChange = - int(moveFloatValue))
def moveCurveRight():
    moveFloatValue = cmds.floatField("moveFloatGraphBox", q=True, v=True)
    cmds.keyframe(animation="keys", relative=True, timeChange = int(moveFloatValue))



#サイクルをコピペする
def copyPasteCycleKey():
    selectLists = cmds.ls( sl=True )
    selectcurve_list = cmds.keyframe(selectLists, q=True, n=True, sl=True)#選択したオブジェクトのＦカーブ一覧を取得
    for selectcurve in selectcurve_list:#取得したFカーブリストから、一本だけＦカーブを取り出し個別に処理
        lastKey = cmds.keyframe(selectcurve, q=True, tc=True)[-1]#tc= キーの時間の取得
        cmds.copyKey(selectcurve)
        cmds.pasteKey(selectcurve, time=(lastKey,lastKey), option="merge", copies=1, timeOffset=0, floatOffset =0, valueOffset= 0)
    cmds.selectKey(selectcurve_list)



#カーブを平均化
def oaSmoothKeys():
# /* oaSmoothKeys downloaded from Highend3d.com
# ''  
# ''  Highend3d.com File Information:
# ''  
# ''    Script Name: oaSmoothKeys
# ''    Author:  
# ''    Last Updated: Jun 14, 2008
# ''    Update/Change this file at:
# ''    http://Highend3d.com/maya/downloads/mel_scripts/animation/5051.html
# ''  
# ''  Please do not alter any information above this line
# ''  it is generated dynamically by Highend3d.com and will
# ''  be changed automatically on any updates.
# */
# /*
# ===========================================================================

# <NAME> oaSmoothKeys.mel </NAME>
# <VERSION> v1.1 </VERSION>
# <AUTHORS> Oleg Alexander (olegalexander@gmail.com) </AUTHORS>
# <WEBSITE> www.image-metrics.com </WEBSITE>

# <DESCRIPTION>

# "Blurs" selected keys. Perfect for animation cleanup and
# for smoothing jittery mocap data. (Simplify Curve is not the same thing!)
# </DESCRIPTION>

# <TO_USE>

# 	o Select at least 3 keys in the Graph Editor.
# 	o Execute 'oaSmoothKeys'.
# 	o Repeat as necessary. </TO_USE>

# <HISTORY>

# 	v1.1 (Saturday, June 14, 2008)
# 		o New blur algorithm, instead of moving average.

# 	v1.0 (Sunday, December 30, 2007)
# 		o Original Release 	</HISTORY>

# IF YOU ENJOY THIS MEL SCRIPT, PLEASE RATE IT. I WOULD APPRECIATE IT. THANK YOU!
# ===========================================================================
    selectCurves = []
    selectCurves = cmds.keyframe(q=True, name=True)


    if len(selectCurves) == 0:
        cmds.warning(u"Select at least 3 keys in the Graph Editor.")


    else:
        prevVal = []
        currVal = []
        nextVal = []
        average = []
        keys = [] # frame numbers
        sizeOfKeys = []
        dupCurve = []
        dupCurveVal = []


        for selectCurve in selectCurves:
            keys = cmds.keyframe(selectCurve, q=True, sl=True)
            sizeOfKeys = len(keys)


            if sizeOfKeys < 3:
                continue


            dupCurve = cmds.duplicate(selectCurve)


            i = 1
            ii = 1
            while i < sizeOfKeys-1:
                prevVal = cmds.keyframe(selectCurves, time = (keys[i-1], keys[i-1]), q=True, vc=True)
                currVal = cmds.keyframe(selectCurves, time = (keys[i], keys[i]), q=True, vc=True)
                nextVal = cmds.keyframe(selectCurves, time = (keys[i+1], keys[i+1]), q=True, vc=True)
                average = (prevVal[0] + currVal[0] + nextVal[0]) / 3
                cmds.keyframe(dupCurve[0], time=(keys[i], keys[i]), absolute=True, valueChange=(average))
                i +=1


            while ii < sizeOfKeys-1:
                dupCurveVal = cmds.keyframe(dupCurve[0], time=(keys[ii], keys[ii]) , q=True, vc=True)
                cmds.keyframe(selectCurves, time=(keys[ii], keys[ii]), absolute=True, valueChange=(dupCurveVal[0]))
                ii += 1


            cmds.delete(dupCurve[0])





#UIの作成
def AraiyCustomGraphEditor():



    if cmds.window('AraiyCustomGraphEditor' , exists=True):#同じウィンドウがあれば削除して再生性
        cmds.deleteUI('AraiyCustomGraphEditor' , window = True)


    AraiyCustomGraphEditor = cmds.window('AraiyCustomGraphEditor', title='AraiyCustomGraphEditor', widthHeight=(200, 450), resizeToFitChildren=True)
    #パネルがドッキングできるようにする
    cmds.workspaceControl('AraiyCustomGraphEditor', retain=False, floating=True)


    #パネル自体を親レイアウトにし、グラフエディタを子にして表示する
    Wingraphpanel = cmds.paneLayout(configuration='horizontal2', paneSize=[100,100,1], parent=AraiyCustomGraphEditor)
    graphmenu = 'graphEditor2'

    if cmds.window('AraiyCustomGraphEditor' , exists=True):#同じウィンドウがあれば削除して再生性
        cmds.deleteUI('AraiyCustomGraphEditor' , window = True)

    cmds.scriptedPanel(graphmenu, label=graphmenu ,type='graphEditor', parent=Wingraphpanel)
    cmds.setParent('..')


    #ボタンのレイアウトをここから下に記述します

    cmds.rowLayout(nc=6)#横に並べる枠の数を指定

    #1枠目のレイアウト
    cmds.frameLayout(labelVisible=0, borderVisible=1, width=150, height=100)
    cmds.columnLayout(adjustableColumn=False)
    cmds.rowLayout(nc = 4, cw4 = [60, 30, 30, 30])
    cmds.text('')
    cmds.text('X')
    cmds.text('Y')
    cmds.text('Z')
    cmds.setParent('..')
    cmds.rowLayout(nc = 4, cw4 = [60, 30, 30, 30])
    cmds.text('Translate')
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateX ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateX ", 0)' \
                    )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateY ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateY ", 0)' \
                )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateZ ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("translateZ ", 0)', \
                )
    cmds.setParent('..')
    cmds.rowLayout(nc=4, cw4=[60, 30, 30, 30])


    cmds.text('Rotate')
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateX ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateX ", 0)' \
                    )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateY ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateY ", 0)' \
                    )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateZ ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("rotateZ ", 0)' \
                    )
    cmds.setParent('..')
    cmds.rowLayout(nc=4, cw4=[60, 30, 30, 30])


    cmds.text('Scale')
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleX ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleX ", 0)' \
                    )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleY ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleY ", 0)' \
                    )
    cmds.checkBox(l = '', \
        onCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleZ ", 1)', \
        offCommand = 'AraiyuCustomGraphEditor.visAnimCurveCommand("scaleZ ", 0)' \
                    )
    cmds.setParent('..')
    cmds.rowLayout(nc=1, h=3)
    cmds.text('')
    cmds.setParent('..')
    cmds.rowLayout(nc=1)
    cmds.checkBox(l="Hide NonSelected \nAnimation Layer", \
        onCommand = "AraiyuCustomGraphEditor.nonActiveAnimLayerHide()", \
        offCommand = "AraiyuCustomGraphEditor.nonActiveAnimLayerShow()" \
                    )
    cmds.setParent('..')
    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆



    #2枠目のレイアウト
    cmds.frameLayout(labelVisible=0, borderVisible=1, width=195, height=100)
    cmds.columnLayout(adjustableColumn=False, rowSpacing=0)
    cmds.rowLayout(nc=2, cw2=[5, 20])
    cmds.text("")
    cmds.checkBox('InfinityCheckBox', l="Show Infinity", cc="AraiyuCustomGraphEditor.switchVisInfinities()")
    cmds.setParent('..')


    cmds.rowLayout(nc=5, cw5=[20, 35, 35, 35, 35], h=32)
    cmds.text("Pre")
    cmds.button(l="Cycle", c="AraiyuCustomGraphEditor.preInfinity('cycle')")
    cmds.button(l="Offset", c="AraiyuCustomGraphEditor.preInfinity('offset')")
    cmds.button(l="Linear", c="AraiyuCustomGraphEditor.preInfinity('linear')")
    cmds.button(l="Constant", w=50, c="AraiyuCustomGraphEditor.preInfinity('constant')")
    cmds.setParent('..')


    cmds.rowLayout(nc=5, cw5=[20, 35, 35, 35, 35])
    cmds.text("Post")
    cmds.button(l="Cycle", c="AraiyuCustomGraphEditor.postIninity('cycle')")
    cmds.button(l="Offset", c="AraiyuCustomGraphEditor.postIninity('offset')")
    cmds.button(l="Linear", c="AraiyuCustomGraphEditor.postIninity('linear')")
    cmds.button(l="Constant", w=50, c="AraiyuCustomGraphEditor.postIninity('constant')")
    cmds.setParent('..')
    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆



    #3枠目のレイアウト
    cmds.frameLayout(labelVisible=0, borderVisible=1, width=120, height=100)
    cmds.columnLayout(adjustableColumn=True, w=100, rowSpacing=1)
    cmds.button(l="Euler Filter", c="cmds.filterCurve()")
    cmds.button(l="Smooth Curve", c="AraiyuCustomGraphEditor.oaSmoothKeys()")
    cmds.rowLayout(nc=2, adjustableColumn=True, w=100, adj=True)
    cmds.checkBox("reverseCurveCheckBox", l="", v=True)
    cmds.button(l="Reverse Curve", c="AraiyuCustomGraphEditor.reverseAnimCurve()", w=100)
    cmds.setParent('..')#rowLayoutの〆
    cmds.button(l="Snap Key", c="AraiyuCustomGraphEditor.snapAnimCurve()")
    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆



    #4枠目のレイアウト
    cmds.columnLayout("animCurveKeyCycleframe", adjustableColumn=True, w=180, rowSpacing=5)


    cmds.frameLayout(labelVisible=0, borderVisible=1, width=175, height=100)
    cmds.columnLayout(adjustableColumn=True, w=180)
    cmds.rowLayout(nc = 1)
    cmds.radioButtonGrp("startEndMode", nrb=2, label1="Start > End", label2="End > Start", select=1, columnWidth=[(1, 90), (2, 90)])
    cmds.setParent('..')
    cmds.rowLayout(nc = 3, cw3 = [20, 70, 10])
    cmds.text(" ")
    cmds.checkBox("checkTan", l="Tangent", v=True)
    cmds.checkBox("checkPos", l="Position", v=True)
    cmds.setParent('..')


    cmds.rowLayout(nc=4, cw4 = [70, 20, 10, 20])
    cmds.checkBox("SetAnimCycleTime", l="Set Time", v=False, onCommand="AraiyuCustomGraphEditor.onIntBoxEdit()", offCommand="AraiyuCustomGraphEditor.offIntBoxEdit()")
    cmds.intField("startIntBox", width=40, editable=False)
    cmds.text(" ~ ")
    cmds.intField("endIntBox", width=40, editable=False)
    cmds.setParent('..')


    cmds.columnLayout()
    cmds.text(" ", h=2)
    cmds.rowLayout(nc=2, cw2 = [50, 20])
    cmds.text(" ")
    cmds.button(l="Run", c="AraiyuCustomGraphEditor.animCurveKeyCycle()", h=25, w=80)
    cmds.setParent('..')#rowLayoutの〆
    cmds.setParent('..')#columnLayoutの〆


    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆


    cmds.setParent('..')#columnLayoutの〆



    #5枠目のレイアウト
    cmds.columnLayout(adjustableColumn=True, w=132, rowSpacing=5)


    cmds.frameLayout(labelVisible=0, borderVisible=1, width=130, height=100)
    cmds.columnLayout(adjustableColumn=True, w=132)
    cmds.rowLayout(nc=1)
    cmds.text(" ", h=2)
    cmds.setParent('..')
    cmds.rowLayout(nc=2, cw2=[41, 10])
    cmds.text(" ")
    cmds.button(l="UP", w=40, h=25, c="AraiyuCustomGraphEditor.moveCurveUp()")
    cmds.setParent('..')
    cmds.rowLayout(nc=3)
    cmds.button(l="LEFT", w=35, h=25, c="AraiyuCustomGraphEditor.moveCurveLeft()")
    cmds.floatField("moveFloatGraphBox", w=50, h=30)
    cmds.button(l="RIGHT", w=35, h=25, c="AraiyuCustomGraphEditor.moveCurveRight()")
    cmds.setParent('..')
    cmds.rowLayout(nc=2, cw2=[41, 10])
    cmds.text(" ")
    cmds.button(l="DOWN", w=40, h=25, c="AraiyuCustomGraphEditor.moveCurveDown()")
    cmds.setParent('..')


    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆


    cmds.setParent('..')#columnLayoutの〆



    #6枠目のレイアウト
    cmds.frameLayout(labelVisible=0, borderVisible=1, width=130, height=100)
    cmds.columnLayout(adjustableColumn=True, w=100, rowSpacing=1)
    cmds.rowLayout(nc=1)
    cmds.text(l="etc...")
    cmds.setParent('..')
    cmds.rowLayout(nc=1)
    cmds.button(l="Delete Float Num Key", w=130, c="AraiyuCustomGraphEditor.deleteFloatFrame()")
    cmds.setParent('..')
    cmds.rowLayout(nc=1)
    cmds.button(l="Copy Key Cycle", w=130 ,c="AraiyuCustomGraphEditor.copyPasteCycleKey()")
    cmds.setParent('..')
    cmds.rowLayout(nc=1)
    cmds.button(l="Delete Flat AnimCurve", w=130, c="AraiyuCustomGraphEditor.deleteFlatAnimCurve()")
    cmds.setParent('..')
    cmds.setParent('..')#columnLayoutの〆
    cmds.setParent('..')#frameLayoutの〆




    cmds.showWindow(AraiyCustomGraphEditor)





AraiyCustomGraphEditor()

