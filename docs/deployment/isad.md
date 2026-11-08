# ISAD：运行前提与构建流程

适用于获得授权的 Electron 桌面工程。不要套用历史 Tauri / 独立 Bridge 工程的运行说明。

## 环境

- Windows 10/11、Node.js 24、npm。
- MySQL 8.0.16 或更高版本。
- 需要正式图包和本地建模预览时，安装 StarUML，并在客户端配置可执行文件位置。

## 配置与初始化

依据工程中的配置模板创建后端环境配置，使用自己的数据库、JWT 和对象存储设置。不要复制演示账号口令或现有服务器地址。

在授权源码根目录执行：

```bash
npm install
npm run db:migrate
npm run db:seed
```

数据库迁移和初始化会改变目标数据库。先确认连接的是专用开发数据库，并阅读 seed 内容，不能对真实教学数据直接执行。

## 开发启动

分别在独立终端运行：

```bash
npm run server:dev
npm run dev
npm run admin:dev
```

分别对应后端、Electron/Vite 桌面开发和独立 Web 管理端。StarUML 集成位于 Electron 内部，不需要单独启动 Bridge。

默认后端端口为 3001，可先检查：

```powershell
curl.exe --fail http://127.0.0.1:3001/health
```

预期返回 `{"ok":true}`；若修改了后端端口，请同步调整地址。这个接口不能替代 MySQL、角色权限或 StarUML 集成验证。

用独立演示账号检查：新建分析 → 保存结构化内容 → 语义检查 → 草稿预览 → 正式图包 → 提交审核。草稿变化后应重新检查版本与产物准备度，不能用旧快照代替当前数据。

## 构建与验证

```bash
npm run admin:build
npm run desktop:dist
```

桌面打包脚本包含客户端构建、Windows NSIS 安装包生成和发布一致性检查。生产构建需要设置 `VITE_API_BASE_URL`；远程地址应使用 HTTPS，不携带凭据、查询串或片段。

已有检查入口包括 `npm run server:test`、`npm run test:ui`、`npm run verify:release`。本次未执行，不表示当前全部通过。

## 常见问题与更新

| 现象 | 检查方向 |
| --- | --- |
| 桌面打开但后端不可用 | 检查后端进程、API 地址与跨域配置；与 WhiteGZ 同时运行时处理默认端口冲突 |
| StarUML 预览失败 | 检查软件路径、输入准备度和失败原因；界面保留的旧成功预览不能当作本次成功 |
| 提交被版本或质量状态阻断 | 重新生成与当前 working data 一致的分析快照、质量报告和正式图包 |
| 数据库初始化失败 | 核对 MySQL 版本和专用开发库，不对真实教学库反复执行 seed |

升级前备份数据库、对象存储文件与私有配置，记录安装包和迁移版本。数据库已迁移时，回退客户端并不等于完成数据回滚；先验证旧版本兼容性或恢复经过核对的备份。

## 部署边界

本地对象存储是开发方案；云迁移规划不能写成已经完成的云部署。公开展示仓库不提供源码、安装包、数据库或实际服务器入口。

[项目介绍](../../projects/isad.md) · [部署总览](../deployment.md)
