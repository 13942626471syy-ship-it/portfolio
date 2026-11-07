# 运行与部署

## 先区分两个仓库用途

- **本公开仓库**：Markdown、已审核图片，通过 GitHub 阅读即可。
- **各产品私有工程**：包含实际应用、后端、数据库及构建配置，只有获得源码授权后才能按对应教程运行。

GitHub Pages 可以托管静态展示页面，不能运行 Express/FastAPI、MySQL、桌面客户端或真实业务接口。本次未启用 Pages，也未部署公共后端。

## 产品运行前提与构建流程

- [WhiteGZ](deployment/whitegz.md)：Node.js / Express 本地运行及发布检查。
- [ISAD](deployment/isad.md)：Electron 桌面端、后端、Web 管理端与 Windows 安装包。
- [ERP Agent](deployment/erp-agent.md)：规则/规划主工程与学生助手独立入口。
- [拾光盒子 CampusLoop](deployment/campusloop.md)：Flask MVP 本地运行及生产化边界。
- DNUI：涉及校园身份与真实业务环境，部署资料暂不公开。需要先形成独立演示环境与经过审核的配置模板。

教程依据相应工程的启动脚本、包配置与现有文档整理。这次完成的是文档和素材发布，不把命令存在写成当前机器已部署成功，也没有重新运行各产品完整测试。

## 从开发到发布的维护流程

1. **确定版本**：固定项目、分支与提交，区分主工程、演示副本和历史包。
2. **准备配置**：仅提交无真实值的配置模板，凭据留在部署环境；先使用合成数据。
3. **安装依赖**：优先使用锁文件和受支持的运行时，不把本机依赖目录打包进 Git。
4. **验证**：分开记录构建、单元测试、集成测试、界面回归与真实环境联调。
5. **预发布**：使用隔离环境核对数据库迁移、权限、文件访问、日志和错误恢复。
6. **交付**：标明版本、变更、依赖、已知限制、启动方式及回滚方法。
7. **发布后检查**：核对实际版本、健康检查、关键流程和资源链接；失败则回滚或明确停用。

这是建议的发布流程，不表示所有私有工程已经完成上述步骤。

## 本展示仓库的发布检查

本次对相对链接、图片指纹、图片元数据和待上传文件清单作了检查，并逐张核对所选截图。发布后核对远端文件与匿名访问结果。这些检查只针对展示资料，不替代产品测试。

后续可以在独立的文档流程中增加持续检查，但自动检查也不能替代截图与视频的人工隐私审核。

## 参考

- [GitHub：README 应包含什么](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [Excalidraw](https://github.com/excalidraw/excalidraw)：区分产品入口、功能与本地开发。
- [Immich](https://github.com/immich-app/immich)：截图、安装、文档与版本记录分层。
- [Hoppscotch](https://github.com/hoppscotch/hoppscotch)：演示、使用、开发与维护入口。

参考的是资料组织方式，不复制这些项目的代码或宣传成果。

[返回作品集](../README.md)
