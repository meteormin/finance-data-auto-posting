# changelog

> alpha 버전 완료 일정: 2021.10.27

## v2.0-alpha.8

### 2021.10.17

**feat**

기존 config 파일들 확장자 ini에서 json으로 변경

- 장고 프레임워크와 통합 시, 설정파일 내용을 코드를 통해서 수정할 수도 있는데, json이 수정과 읽기가 좀 더 편리하다고 판단하여 수정

DB 연동을 위한 준비

- 장고 통합 전에 standalone 버전은 SQLAlchemy를 사용하여 db 제어 예정

## v2.0-alpha.7

### 2021.10.16

**feat**

표 생성과 차트 생성 파일 분리하여 클래스로 작성

- fdap/app/infographic/table.py
    - DataFrame 생성 및 표 이미지 저장
- fdap/app/infographic/chart.py
    - 차트 이미지 저장
- 변경사항 infographic 프로토타입 모듈 반영 및 테스트 완료
    - [프로토타입 결과](./prototype/results)

## v2.0-alpha.6

### 2021.10.16

**feat**

- fdap/app/infographic.py
    - DataFrame 생성 및 차트, 표 관련 함수
- infographic 프로토타입 모듈 테스트 추가
    - 이미지 생성 및 저장 테스트 성공

## v2.0-alpha.5

### 2021.10.13

**feat**

- 패키지 루트 경로 변경
- 다른 python 패키지들과 유사하게 구조 변경

## v2.0-alpha.4

### 2021.10.12

**feat**

- 전체 구조 변경
    - src > app
    - koapy > kiwoom
    - koapy_service > kiwoom_service
    - tistory, refine 패키지 모듈 기능 및 목적에 따라 파일 분리
- 테스트 결과 저장 디렉토리 생성

**fix**

- tests 패키지 명을 사용할 수 없어 기존 테스트툴을 prototype으로 명명

## v2.0-alpha.3

### 2021.10.11

**feat**

- 티스토리 API 구현
    - 로그인 API: 완료
    - 포스팅 API: 테스트 필요
        - Post.list(포스팅 목록 불러오기): 완료
- 간단한 Test도구 생성
    - src.tests.testable
    - test 관련 logger 정의
- 기존 'modules' 패키지 'src'(으)로 변경
- customlogger
    - logs 및 logs/tests 폴더 없을 경우 생성 하게 수정
- opdart
    - Acnt 리스트 다루기 쉽게 AcntCollection 클래스 생성
- Refine
    - refine 모듈 구현, 데이터 정확도 체크 필요

**fix**

- 티스토리 API
    - 로그인 API: 크롤링 과정에서 발생하는 오류 해결
        - 원인: confirm 버튼 관련해서 클릭을 하지 않고 있었고, 마지막 confirm 버튼의 css 셀렉터를 잘못 입력했다.
    - 포스팅 API, Post 클래스 엔드포인트 및 리소르를 제대로 설정하지 않았었다.

## v2.0-alpha.2

### 2021.10.11

**feat**

- 티스토리 API 구현(테스트 필요!)
    - 로그인 API
    - 포스팅 API
- resources 디렉터리 추가
    - 업로드 이미지를 생성하면 해당 폴더에 저장 할 예정

## v2.0-alpha.1

### 2021.10.10

**feat**

v1 버전은 키움증권 API를 통해 데이터를 가져오는 단순한 프로그램이었습니다.

v2 버전은 open dart API, 블로그 포스팅 기능까지 전체 구현을 목적으로 개발 중입니다.

**개발중**

- modules
    - kiwoom: 키움 API 관련 모듈
    - opendart: Open Dart API 관련 모듈
    - tistory: Tistory API 관련 모듈
    - utils: 유틸리티 클래스 및 스크립트
    - refine: OpenDart 데이터 + 키움 API 데이터