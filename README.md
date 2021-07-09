# AutomaticPosting-Python
AutomaticPosting-Python

# [Custom Koapy](https://github.com/miniyus/AutomaticPosting-Koapy/tree/master)

# 설치방법

```bash
git clone https://github.com/miniyus/AutomaticPosting-Python.git

# 해당 프로젝트의 repository폴더로 이동합니다.
cd ./repository

# 해당 프로젝트의 참조 repository입니다.
git clone https://github.com/miniyus/AutomaticPosting-koapy.git

# anaconda 설치 후
activate x86

# koapy를 먼저 설치해야 의존성 에러가 나오지 않습니다.
# 추 후 koapy설치 없이, git clone 만으로 설치가 가능하게 수정할 예정입니다.
pip install koapy

# 받은 repository에서
cd ./repository/koapy

# 수동으로 install
# pip install koapy는 단지 의존성 해결을 위한 동작이며, 아래의 명령을 실행하지 않으면, 업종별 데이터를 불러올 수 없습니다.
python setup.py install
```

# 사용법

```bash
# find by sector code
main.py --sector {sector_code} --market {market_code}

# find by theme code
main.py --theme {theme_code}
```

## [change log](.changelog.md)