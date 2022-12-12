# ysoserial fixed

为防止仓库过分膨胀，删除`ysoserial-0.0.6-SNAPSHOT-all.jar`包

## 如本地没有相关jar包

执行：

- step 1

```bash
git clone https://github.com/Bin4xin/sweet-ysoserial
```

- step 1

```bash
cd sweet-ysoserial && mvn clean package -DskipTests
```

- step 3

拷贝`target/ysoserial-0.0.6-SNAPSHOT-all.jar`文件到与`shiro_deserialization.py`同目录下

更多参阅[README.md#error](https://github.com/Bin4xin/sweet-ysoserial/blob/main/README.md#error)

或者提[new issues](https://github.com/wnltt/Ant_colony/issues/new)

## 本地有jar包

拷贝`ysoserial-0.0.6-SNAPSHOT-all.jar`文件到与`shiro_deserialization.py`同目录下