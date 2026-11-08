# 展示资料 CI 配置模板

**状态：尚未启用。** 本地校验器与回归用例已经提供；本轮没有成功向仓库安装 GitHub Actions 工作流。

具有相应工作流写入权限的维护者，可以审核下方内容后保存为 `.github/workflows/showcase.yml`。模板仅运行公开资料检查，不部署产品，不使用 Secrets。启用后仍需查看首轮实际运行结果。

```yaml
name: Showcase checks

on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          persist-credentials: false
      - name: Test showcase validator
        run: python3 -m unittest discover -s tests -v
      - name: Check public files, links and media
        run: python3 scripts/validate_showcase.py
```

当前可在本地运行同样的检查，见[维护说明](maintenance.md#自动检查)。外部链接与素材隐私仍需人工核对。

[返回作品集](../README.md)
