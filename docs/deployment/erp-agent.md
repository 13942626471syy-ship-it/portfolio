# ERP Agent：主工程与学生助手

适用于已经获得对应源码或交付包授权的协作者。主工程与学生助手独立副本必须分别维护，不能混用目录、状态和验收记录。

## 规则与规划主工程

现有说明使用 Python、uv、PostgreSQL、Qdrant 和 FastAPI。依赖版本以目标工程的 `pyproject.toml` 与锁文件为准。

在主工程根目录的开发环境执行：

```bash
uv sync --all-groups
docker compose up -d postgres qdrant
uv run alembic upgrade head
uv run uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

数据库迁移需先确认专用开发库。不要将真实课堂状态或私人配置带入演示环境。服务启动后先检查 API 文档与 readiness，再运行需要数据库或证据检索的功能。

## 学生助手独立入口

现有 Windows 启动器支持独立端口及离线模式：

```powershell
.\Start-StudentAssistant.ps1 -Offline -WebPort 3004 -ApiPort 8016
```

对应本机入口为 `http://127.0.0.1:3004/student`。先使用离线确定性功能；模型讲解需要另外具备授权配置。本公开仓库不提供任何凭据。

截图来自该独立界面的历史演示，不是主工程当前搜索能力的完整证明。

## 验证与结果表达

- 规则计算、候选方案生成、执行回放、独立复验和真实课堂验证分别记录。
- 当前工程的测试门禁以其维护文档为准，不能用旧版测试数替代最新验收。
- 候选得分不等于官方成绩或全局最优。
- 运行超时、停止和未完成验证应明确记录，不写成通过。

本次没有启动服务、规划搜索或重跑完整测试。

[项目介绍](../../projects/erp-agent.md) · [部署总览](../deployment.md)
