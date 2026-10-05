# 系统产品设计 · System Product Design

让 AI 把业务需求做成新人能上手、熟手能持续工作的系统：对象有状态，任务有工作台，流程有结果，电脑和手机分别设计交互。

**版本：1.4.0 · 许可证：MIT · 支持：Claude Code / Codex**

这是一个可独立安装的 Agent Skill，由 moodytiger 开源。适用于多模块业务系统、内部工具的新建或结构改造，也可以只用来做产品设计。公开版保留完整设计方法，去除了个人路径、内部链接和真实项目材料。

## 最快安装方式

把下面这段发给自己的 **Claude Code 或 Codex**：

> 请阅读 https://github.com/moodytiger-it/system-product-design 的 README，克隆这个仓库，按照说明把 system-product-design skill 安装到我正在用的工具。先检查是否已有同名 skill；有差异时保留原版并询问是否更新，不直接覆盖。安装后回读 SKILL.md 和 references，告诉我如何调用。此步只安装，不开始开发或发布系统。

也可以在**准备使用 skill 的电脑**（MacBook Pro、Studio、Linux 或 Windows）运行。需要 Git 和 Python 3.9+；skill 本身没有程序依赖，不要求 Node、飞书 CLI 或 Obsidian：

```bash
git clone https://github.com/moodytiger-it/system-product-design.git
cd system-product-design
python3 scripts/install.py --target both
```

只装一种工具时使用 `--target claude` 或 `--target codex`。Windows 可将 `python3` 换成 `py -3`。

| 工具 | 安装位置 | 调用方式 |
|---|---|---|
| Claude Code | `~/.claude/skills/system-product-design/` | `/system-product-design` + 业务问题 |
| Codex | `~/.agents/skills/system-product-design/` | `$system-product-design` + 业务问题 |

安装后打开新会话或重新加载 skills。路径依据：[Claude Code 官方说明](https://code.claude.com/docs/en/skills)、[Codex 官方说明](https://developers.openai.com/codex/skills/)。普通网页聊天不能通过这段命令自动读取电脑里的 skill。

安装器只复制本仓库的 skill 文件并逐文件校验，不运行项目、不联网、不安装额外包。同名且内容一致时保持原样；有差异时停止。如明确要更新，可使用 `--replace`，旧目录会先移到 `~/.local/share/moodytiger-skill-backups/system-product-design/`；不会覆盖同名目录的符号链接。`--home-dir` 可指定隔离的安装根目录，用于测试，无需修改 HOME。

## 装好后怎么用

```text
系统产品设计：把现有供应商资料页升级成采购每天用的系统。
采购在手机上补材料，主管在电脑上复核，退回后采购继续补充。
保留现有资料与技术栈。这次只交付产品设计，不开发、不上线。
```

常用触发词：**系统产品设计、做成真正的系统、把页面升级成系统、电脑和手机都要像系统**。也保留「按第二种搭系统」这一入口，只在系统搭建语境中使用。

告诉 AI 真实用户、最重要的工作、已有项目和这次终点即可。已有信息会复用，缺少的业务信息会明确待确认；无需自行选择技术栈或填完整模板。只要求设计就交付设计，要求原型或实现则按授权推进；开发不自动等于部署或对外发布。

## 它会交付什么

1. 模块与导航地图、核心对象与状态转换。
2. 关键工作流、异常修复、保存续做和结果找回。
3. 电脑与手机各自的页面结构和操作方式。
4. 产品内「开始使用」、快速开始、可重看的帮助。
5. 与请求一致的设计、可操作原型或真实系统。
6. 按模块的验收证据、接入边界和待完成项；真实运行时附恢复与接手材料。

v1.4 补充五项体验验收：参照图逐项对应实现与证据；按各角色产品内教程原路径完成任务；按明确场景交付真实手机预览；账号预览默认服务端只读并隔离跨标签身份；检查常用宽高下的入口可达，并保留能识别缺陷的失败案例。布局和预览按业务选择，不强制手机外框、iframe、三栏或固定导航数量。

适用于门店巡检、资料补件、内容工作台、业务协作等有操作闭环的系统。纯只读 BI、报告、落地页、小文案样式修改或后台接口修复不强制套用整套流程。

本规范保留**飞书账号登录**的组织默认：真实系统不用共享密码、Basic Auth 或模拟身份代替正式登录。外部组织如要适配其他身份平台，应在自己的项目规范中明确调整，而不是由 AI 擅自切换。

## 内容与边界

```text
skills/system-product-design/
├── SKILL.md                      # 完整执行规范
├── LICENSE
├── references/
│   ├── design-principles.md       # 设计原则概览
│   ├── workspace-example.md       # 虚构内容工作台示例
│   ├── task-spec.md               # 关键任务卡与模块覆盖表
│   ├── onboarding.md              # 入门与持续帮助
│   ├── system-readiness.md        # 完整性与运行条件
│   ├── acceptance-checklist.md    # 验收清单
│   └── experience-review.md       # 体验走查与失败案例
└── evals/evals.json               # 11 个虚构评测场景（原8个 + 新增3个）
```

相邻工作流、品牌或平台 skills 都是可选衔接，不是安装前置条件。本包不包含公司数据、账号凭据、后台服务或其他未公开 skills。调用外部系统时沿用项目的真实权限与可用工具。

评测场景用于复查范围、任务结构和证据纪律，不是已通过的真人试用或产品验收。设计、原型、真实接入、软件部署、业务接受分别核验。

## 下载、更新与维护

固定版本下载见 [v1.4.0 Release](https://github.com/moodytiger-it/system-product-design/releases/tag/v1.4.0)。`system-product-design-v1.4.0.tgz` 包含完整 skill 和许可证，`SHA256SUMS` 用于校验；解压后可将顶层 `system-product-design` 文件夹放到上述对应的 skills 目录。

从仓库更新时先 `git pull --ff-only`，再运行安装器；有差异时按提示决定是否 `--replace`。

维护者可运行：

```bash
python3 scripts/validate.py
python3 scripts/package.py
```

打包器只打包 skill 目录，输出到 `dist/`，使用固定排序与时间戳，可重复生成相同 SHA-256。提交改动前更新版本与 [CHANGELOG](CHANGELOG.md)，复查引用、公开内容和安装结果。欢迎通过 [Issues](https://github.com/moodytiger-it/system-product-design/issues) 或 PR 提出具体使用场景、卡点和改进建议。

## English

System Product Design is a standalone agent skill for turning business requirements into usable workspaces. It covers objects and states, module navigation, task flows, desktop/mobile interaction, onboarding, recovery, and evidence-based acceptance. Use it for a design brief, an interactive prototype, or an implementation within the user's requested scope.

Install with `python3 scripts/install.py --target claude`, `--target codex`, or `--target both`. Invoke `/system-product-design` in Claude Code or `$system-product-design` in Codex. The current detailed guidance is in Chinese. Adjacent skills are optional. The organization default is Feishu account login. Installation does not include cloud-chat or Cowork account installation.

Released by moodytiger under the [MIT License](LICENSE).
