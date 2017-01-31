# Simple Regex

## 简介

[SRL] 是一个正则表达式的DSL，其文档见 [Simple Regex]。[Simple Regex] 通过将正则表达式转化为自然语言来增加可读性。正则表达式很强大，但新手入门门槛高。这个库加快了理解正则表达式的时间，非常适合新手学习。其原始实现是 PHP, 进行中的 Python 实现对应的仓库是 [soasme/SRL.py]。

## 快速起步

- 大小写不敏感
- 逗号是可选的
- 子查询需要使用括号
- Characters 指的是可以匹配文字的部分：例如 `letter`, `digit`, `literally`等
- Quantifiers 用于指定出现次数
- Groups 用于分组 Characters 和 Quantifiers，可用于做子查询
- Lookarounds 用于做向前向后标记
- Flags 是正则的标记，比如贪心，大小写敏感等
- Anchors 用于指定起止

## 基本使用

```python
srl = SRL('literally "color: ", capture (letter once or more) as "color", literally "."')
matches = srl.getMatches('Favorite color: green. Another color: yellow.')
print matches[0]['color'], matches[1]['color']
```

## 快速实现

- 使用 TDD 的方式，根据 PHP 项目的测试用例，快速构建起可用的 Builder
- 补齐 simple regex 文档页提供的测试用例
- 根据 Builder 写 Parser。
- 完成开源项目的标准配置：文档，证书，发版，注释等。

可针对 Python re 库的特性做一些小变动，但基本保持 API 与 SRL 库一致。
测试可分为文档测试和单元测试。单元测试通过 [SRL] 的所有用例，文档测试参照 beanstalkc 的文档测试。

## 进度

- 1 Sep, 2016 编写了所有文档页提及的构建器方法，并通过了 srl 库对 builder 的所有单元测试用例
- 2 Sep, 2016 继续完善 builder，使其通过了 [Simple Regex] Documentation 描述的所有特性，使用与 beanstalkc 测试类似的技术结合了文档和测试
- 6 Sep, 2016 注意到上游原始PHP实现分化出了规范和各种语言的实现，均为占坑无实现状态。加入开发讨论组 simpleregex.slack.com。加入 SimpleRegex Github Developer Team。[soasme/SRL.py] 与作者讨论后做为 SRL-Python 的官方实现。注册了 Pypi SRL 包名。
- 7 Sep, 2016 使用 lex yacc 实现了一个 parser，并将 parser 应用于文档测试。
- 8 Sep, 2016 通过了所有的测试，针对命名，Builder的行为与开发组讨论，发出了第一个实现PR。编写了2/3兼容。重写了Documentation的文档测试。增加了新特性：打印SRL对象时显示正则表达式。

[SRL]: https://github.com/TYVRNET/SRL
[Simple Regex]: https://simple
[soasme/SRL.py]: https://github.com/soasme/SRL.py)
