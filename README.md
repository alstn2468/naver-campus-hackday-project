## 그룹 일일커밋 스터디 플랫폼

### 주제 선정 배경
나태해질 수 있는 마음을 바로잡고 동료 개발자와 함께 성장하기 위해<br>
그룹 일일커밋 스터디를 진행할 수 있는 플랫폼을 개발한다.

### 필수 구현사항
- 기본적인 유저 등록 및 로그인 기능
- 커밋 스터디 그룹 관리
  - 그룹 생성 및 관련 메타 정보 관리 (e.g. 시작-종료 시간, 일일 최소 커밋 횟수, etc.)
  - 구성원 초대
- 그룹 스터디 진행
  - 그룹 구성원의 일간 커밋 여부 체크
    - 커밋 여부를 체크하는 방식에는 여러방식 존재
      - Git remote 서비스 API를 활용하는 방식은 기본적으로 포함
  - 구성원 일일 커밋 여부에 대한 UI 구성
  - 그룹 스터디 종료
    - 스터디 종료에 따른 결과 산출
    - 결과에 대한 UI 구성

### To Do

#### Back-End

- [ ] 모델 구조 설계
- [ ] 설계된 모델기반 모델 생성
- [ ] 유저 등록 및 로그인 기능 (`Github OAuth` 이용)
- [ ] 개인 사용자 커밋 여부 확인 기능
- [ ] 그룹 생성 기능
- [ ] 그룹 초대 기능
- [ ] 그룹 삭제 기능
- [ ] 그룹 스터디 생성 기능
- [ ] 그룹 스터디 목록 표시 기능
- [ ] 그룹 구성원 일간 커밋 확인 기능
- [ ] 그룹 구성원 월간 커밋 확인 기능
- [ ] 그룹 구성원 년간 커밋 확인 기능
- [ ] 그룹 스터디 종료 기능
- [ ] 그룹 스터디 종료시 평가 기능

#### Front-End

- [ ] local storage를 활용한 로그인 기능
- [ ] 메인 페이지 구성
- [ ] 개인 사용자 정보 페이지 구성
- [ ] 그룹 생성 페이지 구성
- [ ] 그룹 관리 페이지 구성
  - [ ] 그룹원 초대 컴포넌트 구성
  - [ ] 그룹 삭제 컴포넌트 구성
  - [ ] 그룹원 삭제 컴포넌트 구성
- [ ] 그룹 정보 페이지 구성
- [ ] 스터디 생성 페이지 구성
- [ ] 스터디 목록 페이지 구성
  - [ ] 진행 중 스터디 컴포넌트 구성
  - [ ] 종료 된 스터디 컴포넌트 구성
- [ ] 스터디 관리 페이지 구성
  - [ ] 스터디 종료 컴포넌트 구성
  - [ ] 스터디 수정 컴포넌트 구성

### Dependencies

#### Back-End

- Python
- pip
- django
- django rest framework
- django-rest-framework-social-oauth2

#### Front-End

- Node.js
- npm
- React
- redux
- react-redux