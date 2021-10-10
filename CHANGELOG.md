# changelog

> alpha 버전 완료 일정: 2021.10.27

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