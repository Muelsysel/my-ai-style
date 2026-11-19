# my-ai-style

个人 AI 协作规范与素材库，也是其他仓库的规约来源：一份模板加几份提示词，从这里安装到各个项目。

解决的问题只有两个：每个新仓库都要重新交代同一套协作规则；写作、汇报类任务反复调整语气和格式。

## 结构

| 路径 | 角色 | 是否进目标仓库 |
| --- | --- | --- |
| `agents/AGENTS.md` | 协作规约模板，唯一可编辑的规则源 | 是，由脚本安装到根目录 |
| `prompts/文风提示词（写作与改稿指令）-writing-style.md` | 文风提示词，完整版与精简版 | 否，按需取用 |
| `prompts/汇报PPT提示词（技术幻灯片风格与版式）-ppt-technical-deck.md` | 技术汇报 PPT 的配色与版式规范 | 否，按需取用 |
| `style/文风卡（个人写作特征核对清单）-voice-card.md` | 个人文风画像，用于核对产出、补样本 | 否 |
| `scripts/install.py` | 把规约安装或更新到目标仓库 | 否 |
| `AGENTS.md` | 本仓库自身的规约，脚本生成，勿手改 | — |

## 命名约定

- Markdown 文件统一用 `中文（简单描述作用）-英文.md`：中文在前便于浏览，英文在后便于检索和命令行补全。
- 例外是 `README.md`、`AGENTS.md`、`LICENSE` 这类由平台或工具按固定名识别的文件，保持原名。
- 目录保持英文短名（`agents`、`prompts`、`style`、`scripts`），重命名文件时路径前缀不变。

## 接入方式

### 安装规约（推荐）

```bash
python scripts/install.py D:/Work/some-repo          # 安装或升级
python scripts/install.py --check D:/Work/some-repo  # 只检查是否落后
python scripts/install.py --dry-run D:/Work/some-repo
python scripts/install.py --force D:/Work/some-repo  # 目标没有项目索引段落时强制覆盖
```

安装规则：目标仓库已有的 `## 5. 项目索引` 整段保留，其余内容用模板覆盖；生成文件首行写入模板版本，重复执行即升级。目标已有 `AGENTS.md` 但找不到该段落时脚本中止（退出码 3），避免覆盖别人的自定义规则，确认覆盖再加 `--force`。

### 子模块

```bash
git submodule add https://github.com/Muelsysel/my-ai-style.git .ai-style
```

规约文字需要参与代码评审时用这种方式；日常只要模型上下文生效，用上面的脚本更省事。

### 手动复制

只拷 `agents/AGENTS.md`，把第 5 节换成项目自己的验证命令、文档索引和禁改目录。

## 提示词怎么用

- 写作或改稿：先附文风提示词的完整版，填掉三个槽位；日常短任务用精简版。
- 汇报 PPT：整段粘贴 PPT 提示词，按题材选配色方案，题材不明时默认方案 A。
- 产出核对：拿文风卡逐条比对，比凭感觉判断可靠。

## 维护约定

- 规则只改 `agents/AGENTS.md` 和 `prompts/` 下的提示词，根目录 `AGENTS.md` 是安装脚本的产物。
- `VERSION` 只随规约模板（`agents/AGENTS.md`）的内容变化；提示词和仓库基础设施的改动记在版本记录的未发布一节。
- 交付前在本仓库跑 `python scripts/install.py --check .`，生成物与模板不一致就重跑安装脚本。
