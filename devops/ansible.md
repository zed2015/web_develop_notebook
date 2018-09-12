## set_fact not transfer str to int
> https://github.com/ansible/ansible/issues/15249
- ansible 2.7 版本之后解决了这件事情https://github.com/ansible/ansible/pull/32738

## 查看变量
> ansible -m setup host

## ansible 中的变量
- ansible 的当前文件夹 playbook_dir

## debug
- msg: 调试输出的消息
- var: 
```
- name: Command run line
  shell: date
  register: result
- debug: var=result.stdout verbosity=0

```




