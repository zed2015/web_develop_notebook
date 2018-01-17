
 ######################
 ##  tmux 快捷键     ##
 ######################

C-b ? 显示快捷键帮助
C-b C-o 调换窗口位置，类似与vim 里的C-w
C-b 空格键 采用下一个内置布局
C-b ! 把当前窗口变为新窗口
C-b " 模向分隔窗口
C-b % 纵向分隔窗口
C-b q 显示分隔窗口的编号
C-b o 跳到下一个分隔窗口
C-b 上下键 上一个及下一个分隔窗口
C-b C-方向键 调整分隔窗口大小
C-b c 创建新窗口
C-b 0~9 选择几号窗口
C-b c 创建新窗口
C-b n 选择下一个窗口
C-b l 切换到最后使用的窗口
C-b p 选择前一个窗口
C-b w 以菜单方式显示及选择窗口
C-b t 显示时钟
C-b ; 切换到最后一个使用的面板
C-b x 关闭面板
C-b & 关闭窗口
C-b s 以菜单方式显示和选择会话
C-b d 退出tumx，并保存当前会话，这时，tmux仍在后台运行，可以通过tmux attach进入 到指定的会话"

# 会话命令
C-x s 以菜单的方式查看并选择会话
C-x :new-session 新建一个会话
tmux new-session -s'my rails project'

tmux rename-session -t 1 "my session
C-x d 退出并保存会话
终端运行 tmux attach 返回会话

 ######################
 ##  vim快捷键       ##
 ###################### 


#窗口大小调整
纵向调整
:ctrl+w + 纵向扩大（行数增加）
:ctrl+w - 纵向缩小 （行数减少）
:res(ize) num  例如：:res 5，显示行数调整为5行
:res(ize)+num 把当前窗口高度增加num行
:res(ize)-num 把当前窗口高度减少num行
横向调整
:vertical res(ize) num 指定当前窗口为num列
:vertical res(ize)+num 把当前窗口增加num列
:vertical res(ize)-num 把当前窗口减少num列

# 与系统粘版的集成
+y +p

#以下命令将文中所有的字符串idiots替换成managers：

:1,$s/idiots/manages/g

#通常我们会在命令中使用%指代整个文件做为替换范围：

:%s/search/replace/g

#以下命令指定只在第5至第15行间进行替换:

:5,15s/dog/cat/g

#以下命令指定只在当前行至文件结尾间进行替换:

:.,$s/dog/cat/g

#以下命令指定只在后续9行内进行替换:

:.,.+8s/dog/cat/g

#你还可以将特定字符做为替换范围。比如，将SQL语句从FROM至分号部分中的所有等号（=）替换为不等号（<>）：

:/FROM/,/;/s/=/<>/g

#在可视化模式下，首先选择替换范围, 然后输入:进入命令模式，就可以利用s命令在选中的范围内进行文本替换。

