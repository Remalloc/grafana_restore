# Grafana 恢复工具文档

[中文文档](README_ZH-cn.md) | [English Doc](README.md)
## 概览

Grafana 恢复工具是一个旨在恢复 Grafana 数据的实用程序。该工具通过grafana内置数据表dashboard_version来还原被删除的dashboard。注意：本程序只可以还原dashboard，相应的组织关系等数据仍会丢失。

## 入门指南

### 先决条件

在开始之前，请确保您具备以下条件：

- 在您的系统上安装了 Python 3.7+。

## 安装

克隆包含 Grafana 恢复工具的代码库：
```shell
git clone https://github.com/Remalloc/grafana_restore.git
```

切换到项目目录：
```shell
cd grafana_restore
```

安装所需的 Python 包：
```shell
pip install -r requirements.txt
```

## 使用方法

填写main函数中的grafana的数据库链接，如果使用了默认的grafana数据库(sqlite)，需要复制数据库文件到项目目录，文件的默认位置为/var/lib/grafana/grafana.db

在grafana页面创建一个组织，并填写组织id
```python
def main():
    restore = Restore(db_url="sqlite:///grafana.db", org_id=8)
    restore.run()
```

调用 run 方法运行程序：
```python
restore.run()
```

如果是sqlite数据库，恢复完成后还需要将文件拷贝回原处