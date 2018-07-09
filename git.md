### git 有用操作
+ git 忽略已经提交的文件
```
git rm -f --cached dir/file
git add dir/file
git commit -m "删除版本库的东西"
```
### 展示log
`git log --graph --pretty=oneline --abbrev-commit`

### 删除远程分支
`git push origin --delete branchname`

### 删除本地分支
`git branch -d branchname`

### 拉取远程分支
`git fetch origin 远程分支名x:本地分支名x`
`git checkout -b 本地分支名x origin/远程分支名x`


## 换源
get remote set-url source
