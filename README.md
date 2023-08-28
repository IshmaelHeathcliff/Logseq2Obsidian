# 简介

一个简单的python实现的Logseq转到Obsidian的markdown格式转换程序



# 功能

- Front-matter格式转换

```
# Logseq
prop:: value

# Obsidian
---
prop: value
---
```

- alias识别与格式替换，需要Front-matter中有`alias`或`aliases`

```
# Logseq
[[alias]]

# Obsidian
[[title|alias]]
```

- 去除Logseq块属性

- TODO格式转换

```
# Logseq
- TODO something
- NOW something

# Obsidian
- [ ] something
- [x] something
```

- 代码块格式转换，去除代码块前`-`

