
# Punica Cli

-[概览](#概览)
-[安装](#安装)
-[快速开始](#快速开始)
-[开始](#开始)

## 概览
欢迎使用Punica! Punica 机会拥有一切开发dapp所需要的功能。

### 特点
* Punica-Cli 支持智能合约编译，部署，调用，测试。
* Punica-Cli 实现了Python和TypeScript版本。
* Punica 网站提供了健全的文档和合约模板。
* 自动化生成dapp工程目录，提供多种box，是的开发者很容易的基于Punica-Boxes进行开发。
* 智能合约测试配置与smartx有相同的配置标准。
* 提供智能合约包管理工具。

```shell
punica
Usage: punica [OPTIONS] COMMAND [ARGS]...

Options:
  -p, --project PATH  Specify a punica project directory.
  -v, --version       Show the version and exit.
  -h, --help          Show this message and exit.

Commands:
  compile  Compile the specified contracts to avm and...
  deploy   Deploys the specified contracts to specified...
  init     Initialize new and empty Ontology DApp...
  invoke   Invoke the function list in default-config or...
  node     Ontology Blockchain private net in test mode.
  scpm     Smart contract package manager，support...
  smartx   Ontology smart contract IDE,SmartX...
  test     Unit test with specified smart contract
  unbox    Download a Punica Box, a pre-built Ontology...
  wallet   Manager your ontid, account, asset.
```

## 安装

安装之前请先确保下面的工具已经安装

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Git](https://git-scm.com/)

然后，执行下面的命令进行安装

```shell
pip install punica
```
or

```shell
python setup.py install
```

## 快速开始

为了使用Punica命令，你需要先创建一个Punicax项目。

### 创建Punica项目

#### 初始化一个新项目

可以使用`punica init`命令创建一个空项目

```shell
$punica init --help
Usage: punica init [OPTIONS]

  Initialize new and empty Ontology DApp project.

Options:
  -h, --help  Show this message and exit.
```

使用下面的命令生成一个新项目

```shell
sss$ punica init
Downloading...
Unpacking...
Unbox successful. Enjoy it!
sss$
```

生成的项目结构如下：

```shell
$ ls
punica-config.json
wallet
README.md
src
contracts
test
```

- `contracts/`: 用于存放合约文件.
- `src/`: 用于存放dapp js和html等相关文件.
- `test/`: 合约代码测试文件.
- `wallet/`: 用于存放钱包文件.
- `punica-config.json` 用于配置区块链网络

#### 创建一个Box项目

Punica Box 是punica dapp模板库，你可以下载你感兴趣的下载，然后基于该项目进行创建你的dapp。

- 创建一个新文件夹

```shell
mkdir tutorialtoken
cd tutorialtoken
```

- 下载Box

```shell
punica unbox tutorialtoken
```


```shell
punica unbox --help
Usage: punica unbox [OPTIONS] BOX_NAME

  Download a Punica Box, a pre-built Ontology DApp project.

Options:
  -h, --help  Show this message and exit.
```

**Note**:

- 你可以使用`punica unbox <box-name>`免费下载任意的Box项目。
- 你可以在你的项目根目录使用punica的其他命令，也可以`-p` or `--project` 选项指定使用哪个项目。

### 编译

使用下面的命令编译你的合约


```shell
punica compile
```

如果执行成功，将会在contracts文件夹下生成build文件夹


```shell
contacts
    ├─build
    │      contract.avm
    │      contract_abi.json
```

如果你想使用punica更多的用法，你可以使用`punica compile --help`命令查看。

```shell
$ punica compile --help
Usage: punica compile [OPTIONS] CONTRACT_NAME

  Compile the specified contracts to avm and abi file.

Options:
  --contracts TEXT  Compile specified contracts files in contracts dir.
  --local BOOLEAN   Use local compiler.
  -h, --help        Show this message and exit.
```

`--contracts`选项用于指定编译哪个合约文件
`--local`选项用于指定使用哪个编译器

### 部署

部署之前，你要关心两个配置文件，一个是`punica-config.json`,该文件配置使用的区块链网络，另一个配置文件是