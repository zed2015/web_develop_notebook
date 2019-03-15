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

### 暂存
`git stash`
`git stash list`
`git stash apply stash@{0}`

### 跟踪
`git branch --set-upstream branch-name origin/branch-name`
`git checkout -b branch-name origin/branch-name`


## 换源
get remote set-url origin source 


## 打包暂存区
- stashName=`git stash create`;
- git archive <options> $stashName


## git flow
> http://www.ruanyifeng.com/blog/2015/12/git-workflow.html
> http://www.open-open.com/lib/view/open1451353135339.html

## git rebase
git rebase --onto commit \[remote,commit, begin\] \[commit, end]

## git cherry-pick commit 
